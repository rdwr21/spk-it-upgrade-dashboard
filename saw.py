import pandas as pd

def normalize_matrix(df, benefit_cols, cost_cols):

    norm = df.copy()

    for col in benefit_cols:
        norm[col] = df[col] / df[col].max()

    for col in cost_cols:
        norm[col] = df[col].min() / df[col]

    return norm


def calculate_saw(df, weights, benefit_cols, cost_cols):

    norm = normalize_matrix(df, benefit_cols, cost_cols)

    weighted = norm * weights

    score = weighted.sum(axis=1)

    ranking = score.sort_values(ascending=False)

    return ranking, norm