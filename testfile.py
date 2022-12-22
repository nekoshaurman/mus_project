import transform_data as data
import pandas as pd
from random import randint
import numpy as np
from numpy.linalg import norm

pd.set_option('display.max_columns', None)
file_name = 'data_copy3.csv'
dataset_src = data.getDataset(file_name)
dataset_src["mood_vec"] = dataset_src[["valence", "energy"]].values.tolist()

like_list = ["5IPaGvxQmoL60m5i0eRz8n",  # Reflect ClariS
             "5dI3N3YCNaQJxL3U9f2oMg",  # border ClariS
             "6C7RJEIUDqKkJRZVWdkfkH",  # Stronger Kanye West
             "1R2SZUOGJqqBiLuvwKOT2Y",  # Gangnam style PSY
             "3fyMH1t6UPeR5croea9PrR",  # Best I ever had Drake
             "7w87IxuO7BDcJ3YUqCyMTT",  # Pumped Up Kicks Foster The People
             "7iP1c4SKzbR2TzEvcKpGdB"]  # Dippin' Shake Yurufuwa Gang

favorite_list = []


# 5 из лайков
# 5 рандомных
# берем 5 лайков и ищем по 2 схожих с ними

def recommend(track_id, ref_dataset, list_to_user):
    added = list_to_user["id"].to_numpy()
    i = 0

    track = ref_dataset.loc[ref_dataset["id"] == track_id]
    valence = track.iloc[0]["valence"]
    energy = track.iloc[0]["energy"]
    track_moodvec = np.array([valence, energy])

    ref_dataset["distances"] = ref_dataset["mood_vec"].apply(lambda x: norm(track_moodvec - np.array(x)))

    ref_dataset_sorted = ref_dataset.sort_values(by="distances", ascending=True)

    while i != 2:
        k = randint(1, 5)
        track = ref_dataset_sorted.iloc[k]
        if track["id"] not in added:
            list_to_user = pd.concat([list_to_user, track.to_frame().T], ignore_index=True)
            added = list_to_user["id"].to_numpy()
            i += 1
    return list_to_user


def getList(ref_dataset, user_favorite):
    added = []
    count_tracks = len(ref_dataset["id"].to_numpy())
    list_to_user = pd.DataFrame()
    likes = len(user_favorite)
    if likes > 5:
        likes = 5
    from_likes = likes * 2
    if likes != 0:
        while len(added) < likes:
            i = randint(0, len(user_favorite)-1)
            track = ref_dataset.loc[ref_dataset["id"] == user_favorite[i]]
            if track.iloc[0]["id"] not in added:
                list_to_user = pd.concat([list_to_user, track], ignore_index=True)
                added = list_to_user["id"].to_numpy()

        while len(added) < likes + from_likes:
            i = randint(0, len(user_favorite) - 1)
            track = ref_dataset.loc[ref_dataset["id"] == user_favorite[i]]
            list_to_user = recommend(track.iloc[0]["id"], dataset_src, list_to_user)
            added = list_to_user["id"].to_numpy()

    while len(added) < 20:
        i = randint(0, count_tracks)
        track = ref_dataset.iloc[i]
        if track["id"] not in added:
            list_to_user = pd.concat([list_to_user, track.to_frame().T], ignore_index=True)
            added = list_to_user["id"].to_numpy()
    list_to_user = list_to_user.drop("distances", axis=1)
    list_to_user = list_to_user.drop("mood_vec", axis=1)
    return list_to_user


list_tracks = getList(dataset_src, like_list)  # favorite_list)
print(list_tracks)

