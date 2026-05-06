"""
    Veszem a target col értékét, kiszámolom az átlagot.

    Külső szórás megvalósítása:
        - csoportosítok a megfelelő ismérv szerint (Region)
        - kiszámolom az átlagokat az ismérv és target col szerint
        - (db a kategóriában) * (kategória értéke - átlag) ** 2

    Belső szórás megvalósítása:
        - simán csak a target_col szerint számolom a varianciát

    A kettőt elosztom egymással.
"""

def variance_ratio(df, group, target_col):
    grand_mean = df[target_col].mean()

    group_stats = df.groupby(group)[target_col].agg(['mean', 'count'])
    
    between_var = (group_stats['count'] * (group_stats['mean'] - grand_mean) ** 2).sum() / (len(df) - 1)
    total_var = df[target_col].var()

    return between_var/total_var