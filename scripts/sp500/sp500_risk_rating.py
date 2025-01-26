import pandas as pd

sp500_data = pd.read_csv('../cleandata/sp500Weekly.csv')
etf_data  = pd.read_csv('../cleandata/eu_etf_dataset_predict.csv')

sp500_data['Date'] = pd.to_datetime(sp500_data['Date'])  # Convertir la columna de fechas al formato datetime
sp500_data.sort_values(by=['Symbol', 'Date'], inplace=True)  # Ordenar por símbolo y fecha
sp500_data['weekly_return'] = sp500_data.groupby('Symbol')['Adj Close'].pct_change()  # Calcular el retorno semanal

# Calcular la volatilidad (mediante la desviación estándar) de los retornos semanales para cada acción
sp500_volatility = sp500_data.groupby('Symbol')['weekly_return'].std()

sp500_risk_data = pd.DataFrame(sp500_volatility).reset_index()
sp500_risk_data.columns = ['Symbol', 'Volatility']

# Definir umbrales de volatilidad en función de los valores observados en ETFs y aplicar a las acciones del S&P 500
def assign_sp500_risk(volatility):
    if volatility > 0.05:
        return 5  # Muy volátil
    elif volatility > 0.025:
        return 4  # Moderadamente volátil
    else:
        return 4  # Riesgo mínimo de 4 para activos individuales no diversificados

# Asignar el `risk_rating` a las acciones del S&P 500 en función de su volatilidad
sp500_risk_data['Risk_Rating'] = sp500_risk_data['Volatility'].apply(assign_sp500_risk)

# Mostrar el resultado final
print("SP500 Risk Ratings Based on Volatility:\n", sp500_risk_data)

conteo_valores = sp500_risk_data['Risk_Rating'].value_counts()
conteo_especifico = conteo_valores.loc[[4, 5]]
print(conteo_especifico)

sp500_risk_data.to_csv('../cleandata/sp500riskrating.csv', index=False)