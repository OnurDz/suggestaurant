import pandas as pd
import numpy as np
from suggestaurant import func_def as f

def get_data():
    df = pd.read_csv('./suggestaurant/data/data.csv')
    return df

def get_relevant(df, category):
    return df.loc[df['categories'] == category]

def get_discounted(df):
    return df.loc[df['discount'] > 0]

def sort_by_eco(df):
    df_sorted = df.sort_values(by=['eco'], ascending=False)
    return df_sorted

def sort_by_best(df):
    scores = []
    points_df = df[['speed', 'taste', 'serv_quality']]
    points = points_df.to_numpy()
    for p in points:
        scores.append(f.defuzz(p))
    df['score'] = scores
    df_sorted = df.sort_values(by=['score'], ascending=False)
    return df_sorted
    

def return_by_best():
    df = get_data()
    sorted = sort_by_best(df) # all data in sorted

    sorted_res = sorted['name'] # res names in sorted
    sorted_score = sorted['score'] # scores in sorted
    sorted_categories = sorted['categories']
    discount = sorted['discount']
    eco = sorted['eco']

    result = pd.DataFrame()
    result['name'] = sorted_res
    result['score'] = sorted_score
    result['categories'] = sorted_categories
    result['discount'] = discount
    result['eco'] = eco
    return result

