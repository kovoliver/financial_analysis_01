import pandas as pd
from outliers import count_outliers_iqr, remove_outliers_iqr
import matplotlib.pyplot as plt
import seaborn as sns
from variance_analysis import variance_ratio

pd.set_option('display.float_format', '{:,.2f}'.format)
pd.options.display.float_format = '{:,.2f}'.format

df = pd.read_csv("global_finance_sales_dataset_1200_rows.csv", parse_dates=['Date'])

print(df.shape)
print(df.isnull().sum())
print(df.duplicated().sum())

df.drop_duplicates(inplace=True)

print("outlierek száma (Revenue_USD)", count_outliers_iqr(df, 'Revenue_USD'))
print("outlierek száma (COGS_USD)", count_outliers_iqr(df, 'COGS_USD'))

df_original = df.copy()

df.dropna(inplace=True)

df = remove_outliers_iqr(df, ['Revenue_USD', 'COGS_USD'])

print("aszimmetria (Revenue_USD): ", df['Revenue_USD'].skew())
print("csúcsosság (Revenue_USD): ", df['Revenue_USD'].kurt())

# Q1 = df['Revenue_USD'].quantile(0.25)
# Q3 = df['Revenue_USD'].quantile(0.75)
# Me = df['Revenue_USD'].median()

# print("Q1: ", Q1)
# print("Me: ", Me)
# print("Q3: ", Q3)

# F = ((Q3 - Me) - (Me - Q1)) / ((Q3 - Me) + (Me - Q1))
# print("F mutató: ", F)

"""
    Alapvető bevételi és költségmutatók
"""

#teljes bevétel
revenue_sums = df_original['Revenue_USD'].sum()
print('Teljes bevétel: ', revenue_sums)
cogs_sums = df_original['COGS_USD'].sum()
print('Teljes költség: ', cogs_sums)

cogs_revenue_ratio = cogs_sums/revenue_sums
print('Bevétel/költség arány: ', cogs_revenue_ratio*100, "%", sep="")

"""
    Régiónkénti mutatók
"""

#bevétel régiónként
revenue_by_region = df_original.groupby('Region')['Revenue_USD'].sum()
print("Régiónkénti bevételek:\n", revenue_by_region, sep="")
print("*****************************************************")

#költség régiónként
cogs_by_region = df_original.groupby('Region')['COGS_USD'].sum()
print("Régiónkénti költségek:\n", cogs_by_region, sep="")
print("*****************************************************")

#költség/bevétel arány régiónként
cogs_revenue_ratio_by_region = cogs_by_region/revenue_by_region * 100
print("Régiónkénti költség/bevétel arány:\n", cogs_revenue_ratio_by_region, sep="")
print("*****************************************************")

#jövedelmezőség régiónként
profit_margin_by_region = (revenue_by_region-cogs_by_region)/revenue_by_region
print("Régiónkénti jövedelmezőség:\n", profit_margin_by_region, sep="")
print("*****************************************************")


"""
    Termékkategóriánkénti mutatók
"""

#bevétel termékkategóriánként
revenue_by_category = df_original.groupby('Product Category')['Revenue_USD'].sum()
print("Termékkategóriánkénti bevételek:\n", revenue_by_category, sep="")
print("*****************************************************")

#költség termékkategóriánként
cogs_by_category = df_original.groupby('Product Category')['COGS_USD'].sum()
print("Termékkategóriánkénti költségek:\n", cogs_by_category, sep="")
print("*****************************************************")

#költség/bevétel arány termékkategóriánként
cogs_revenue_ratio_by_category = cogs_by_category / revenue_by_category * 100
print("Termékkategóriánkénti költség/bevétel arány:\n", cogs_revenue_ratio_by_category, sep="")
print("*****************************************************")

#jövedelmezőség termékkategóriánként
profit_margin_by_category = (revenue_by_category - cogs_by_category) / revenue_by_category
print("Termékkategóriánkénti jövedelmezőség:\n", profit_margin_by_category, sep="")
print("*****************************************************")

"""
    Célmutatók
"""
#milyen százalékban teljesítették a régiók a célt
budget_target_by_region = df.groupby('Region')['Budget_Target'].sum()
print("A régiók bevételi céljai:\n", budget_target_by_region, sep="")

#a régiók bevételi céljainak teljesítése
revenue_target_achievement_by_region = revenue_by_region/budget_target_by_region*100
print("A régiók bevételi céljai:\n", revenue_target_achievement_by_region, sep="")

#az egyes termékcsoportok mennyire teljesítették a bevételi célt
budget_target_by_category = df.groupby('Product Category')['Budget_Target'].sum()
revenue_target_achievement_by_category = revenue_by_category/budget_target_by_category*100
print("A kategóriák bevételi céljai:\n", revenue_target_achievement_by_category, sep="")

"""
    A tervezett bevétel mennyire korrelál a tényleges bevétellel.
"""
corr_basis = df[['Revenue_USD', 'Budget_Target']]
rev_bud_correlation = corr_basis.corr(method='pearson')
print("Korreláció a jövedelem és a tervezett jövedelem között: ", round(rev_bud_correlation.iloc[0, 1], 3))

#ügyfélelégedettség és kedvezmény közötti kapcsolat
corr_basis = df[['Discount_Percent', 'CSAT']]
disc_csat_correlation = corr_basis.corr(method='spearman')
print('Korreláció a kedvezmény és az ügyfélelégedettség között: ', round(disc_csat_correlation.iloc[0, 1], 3))

eta_squared_region = variance_ratio(df, 'Region', 'Revenue_USD')
print("Régió-bevétel kapcsolat: ", eta_squared_region)

"""
    Kapcsolat szorossága a termékkategória és a bevétel között.
"""
eta_squared_prod_cat = variance_ratio(df, 'Product Category', 'Revenue_USD')
print("Termékkategória-bevétel kapcsolat: ", eta_squared_prod_cat)