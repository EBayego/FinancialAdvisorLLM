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

model = RandomForestClassifier(
    random_state=42,
    max_depth=7,                # Evita que los árboles sean demasiado profundos, reduciendo el riesgo de sobreajuste y mejorando la generalización.
    min_samples_split=10,       # Especifica el número mínimo de muestras requeridas para dividir un nodo. Un valor más alto fuerza a los árboles a ser menos complejos, ayudando a prevenir el sobreajuste.
    min_samples_leaf=5,         # Define el número mínimo de muestras necesarias en una hoja. Asegura que las hojas no sean demasiado pequeñas, ayudando a suavizar el modelo y mejora su capacidad de generalización.
    n_estimators=150,           # Determina el número de árboles en el bosque. Más árboles generalmente mejoran la precisión, pero aumentan el tiempo de entrenamiento y predicción.
    max_features='sqrt',        # Controla el número de características consideradas en cada división. Al usar la raíz cuadrada del número total de características, se introduce aleatoriedad en los árboles, reduciendo la correlación entre ellos y mejorando la robustez del modelo.
    class_weight='balanced'     # Ajusta automáticamente los pesos de las clases según su frecuencia en los datos. Es útil para manejar desequilibrios en las clases, asegurando que las menos frecuentes sean consideradas en el entrenamiento.
)
model.fit(X_train, y_train)

# Evaluar el modelo en el conjunto de prueba
y_test_pred = model.predict(X_test)
print("=== Métricas del conjunto de prueba ===")
print(classification_report(y_test, y_test_pred))
print(f"Precisión del modelo en prueba: {accuracy_score(y_test, y_test_pred):.2f}")

# Evaluar el modelo en el conjunto de entrenamiento
y_train_pred = model.predict(X_train)
print("=== Métricas del conjunto de entrenamiento ===")
print(classification_report(y_train, y_train_pred))
print(f"Precisión del modelo en entrenamiento: {accuracy_score(y_train, y_train_pred):.2f}")

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