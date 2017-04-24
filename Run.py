import codecs
import csv
import json

from bs4 import BeautifulSoup
import urllib3

# MAP_POINTS_CSV_FILE = "PlacesGreenpeaceSPB.csv"
MAP_POINTS_CSV_FILE = "PlacesGreenpeaceMSK.csv"

def getDataFromSite(i):
    site_base = []
    http = urllib3.PoolManager()
    URL = 'http://recyclemap.ru/index.php?task=infopoint&pointid=' + str(i) + '&tmpl=component'
    response = http.request('GET', URL)

    soup = BeautifulSoup(response.data, fromEncoding='utf-8')
    # soup = BeautifulSoup(html_doc, 'html.parser')
    for x in soup.findAll('div'):
        if (x.has_attr('data-id')):
            if(x.get("data-id") != ""):
                site_id = x.get("data-id")
                site_latitude = x.get("data-lat")
                site_longitude = x.get("data-lng")
                print("ИД:", site_id, "Координаты:", site_latitude, site_longitude)

                image_lst = []
                point_image = soup.find('div', attrs={'class': 'point_image'})
                if (point_image):
                    for a in point_image.findAll('a'):
                        # point_contact_site = point_contact_site+" "+a.string
                        image_lst.append(a.get("href"))
                    print("Изображения:", image_lst)

                point_title = soup.find('div', attrs={'class': 'point_title'})
                print("Название:", point_title.span.text)

                point_fractions = soup.find('div', attrs={'class': 'point_fractions trash_type sm_trash_type'})
                fractions = []
                if (point_fractions):
                    for sp in point_fractions.findAll('span'):
                        fractions.append(sp.get('data-tooltip'))
                    print("Типы сырья:", fractions)

                point_address = soup.find('div', attrs={'class': 'point_address'})
                print("Адрес:",point_address.string.strip())

                spoiler_inside = soup.find('div', attrs={'class': 'spoiler_inside'})
                print("Информация:",spoiler_inside.text.strip())

                time_schem = soup.find('table', attrs={'class': 'time_schem'})
                work_schedule = []
                work_schedule_days = []
                work_schedule_times = []
                if (time_schem):
                    print("Расписание:")
                    for tri in time_schem.findAll('tr'):
                        for thi in tri.findAll('th'):
                            work_schedule_days.append(thi.text)
                        for tdi in tri.findAll('td'):
                            # if(tdi.get('class') == 'holiday'):
                            #     tdi.text = 'holiday'
                            work_schedule_times.append(tdi.text)
                    days_num = 0
                    for days in work_schedule_days:
                        work_schedule.append({days:work_schedule_times[days_num]})
                        days_num+=1
                print(work_schedule)

                cofebreack = soup.find('div', attrs={'class': 'cofebreack'})
                coffee_break = ""
                if(cofebreack):
                    coffee_break = ' '.join(cofebreack.text.split())
                    print(coffee_break)

                point_contact = soup.find('div', attrs={'class': 'point_contact'})
                # point_contact_phone = ""
                # point_contact_email = ""
                # point_contact_site = ""
                point_contact_lst = []
                if(point_contact):
                    print("Контакты:")
                    for sp in point_contact.findAll('span'):
                        point_contact_lst.append({sp.get("class")[0]:sp.string})
                    # for sp in point_contact.findAll('span', attrs={'class': 'phone'}):
                    #     point_contact_phone=point_contact_phone+" "+sp.string
                    #     print(sp.get("class")[0] + ":", sp.string)
                    # for sp in point_contact.findAll('span', attrs={'class': 'email'}):
                    #     point_contact_email = point_contact_email + " " + sp.string
                    #     print(sp.get("class")[0] + ":", sp.string)
                    for a in point_contact.findAll('a'):
                        # point_contact_site = point_contact_site+" "+a.string
                        point_contact_lst.append({a.get("class")[0]:a.string})
                        print(a.get("class")[0]+":", a.string)
                    print(point_contact_lst)

                point_comments = soup.find('div', attrs={'class': 'point_comments'})
                point_comments_list = []
                if (point_comments):
                    if(len(point_comments.findAll('div', attrs={'class': 'point_comment'})) > 0):
                        print("Последние комментарии:")
                    point_comments_id = 0
                    for divs in point_comments.findAll('div', attrs={'class': 'point_comment'}):
                        comment_author_ava = divs.find('div', attrs={'class': 'comment_author_ava'})
                        comment_author_name = divs.find('div', attrs={'class': 'comment_author_name'})
                        comment_author_date = divs.find('div', attrs={'class': 'comment_author_date'})
                        comment_body = divs.find('div', attrs={'class': 'comment_body'})
                        point_comment_author_ava = ""
                        point_comment_author_name = ""
                        point_comment_author_date = ""
                        point_comment_body = ""
                        print(str(point_comments_id+1))
                        if(comment_author_ava):
                            point_comment_author_ava = comment_author_ava.img.get("src")
                            print(" Аватар:", comment_author_ava.img.get("src"))
                        if (comment_author_name):
                            point_comment_author_name = comment_author_name.text.strip()
                            print(" Имя:", comment_author_name.text.strip())
                        if (comment_author_date):
                            point_comment_author_date = comment_author_date.text.strip()
                            print(" Дата:", comment_author_date.text.strip())
                        if (comment_body):
                            point_comment_body = comment_body.text.strip()
                            print(" Текст:", comment_body.text.strip())
                        comment = {'id':point_comments_id,
                                   'author_avatar': point_comment_author_ava,
                                   'author_name': point_comment_author_name,
                                   'publish_date': point_comment_author_date,
                                   'body': point_comment_body}
                        point_comments_list.append(comment)
                        point_comments_id+=1

                site_base.append({'site_id': site_id,
                                  'site_latitude': site_latitude,
                                  'site_longitude': site_longitude,
                                  'site_title':point_title.span.text,
                                  'site_images':image_lst,
                                  'site_fractions':fractions,
                                  'site_address':point_address.string.strip(),
                                  'site_point_info':spoiler_inside.text.strip(),
                                  'site_work_schedule':work_schedule,
                                  'site_coffee_break':coffee_break,
                                  'site_contacts':point_contact_lst,
                                  # 'site_contact_phone': point_contact_phone,
                                  # 'site_contact_email': point_contact_email,
                                  # 'site_contact_site': point_contact_site,
                                  'site_comments': point_comments_list
                                  })
                return site_base

with codecs.open(MAP_POINTS_CSV_FILE, encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    i = 0
    db_PlacesGreenpeace = []
    # row_count = sum(1 for row in reader)
    # print(row_count)
    for row in reader:
        if 0 < i :# < 10:
            print("\n\n"+str(row))
            db_id = row[0]
            db_city = 'spb'
            db_latitude = row[1]
            db_longitude = row[2]
            db_title = row[3]
            db_reiting = row[4]
            db_content_text = row[5]
            db_address = row[6]
            db_content = row[7]
            db_cats = row[8]
            site_base = getDataFromSite(db_id)
            db_PlacesGreenpeace.append({
                'id': db_id,
                'city': db_city,
                'latitude': db_latitude,
                'longitude': db_longitude,
                'title': db_title,
                'raiting': db_reiting,
                'fractions': db_content_text,
                'address': db_address,
                'site_db': site_base
            })
        i += 1
        pass

    print(">",db_PlacesGreenpeace)

    json.dumps(db_PlacesGreenpeace)
    with open((MAP_POINTS_CSV_FILE+'.json'), 'w') as outfile:
        json.dump(db_PlacesGreenpeace, outfile)
    #
    # for rec in db_PlacesGreenpeace:
    #     _site_base = rec['site_db']
    #     for srec in _site_base:
    #         srec_site_comments = srec['site_comments']
    #         if(srec_site_comments):
    #             print(srec_site_comments)
