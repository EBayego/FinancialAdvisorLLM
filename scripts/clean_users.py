import pandas as pd
from user_risk_rating import calcular_perfil_riesgo 

df = pd.read_csv("../data/users_dataset.csv")

def calcular_riesgo_para_fila(fila):
    datos_usuario = {
        'edad': fila['edad'],
        'ingresos_mensuales': fila['ingresos_mensuales'],
        'ahorro_mensual': fila['ahorro_mensual'],
        'deudas_mensuales': fila['deudas_mensuales'],
        'horizonte_inversion': fila['horizonte_inversion'],
        'objetivo_financiero': fila['objetivo_financiero'],
        'tolerancia_riesgo': fila['tolerancia_riesgo'],
        'estabilidad_ingresos': fila['estabilidad_ingresos'],
        'conocimiento_inversiones': fila['conocimiento_inversiones'],
        'colchon_seguridad': fila['colchon_seguridad']
    }
    return calcular_perfil_riesgo(datos_usuario)

df['perfil_riesgo'] = df.apply(calcular_riesgo_para_fila, axis=1)

# Analizar los resultados
resumen_perfiles = df['perfil_riesgo'].value_counts().sort_index()
total_casos = len(df)

# Calcular el porcentaje para cada perfil de riesgo
resumen_perfiles_porcentaje = (resumen_perfiles / total_casos * 100).round(2)

# Mostrar estadísticas
print("Cantidad de usuarios en cada perfil de riesgo:")
print(resumen_perfiles)
print("\nPorcentaje de usuarios en cada perfil de riesgo:")
print(resumen_perfiles_porcentaje)

df.to_csv("../cleandata/users_dataset_full.csv", index=False)
print(f"\nArchivo con los perfiles de riesgo guardado")