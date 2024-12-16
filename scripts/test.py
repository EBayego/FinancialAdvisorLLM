import pandas as pd

df = pd.read_csv('../cleandata/eu_etf_dataset_predict.csv')
df_filtrado = df[df['fund_type'] == 'bond'][['isin','fund_name','risk_rating', 'fund_type']]

print("iShares MSCI Taiwan UCITS ETF USD (Dist)".__contains__("Dist"))


data = {'Columna1': [1, 2, 3, 1],
        'Columna2': ['A', 'B', 'C', 'A'],
        'Columna3': [10, 20, 30, 10]}

# Convertimos el diccionario en un DataFrame
df = pd.DataFrame(data)
usuarios_procesados = set()

for _, usuario in df.iterrows():
    print("usuario :", usuario)
    # Convertir el perfil de usuario a un formato hashable para verificar duplicados
    usuario_hash = tuple(usuario.items())

    print("usuario_hash :", usuario_hash)
    if usuario_hash in usuarios_procesados:
        print("usuario procesados YA")
        continue

    # Marcar el usuario como procesado
    usuarios_procesados.add(usuario_hash)
    print("usuarios_procesados :", usuarios_procesados)

#df = pd.read_csv('../cleandata/users_dataset_full.csv')
print("DUPLICADOS: ", df.duplicated().any())