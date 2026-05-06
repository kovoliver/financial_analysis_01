def variance_ratio(df, group, target_col):
    grand_mean = df[target_col].mean()

    group_stats = df.groupby(group)[target_col].agg(['mean', 'count'])
    
    between_var = (group_stats['count'] * (group_stats['mean'] - grand_mean) ** 2).sum() / (len(df) - 1)
    total_var = df[target_col].var()

    return between_var/total_var