import pandas as pd

df = pd.read_csv('../data/eu etf/Morningstar - European ETFs.csv')

columns_to_keep = ['isin', 'fund_name', 'category', 'risk_rating', 'performance_rating', 'investment_strategy', 'dividend_frequency', 'roe', 'asset_stock', 'asset_bond', 'country_exposure', 
 'ongoing_cost', 'management_fees', 'nav_per_share_currency', 'nav_per_share', 'latest_nav_date', 'fund_trailing_return_ytd', 'fund_trailing_return_3years', 'fund_trailing_return_5years', 
 'fund_trailing_return_10years', 'long_term_projected_earnings_growth', 'historical_earnings_growth']

df = df[columns_to_keep]

def classify_fund_type(row):
    category = row['category'].lower() if pd.notna(row['category']) else ''
    
    if 'equity' in category.lower():
        return 'equity'
    elif 'bond' in category.lower():
        return 'bond'
    
    asset_stock = row['asset_stock']
    asset_bond = row['asset_bond']
    
    if pd.notna(asset_stock) and pd.notna(asset_bond):
        if asset_stock > asset_bond:
            return 'equity'
        elif asset_bond > asset_stock:
            return 'bond'
    
    # Si son iguales o no hay datos, asumir que es 'equity'
    return 'equity'

df['fund_type'] = df.apply(classify_fund_type, axis=1)

# Reordenar las columnas para que 'fund_type' sea la segunda
cols = df.columns.tolist()
cols.insert(3, cols.pop(cols.index('fund_type')))
df = df[cols]

print(df)

print(df.isnull().sum())

# Rellenar los valores nulos de 'dividend_frequency' con 'Acc', dado que el dataset solo tenia valores para los fondos que reparten dividendos
# y no para el resto, que son de acumulacion.
df['dividend_frequency'].fillna('Acc', inplace=True)

# Eliminar las filas con valores nulos en los campos clave que no pueden ser nulos
df = df.dropna(subset=['nav_per_share', 'management_fees', 'ongoing_cost', 'fund_trailing_return_ytd'])  

print(df.isnull().sum())

df.to_csv('../cleandata/eu_etf_dataset_cleaned.csv', index=False)

print("Dataset transformado y guardado")