import pandas as pd
import numpy as np
from get_cleaned_data import get_cleaned_data as gcd
from outliers import remove_outliers_iqr
import matplotlib.pyplot as plt

df = gcd(
    filepath="global_finance_sales_dataset_1200_rows.csv", 
    date_cols=['Date'], 
    outlier_callback=remove_outliers_iqr,
    outlier_cols=['Revenue_USD', 'COGS_USD'],
    dropna_subset=['Revenue_USD', 'COGS_USD', 'Budget_Target'],
    remove_duplicates=True
)

df = df.sort_values('Date')

df['Days'] = (df['Date'] - df['Date'].min()).dt.days
x = df['Days'].values
y = df['Revenue_USD'].values

slope, intercept = np.polyfit(x, y, 1)
df['Linear_Trend'] = slope * x + intercept

print(f"Lineáris egyenlet: y = {slope:.2f}x + {intercept:.2f}")

fit = np.polyfit(x, np.log(y), 1)
b = fit[0]
a = np.exp(fit[1])

df['Exponential_Trend'] = a * np.exp(b * x)

print(f"Exponenciális egyenlet: y = {a:.2f} * e^({b:.4f}x)")


mse_linear = np.mean((df['Revenue_USD'] - df['Linear_Trend'])**2)
mse_exponential = np.mean((df['Revenue_USD'] - df['Exponential_Trend'])**2)

print(f"Lineáris MSE: {mse_linear:,.2f}")
print(f"Exponenciális MSE: {mse_exponential:,.2f}")

if mse_linear < mse_exponential:
    print("A Lineáris trend a pontosabb.")
else:
    print("A Exponenciális trend a pontosabb.")





# # 1. Értelmezési tartomány kiterjesztése (mai naptól + 30 nap)
# x_future = np.linspace(0, x.max() + 30, 200)

# # Függvények kiszámítása a kiterjesztett tartományon
# y_lin_plot = slope * x_future + intercept
# y_exp_plot = a * np.exp(b * x_future)

# # 2. Ábra létrehozása
# plt.figure(figsize=(12, 7), dpi=100)

# # Eredeti adatok (halványabb pontok, hogy a trend látványos legyen)
# plt.scatter(df['Date'], y, color='gray', alpha=0.3, label='Tényleges adatok', s=15)

# # Dátumok generálása a jövőbeli x értékekhez az ábrázoláshoz
# start_date = df['Date'].min()
# future_dates = pd.to_datetime([start_date + pd.Timedelta(days=int(val)) for val in x_future])

# # Trendvonalak rajzolása
# plt.plot(future_dates, y_lin_plot, color='blue', label=f'Lineáris trend (MSE: {mse_linear:,.0f})', linewidth=2)
# plt.plot(future_dates, y_exp_plot, color='red', linestyle='--', label=f'Exponenciális trend (MSE: {mse_exponential:,.0f})', linewidth=2)

# # 3. Design és érthetőség
# winner = "Lineáris" if mse_linear < mse_exponential else "Exponenciális"
# plt.title(f'Revenue Trendszámítás és Előrejelzés\nGyőztes modell: {winner}', fontsize=14, pad=15)
# plt.xlabel('Dátum', fontsize=12)
# plt.ylabel('Revenue (USD)', fontsize=12)

# # Rácsozás és formázás
# plt.grid(True, linestyle=':', alpha=0.6)
# plt.legend(frameon=True, shadow=True)
# plt.xticks(rotation=35)

# # Az y tengely formázása, hogy ne legyen tudományos jelölés (e+05)
# plt.ticklabel_format(style='plain', axis='y')

# plt.tight_layout()
# plt.show()