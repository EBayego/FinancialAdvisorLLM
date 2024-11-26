import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib  # Para guardar el modelo

dataset_path = "../cleandata/users_dataset_full.csv"
df = pd.read_csv(dataset_path)

categorical_columns = ['horizonte_inversion', 'colchon_seguridad']
label_encoders = {}

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Guardar los encoders para usarlos en nuevas predicciones

# Separar características y etiquetas
X = df.drop(columns=['perfil_riesgo'])
y = df['perfil_riesgo']

# Escalar los datos numéricos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
print("Reporte de Clasificación:")
print(classification_report(y_test, y_pred))
print(f"Precisión del modelo: {accuracy_score(y_test, y_pred):.2f}")

# Guardar el modelo y los preprocesadores
joblib.dump(model, "../models/user_risk_rating/modelo_perfil_riesgo.pkl")
joblib.dump(scaler, "../models/user_risk_rating/scaler.pkl")
joblib.dump(label_encoders, "../models/user_risk_rating/label_encoders.pkl")
print("Modelo y preprocesadores guardados.")

# Uso del modelo para nuevas predicciones
def predecir_perfil_riesgo(nuevos_datos):
    # Nuevos datos deben ser un DataFrame con las mismas columnas que X
    for col, le in label_encoders.items():
        nuevos_datos[col] = le.transform(nuevos_datos[col])
    nuevos_datos_scaled = scaler.transform(nuevos_datos)
    return model.predict(nuevos_datos_scaled)