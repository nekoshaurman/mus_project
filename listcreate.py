import pandas as pd
import numpy as np
from random import randint
from random import shuffle
from numpy.linalg import norm


# user_favorite is np.array
def get_list(ref_dataset, user_favorite):
    added = []
    count_tracks = len(ref_dataset["id"].to_numpy())  # how many tracks at all
    list_to_user = pd.DataFrame()
    likes = len(user_favorite)
    if likes > 5:
        likes = 5
    from_likes = likes * 2
    if likes != 0:
        while len(added) < likes:
            i = randint(0, len(user_favorite)-1)

            track = ref_dataset.loc[ref_dataset["id"] == user_favorite[i]]  # liked track (DataFrame)

            if track.iloc[0]["id"] not in added:
                list_to_user = pd.concat([list_to_user, track], ignore_index=True)  # add track to list
                added = list_to_user["id"].to_numpy()

        while len(added) < likes + from_likes:
            i = randint(0, len(user_favorite)-1)

            track = ref_dataset.loc[ref_dataset["id"] == user_favorite[i]]

            list_to_user = get_recommend(track.iloc[0]["id"], ref_dataset, list_to_user)
            added = list_to_user["id"].to_numpy()

    while len(added) < 21:
        i = randint(0, count_tracks)  # choose random track

        track = ref_dataset.iloc[i]

        if track["id"] not in added:
            list_to_user = pd.concat([list_to_user, track.to_frame().T], ignore_index=True)
            added = list_to_user["id"].to_numpy()
    return list_to_user


def get_recommend(track_id, ref_dataset, list_to_user):
    ref_dataset["mood_vec"] = ref_dataset[["valence", "energy"]].values.tolist()
    added = list_to_user["id"].to_numpy()
    i = 0

    track = ref_dataset.loc[ref_dataset["id"] == track_id]  # find track from likes
    valence = track.iloc[0]["valence"]
    energy = track.iloc[0]["energy"]
    track_moodvec = np.array([valence, energy])

    ref_dataset["distances"] = ref_dataset["mood_vec"].apply(lambda x: norm(track_moodvec - np.array(x)))

    ref_dataset_sorted = ref_dataset.sort_values(by="distances", ascending=True)

    while i != 2:
        k = randint(1, 5)

        track = ref_dataset_sorted.iloc[k]  # add 2 of 5 nearest

        if track["id"] not in added:
            list_to_user = pd.concat([list_to_user, track.to_frame().T], ignore_index=True)
            added = list_to_user["id"].to_numpy()
            i += 1
    list_to_user = list_to_user.drop("distances", axis=1)
    list_to_user = list_to_user.drop("mood_vec", axis=1)
    return list_to_user


def get_dataset(file):
    data_tracks = pd.DataFrame()
    data_tracks = pd.read_csv(file, sep=';')

    data_tracks = data_tracks.dropna(axis=0)

    return data_tracks


def get_users(file):
    data_users = pd.DataFrame()
    data_users = pd.read_csv(file, sep=';')

    count = len(data_users.id)

    for index in range(0, count):
        user_favorite = data_users.iloc[index]  # get Series
        user_favorite = user_favorite.likelist  # get String
        if len(user_favorite) > 0:
            user_favorite = user_favorite[1:-1]
            user_favorite = user_favorite.replace("'", "")
            user_favorite = user_favorite.split()
            user_favorite = np.array(user_favorite)
            data_users.at[index, "likelist"] = user_favorite  # save numpy array
    return data_users

#dataset_music = get_dataset("data_copy3.csv")
#dataset_users = get_users("data_users.csv")
#track = dataset_music.loc[dataset_music["id"] == "7w87IxuO7BDcJ3YUqCyMTT"]
#print(type(track))
#data_users = get_users("data_users.csv")
#data_users.info()
#(data_users)