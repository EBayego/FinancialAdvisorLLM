import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

df = pd.read_csv('../cleandata/eu_etf_dataset_cleaned.csv')

# Selecciona las columnas predictoras
delt = ['isin', 'fund_name', 'category', 'investment_strategy', 'asset_stock', 'asset_bond', 'nav_per_share_currency', 'nav_per_share', 'latest_nav_date', 'fund_trailing_return_10years']

print(df.shape[0])
print(df.isnull().sum())

# Identificar columnas en las que no permitiremos nulos
columns_without_nans = [col for col in df.columns if col not in (delt + ['risk_rating', 'performance_rating'])]
print(columns_without_nans)
df_original = df.dropna(subset=columns_without_nans)

data_cleaned = df_original.drop(delt, axis=1)
print("quitando columnas: \n")
print(data_cleaned.shape[0])
print(data_cleaned.isnull().sum())

categorical_cols = ['fund_type', 'dividend_frequency']
data_cleaned = pd.get_dummies(data_cleaned, columns=categorical_cols, drop_first=True)

# Codificación de frecuencia para 'country_exposure', dado que es un valor categórico con muchos valores distintos
country_frequency = data_cleaned['country_exposure'].value_counts(normalize=True)
data_cleaned['country_exposure_freq'] = data_cleaned['country_exposure'].map(country_frequency)
data_cleaned = data_cleaned.drop('country_exposure', axis=1)

known_risk_data = data_cleaned[data_cleaned['risk_rating'].notnull()]
unknown_risk_data = data_cleaned[data_cleaned['risk_rating'].isnull()]

# Variables predictoras (features) y objetivo (target)
X_risk = known_risk_data.drop(['risk_rating', 'performance_rating'], axis=1)
y_risk = known_risk_data['risk_rating']
X_predict_risk = unknown_risk_data.drop(['risk_rating', 'performance_rating'], axis=1)

# Separar datos de entrenamiento y prueba
X_train_risk, X_test_risk, y_train_risk, y_test_risk = train_test_split(X_risk, y_risk, test_size=0.2, random_state=42)

# Entrenar el modelo
risk_model = RandomForestRegressor(random_state=42)
risk_model.fit(X_train_risk, y_train_risk)

def round_to_valid_rating(predictions):
    valid_ratings = [1.0, 2.0, 3.0, 4.0, 5.0]
    return [min(valid_ratings, key=lambda x: abs(x - pred)) for pred in predictions]

# Predicción de valores faltantes en 'risk_rating'
predicted_risk = round_to_valid_rating(risk_model.predict(X_predict_risk))
data_cleaned.loc[data_cleaned['risk_rating'].isnull(), 'risk_rating'] = predicted_risk

# Repetir el proceso para 'performance_rating'
known_performance_data = data_cleaned[data_cleaned['performance_rating'].notnull()]
unknown_performance_data = data_cleaned[data_cleaned['performance_rating'].isnull()]

X_performance = known_performance_data.drop(['risk_rating', 'performance_rating'], axis=1)
y_performance = known_performance_data['performance_rating']
X_predict_performance = unknown_performance_data.drop(['risk_rating', 'performance_rating'], axis=1)

X_train_performance, X_test_performance, y_train_performance, y_test_performance = train_test_split(X_performance, y_performance, test_size=0.2, random_state=42)

performance_model = RandomForestRegressor(random_state=42)
performance_model.fit(X_train_performance, y_train_performance)

predicted_performance = round_to_valid_rating(performance_model.predict(X_predict_performance))
data_cleaned.loc[data_cleaned['performance_rating'].isnull(), 'performance_rating'] = predicted_performance

# Ahora 'data_cleaned' tiene valores estimados en 'risk_rating' y 'performance_rating'
print(data_cleaned.head())
print(data_cleaned.isnull().sum())

# Función para calcular y mostrar las métricas
def print_metrics(y_true, y_pred, label):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    print(f"--- Métricas para {label} ---")
    print(f"MAE (Error Absoluto Medio): {mae:.4f}")
    print(f"MSE (Error Cuadrático Medio): {mse:.4f}")
    print(f"RMSE (Raíz del Error Cuadrático Medio): {rmse:.4f}")
    print(f"R² (Coeficiente de Determinación): {r2:.4f}")
    print()

# Calcular métricas para el modelo de 'risk_rating' en el conjunto de entrenamiento
y_train_pred_risk = risk_model.predict(X_train_risk)
print_metrics(y_train_risk, y_train_pred_risk, "Risk Rating (Entrenamiento)")

# Calcular métricas para el modelo de 'performance_rating' en el conjunto de entrenamiento
y_train_pred_performance = performance_model.predict(X_train_performance)
print_metrics(y_train_performance, y_train_pred_performance, "Performance Rating (Entrenamiento)")

# Calcular métricas para el modelo de 'risk_rating'
y_pred_risk = risk_model.predict(X_test_risk)
print_metrics(y_test_risk, y_pred_risk, "Risk Rating")

# Calcular métricas para el modelo de 'performance_rating'
y_pred_performance = performance_model.predict(X_test_performance)
print_metrics(y_test_performance, y_pred_performance, "Performance Rating")

print("df_ORIGNAIL")
print(df_original.shape[0])
print(df_original.isnull().sum())

df_original.loc[df_original.index, 'risk_rating'] = data_cleaned['risk_rating']
df_original.loc[df_original.index, 'performance_rating'] = data_cleaned['performance_rating']

# Verifica que ya no hay nulos en 'risk_rating' y 'performance_rating' en el dataset completo
print("Valores nulos después de incorporar predicciones:")
print(df_original[['risk_rating', 'performance_rating']].isnull().sum())

print("df_ORIGNAIL")
print(df_original.shape[0])
print(df_original.isnull().sum())

##
# VALORES PREDECIDOS INTEGRADOS AL DATASET ORIGINAL
##
df_original.to_csv('../cleandata/eu_etf_dataset_predict.csv', index=False)