import pandas as pd


def transform_data_old(file):
    dataset = pd.DataFrame()
    dataset = pd.read_csv(file)

    dataset.rename(columns={'energy;': 'energy'}, inplace=True)
    dataset['energy'] = dataset['energy'].str.replace(';', '')

    dataset["energy"] = pd.to_numeric(dataset["energy"])

    dataset.info()
    return dataset


def getDataset(file):
    dataset = pd.DataFrame()
    dataset = pd.read_csv(file, sep=';')

    dataset = dataset.dropna(axis=0)

    # dataset.info()
    # print(dataset.iloc[58])
    return dataset


# def make_new_list()

file_name = 'data_copy3.csv'
dataset = getDataset(file_name)
# dataset.info()
