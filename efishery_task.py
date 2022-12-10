import pandas as pd
import numpy as np
import json
import requests

def load_data():
    url = 'https://raw.githubusercontent.com/fikrifikar/eFishery-Task/main/soal-2.json'
    df_fish = pd.read_json(url)
    df_fish = df_fish.rename_axis('index').reset_index()
    return df_fish


def split_data_comodity(df_fish):
    df_split = df_fish['komoditas'].str.split(",| |/").explode()
    df_done = df_split[(df_split!="")].reset_index(drop=True)
    df_done = df_done.rename_axis('index1').reset_index()
    return df_done


def split_data_weight(df_fish):
    df_split2 = df_fish['berat'].str.split(",| ").explode()
    df_done2 = df_split2[(df_split2!="")].reset_index(drop=True)
    df_done2 = pd.DataFrame (df_done2, columns = ['berat'])
    return df_done2


def cleansing(df_done2):
    to_remove = ['lele', 'bawal', 'nila', 'kakap', 'kembung',
       'tongkol', 'salem', 'rata2', 'kg', 'kurang',
       'dari', 'rata', 'ratarata', 'setengah',
       'kilo', 'kecuali', 'gak', 'nentu', 'setengan', 'tau', 'katanya',
       'cuma', 'jaga', 'warung', 'cumi', 'kg.', 'kg.udang']
    df_done2 = df_done2.loc[~df_done2.berat.isin(to_remove)].reset_index(drop=True)
    df_done2 = df_done2.rename_axis('index2').reset_index(level=0)
    return df_done2


WEIGHT_MAP = {
    '6kg': 6000,
    '1kg': 1000,
    '2kg': 2000,
    '5kg': 5000,
    '3kg': 3000,
    '4kg': 4000,
    '7kg': 7000,
    '8kg': 8000,
    '1': 1000,
    '2': 2000,
    '3': 3000,
    '4': 4000,
    '5': 5000,
    '6': 6000,
    '7': 7000,
    '8': 8000,
    '3-4kg': 3500,
    '1.5' : 1500,
    '1/2' : 500,
    '1-2kg': 1500,
    '2-4kg': 4000,
    '2-5kg': 5000,
    '4-6kg': 6000,
    '4g': 4,
    '1-5kg': 5000
}


def filter_weight(df_done2, WEIGHT_MAP):
    df_done2['berat_scale'] = df_done2['berat']
    df_done2['berat_scale'] = df_done2['berat_scale'].map(WEIGHT_MAP)
    df_done2 = df_done2.drop(columns=['berat'])
    return df_done2

def merge(df_done, df_done2):
    merge_df = pd.merge(df_done, df_done2,  how='inner', left_on = 'index1', right_on = 'index2').drop(columns=['index1', 'index2'])
    final_df = merge_df.sort_values(by=['berat_scale'], ascending=False)
    print(final_df)


def main():
    df_fish = load_data()
    df_done = split_data_comodity(df_fish)
    df_done2 = split_data_weight(df_fish)
    df_done2 = cleansing(df_done2)
    df_done2 = filter_weight(df_done2, WEIGHT_MAP)
    merge(df_done, df_done2)

if __name__ == "__main__":
    main()