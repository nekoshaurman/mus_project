import transform_data as data
import pandas as pd
from random import randint
import numpy as np
from numpy.linalg import norm

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
file_name = 'data_copy3.csv'
dataset_src = data.get_dataset(file_name)

#data_users = pd.DataFrame({"id": [],
                           #"likelist": []})
#data_users.to_csv("data_users.csv", sep=";", index=False)

data_users = data.get_users("data_users.csv")

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
            i = randint(0, len(user_favorite) - 1)
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


# def setPreferences(valence, energy):


list_tracks = data.get_list(dataset_src, like_list)  # favorite_list)
#print(list_tracks)
track_to_user = list_tracks.iloc[0]
artist_name = track_to_user.artist_name
track_name = track_to_user.track_name
#artist_name = track_to_user.iloc[0]["artist_name"]
#track_name = track_to_user.iloc[0]["track_name"]
track_text = str(1) + ". " + track_name + " --- " + artist_name + "\n"
#(track_text)









id1 = "743ghre8231u8"
like1 = "7iP1c4SKzbR2TzEvcKpGdB"
like2 = "5dI3N3YCNaQJxL3U9f2oMg"
id2 = "fuiuwerg8348"
like3 = "1R2SZUOGJqqBiLuvwKOT2Y"
like4 = "5IPaGvxQmoL60m5i0eRz8n"
id3 = "t43gj3jgerg"
like5 = "7iP1c4SKzbR2TzEvcKpGdB"
like6 = "7w87IxuO7BDcJ3YUqCyMTT"
#arr = np.array(["5IPaGvxQmoL60m5i0eRz8n", "5dI3N3YCNaQJxL3U9f2oMg"])
#data_users = pd.DataFrame({"id": ["t43gj3jgerg"],
                           #"likelist": [arr]})
#data_users = pd.DataFrame({"id": [],
                           #"likelist": []})
#print(data_users)


id = 597132545
count = len(data_users.index)
if count == 0:
    print("add new 1")
    new = np.array([like5])
    new_user = pd.DataFrame({"id": [id],
                             "likelist": [new]})
    data_users = pd.concat([data_users, new_user], ignore_index=True)
else:
    if id in data_users.id.unique():
        print("add prev")
        index = data_users[data_users["id"] == id].index[0]
        new_list = data_users.loc[data_users.id == id]
        new_list = new_list.iloc[0]["likelist"]
        if like5 not in new_list:
            new_list = np.append(new_list, like5)
        data_users.at[index, "likelist"] = new_list
    else:
        print("add new 2")
        new = np.array([like5])
        new_user = pd.DataFrame({"id": [id],
                                 "likelist": [new]})
        data_users = pd.concat([data_users, new_user], ignore_index=True)

user_favorite = data_users.loc[data_users.id == 597132545]
user_favorite = user_favorite.iloc[0]["likelist"]
print(user_favorite)
#print(data_users)
#data_users = pd.DataFrame({"id": [],
                           #"likelist": []})
data_users.to_csv("data_users.csv", sep=";", index=False)
#data_users = pd.read_csv("data_users.csv", sep=';')
#new_list = data_users.iloc[0]  # Get Series
#new_list = new_list.likelist  # Get String
#new_list = new_list[1:-1]
#new_list = new_list.replace("'", "")
#new_list = new_list.split()
#new_list.split()
#new_list = np.array(new_list)
#data_users.at[index, "likelist"] = new_list
#print(data_users)
#new_list = data_users.loc[data_users.id == id3]
#new_list = new_list.iloc[0]["likelist"]
#print(type(new_list))
#trackid = "7w87IxuO7BDcJ3YUqCyMTT"
#track_name = dataset_src.loc[dataset_src.id == trackid]
#print(track_name)
#artist_name = track_name.iloc[0]["artist_name"]
#track_name = track_name.iloc[0]["track_name"]
#track_text = track_name + artist_name

#track = dataset_src.iloc[53]
#artist_name = track.artist_name
#track_name = track.track_name
#track_text = track_name + " --- " + artist_name
#print(track_text)
