def count_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return len(df[(df[col] <= lower) | (df[col] >= upper)])

def remove_outliers_iqr(df, cols):
    q1 = df[cols].quantile(0.25)
    q3 = df[cols].quantile(0.75)
    iqr = q3 - q1

    is_not_outlier = (df[cols] >= (q1 - 1.5 * iqr)) & (df[cols] <= (q3 + 1.5 * iqr))
    return df[is_not_outlier.all(axis=1)]