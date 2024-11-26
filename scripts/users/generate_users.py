import pandas as pd
import numpy as np

np.random.seed(42)

n_users = 2000 

def generar_gastos(ingresos):
    # Genera gastos basado en ingresos, considerando los gastos esenciales
    gastos_esenciales = np.random.choice(
        np.append(
            np.random.uniform(500, 1500, int(len(ingresos) * 0.7)),  # Mayoría de casos entre 500 y 1500
            np.append(
                np.zeros(int(len(ingresos) * 0.2)),  # Algunos casos con 0 gastos
                np.random.uniform(1500, 2500, int(len(ingresos) * 0.1))  # Pocos casos entre 1500 y 2500
            )
        ), len(ingresos)
    )
    # Asegurarse de que el ahorro no sea negativo y esté entre al menos 100 y los ingresos totales
    ahorro = np.clip(ingresos - gastos_esenciales, 100, ingresos)
    return ahorro

ingresos = np.random.choice(
    np.append(np.random.uniform(800, 3000, int(n_users * 0.9)), 
              np.random.uniform(3000, 8000, int(n_users * 0.1))), n_users)

ahorro = generar_gastos(ingresos)

data = {
    'edad': np.random.randint(18, 70, n_users),  # Edad entre 18 y 70 años
    'ingresos_mensuales': ingresos,
    'ahorro_mensual': ahorro,
    'deudas_mensuales': np.random.choice(
        np.append(np.zeros(int(n_users * 0.7)),  # 70% sin deudas
                  np.random.uniform(200, 1500, int(n_users * 0.3))),  # 30% con deudas de tipo hipoteca, etc.
        n_users
    ),
    'horizonte_inversion': np.random.choice(['corto plazo', 'medio plazo', 'largo plazo'], n_users),
    'objetivo_financiero': np.random.choice([1, 2, 3], n_users),  # Objetivo financiero (1, 2, o 3)
    'tolerancia_riesgo': np.random.choice([1, 2, 3], n_users),  # Tolerancia al riesgo (1, 2, o 3)
    'estabilidad_ingresos': np.random.choice([1, 2, 3], n_users),  # Estabilidad de ingresos (1, 2, o 3)
    'conocimiento_inversiones': np.random.choice([1, 2, 3, 4], n_users),  # Nivel de conocimientos (1 a 4)
    'colchon_seguridad': np.random.choice(['s', 'n'], n_users)  # Colchón de seguridad (s/n)
}

df_usuarios = pd.DataFrame(data)
df_usuarios.to_csv('../data/users_dataset.csv', index=False)