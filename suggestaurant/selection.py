import pandas as pd
import numpy as np
import func_def as f

def get_data():
    df = pd.read_csv('./data/data.csv')
    return df

def get_relevant(df, category):
    return df.loc[df['categories'] == category]

def get_discounted(df):
    return df.loc[df['discount'] > 0]

def sort_by_best(df):
    scores = []
    points_df = df[['speed', 'taste', 'serv_quality']]
    points = points_df.to_numpy()
    for p in points:
        scores.append(f.defuzz(p))
    df['score'] = scores
    df_sorted = df.sort_values(by=['score'], ascending=False)
    return df_sorted
    

def main():
    df = get_data()
    print(sort_by_best(df))

if __name__ == '__main__':
    main()