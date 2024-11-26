import pandas as pd
import os

df = pd.read_csv('../data/sp500/sp500_stocks.csv')

df['Date'] = pd.to_datetime(df['Date'])

df = df.drop(columns=['High', 'Low', 'Open', 'Close'])

print(df.shape)
print(df.isnull().sum())

# Filtrar los registros a partir de 2014
df = df[df['Date'].dt.year >= 2014].dropna()

print(df.shape)
print(df.isnull().sum())

df['Date'] = pd.to_datetime(df['Date'])

# Agrupando por Símbolo y remuestreando semanalmente la Fecha, tomando la media de Adj Cierre y sumando Volumen.
weekly_df = df.set_index('Date').groupby('Symbol').resample('W').agg({
    'Adj Close': 'mean',
    'Volume': 'sum'
}).reset_index()

print(weekly_df.shape)
print(weekly_df.isnull().sum())

weekly_df.to_csv(os.path.join('../cleandata', 'sp500Weekly.csv'), index=False)

print("Procesamiento completado")