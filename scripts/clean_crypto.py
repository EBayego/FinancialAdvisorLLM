import os
import pandas as pd

data_folder = '../data/crypto W1'
output_folder = '../cleandata/crypto'

csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

crypto_data = {}
combined_data = []

for file_name in csv_files:
    crypto_name = file_name.replace('.csv', '').replace("_W1", "")  # Nombre de la criptomoneda segun el nombre del archivo
    file_path = os.path.join(data_folder, file_name)
    
    df = pd.read_csv(file_path)
    
    df = df[['datetime', 'close', 'volume']]
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Guardar datos mensuales en vez de semanales
    df = df.iloc[::4, :].reset_index(drop=True)

    # Calcular el cambio porcentual semanal en el precio de cierre
    df['close_pct_change'] = df['close'].pct_change() * 100

    df['crypto_name'] = crypto_name
    df = df.reindex(columns=['crypto_name'] + list(df.columns[:-1]))
    crypto_data[crypto_name] = df
    
    # Añadir el perfil de riesgo a todas las criptomonedas
    df['risk_rating'] = 5
    combined_data.append(df)

# Crear un único dataset combinado, eliminando los datos nulos, los cuales son del campo close_pct_change que si empieza el mes, no tiene datos y por lo tanto es un campo vacio
combined_df = pd.concat(combined_data, ignore_index=True).dropna()

print(combined_df.isnull().sum())

combined_df.to_csv(os.path.join(output_folder, '__combined_crypto_data.csv'), index=False)

# Opcional: Guardar los datos individuales procesados en archivos CSV separados
#for crypto_name, df in crypto_data.items():
#    df.to_csv(os.path.join(output_folder, f'{crypto_name}_processed.csv'), index=False)

print("Procesamiento completado. Archivos guardados en la carpeta de salida.")