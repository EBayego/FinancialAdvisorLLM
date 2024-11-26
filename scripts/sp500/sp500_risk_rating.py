import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

sp500_data = pd.read_csv('../cleandata/sp500Weekly.csv')
etf_data  = pd.read_csv('../cleandata/eu_etf_dataset_predict.csv')

etf_features = etf_data[['fund_type', 'performance_rating', 'roe', 'fund_trailing_return_ytd',
                         'long_term_projected_earnings_growth', 'historical_earnings_growth', 'risk_rating']].dropna()

# Convertir 'fund_type' en variables dummy por ser categórico
etf_features_encoded = pd.get_dummies(etf_features, columns=['fund_type'])

# Separar variables predictoras y variable objetivo
X_etf = etf_features_encoded.drop('risk_rating', axis=1)
y_etf = etf_features_encoded['risk_rating'].astype('int')

# Dividir datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_etf, y_etf, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print("Model Accuracy:", accuracy)
print("Classification Report:\n", report)

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