import pandas as pd

from tqdm import tqdm
from joblib import delayed
from joblib import Parallel

from utils import get_data_fom_site

N_PLACES = 20 * 1000

if __name__ == "__main__":
    places = Parallel(n_jobs=32)(delayed(get_data_fom_site)(place_id_) for place_id_ in tqdm(range(N_PLACES)))
    df_places = pd.concat([pd.DataFrame.from_dict(place_, orient="index").T for place_ in places  if place_])
    df_places.to_csv("all_points.csv", index=False)