import os
import urllib3

from bs4 import BeautifulSoup

os.environ['PYTHONWARNINGS'] = "ignore:Unverified HTTPS request"


def get_data_fom_site(point_id):
    site_base = []
    http = urllib3.PoolManager()
    url = 'http://recyclemap.ru/index.php?task=infopoint&pointid=' + \
        str(point_id) + '&tmpl=component'
    response = http.request('GET', url)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    soup = BeautifulSoup(response.data, from_encoding='utf-8', features="lxml")
    # soup = BeautifulSoup(html_doc, 'html.parser')
    for x in soup.findAll('div'):
        if x.has_attr('data-id'):
            if x.get("data-id") != "":
                site_id = int(x.get("data-id"))
                site_latitude = float(x.get("data-lat"))
                site_longitude = float(x.get("data-lng"))
                # print("ИД:", site_id, "Координаты:", site_latitude, site_longitude)

                image_lst = []
                point_image = soup.find('div', attrs={'class': 'point_image'})
                if point_image:
                    for a in point_image.findAll('a'):
                        # point_contact_site = point_contact_site + " " + a.string
                        image_lst.append(a.get("href"))
                    # print("Изображения:", image_lst)

                point_title = soup.find('div', attrs={'class': 'point_title'})
                # print("Название:", point_title.span.text)

                point_fractions = soup.find(
                    'div', attrs={
                        'class': 'point_fractions trash_type sm_trash_type'})
                fractions = []
                if point_fractions:
                    for sp in point_fractions.findAll('span'):
                        fractions.append(sp.get('data-tooltip'))
                    # print("Типы сырья:", fractions)

                point_address = soup.find(
                    'div', attrs={'class': 'point_address'})
                # print("Адрес:", point_address.string.strip())

                spoiler_inside = soup.find(
                    'div', attrs={'class': 'spoiler_inside'})
                # print("Информация:", spoiler_inside.text.strip())

                time_schem = soup.find('table', attrs={'class': 'time_schem'})
                work_schedule = []
                work_schedule_days = []
                work_schedule_times = []
                if time_schem:
                    # print("Расписание:")
                    for tri in time_schem.findAll('tr'):
                        for thi in tri.findAll('th'):
                            work_schedule_days.append(thi.text)
                        for tdi in tri.findAll('td'):
                            # if(tdi.get('class') == 'holiday'):
                            #     tdi.text = 'holiday'
                            work_schedule_times.append(tdi.text)
                    days_num = 0
                    for days in work_schedule_days:
                        work_schedule.append(
                            {days: work_schedule_times[days_num]})
                        days_num += 1
                # print(work_schedule)

                cofebreack = soup.find('div', attrs={'class': 'cofebreack'})
                coffee_break = ""
                if cofebreack:
                    coffee_break = ' '.join(cofebreack.text.split())
                    # print(coffee_break)

                site_base.append({'site_id': site_id,
                                  'site_latitude': site_latitude,
                                  'site_longitude': site_longitude,
                                  'site_title': point_title.span.text,
                                  'site_images': image_lst,
                                  'site_fractions': fractions,
                                  'site_address': point_address.string.strip(),
                                  'site_point_info': spoiler_inside.text.strip(),
                                  'site_work_schedule': work_schedule,
                                  'site_coffee_break': coffee_break,
                                  })
                return site_base[0]
