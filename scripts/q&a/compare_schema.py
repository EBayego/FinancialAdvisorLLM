import pandas as pd
import random
from collections import Counter
import json

def comparar_etfs(etf1, etf2):
    explicacion = f"Comparación entre ETFs '{etf1['fund_name']}' y '{etf2['fund_name']}':\n"
    
    # ISIN
    explicacion += f"- **ISIN**: '{etf1['isin']}' vs '{etf2['isin']}'. El ISIN es un identificador único para cada ETF.\n"
    
    # Tipo de fondo
    explicacion += f"- **Tipo de fondo**: '{etf1['fund_type']}' vs '{etf2['fund_type']}'. "
    explicacion += f"Esto indica el enfoque del fondo, ya sea a renta variable (equity) o renta fija (bond).\n"
    
    # Reparto de dividendos
    explicacion += f"- **Reparto de dividendos**: '{etf1['dividend_frequency']}' vs '{etf2['dividend_frequency']}'. "
    for etf, fund_name in zip([etf1, etf2], [etf1['fund_name'], etf2['fund_name']]):
        if etf['dividend_frequency'] == 'Acc':
            explicacion += f"El ETF '{fund_name}' es de acumulación, no reparte los dividendos sino que los reinvierte automáticamente.\n"
        elif etf['dividend_frequency'] == 'Annually':
            explicacion += f"El ETF '{fund_name}' distribuye dividendos anualmente.\n"
        elif etf['dividend_frequency'] == 'Quarterly':
            explicacion += f"El ETF '{fund_name}' distribuye dividendos trimestralmente.\n"
        else:
            explicacion += f"El ETF '{fund_name}' distribuye dividendos mensualmente.\n"

    # Rating de riesgo
    explicacion += f"- **Nivel de riesgo**: '{etf1['risk_rating']}' vs '{etf2['risk_rating']}'. "
    if etf1['risk_rating'] < etf2['risk_rating']:
        explicacion += f"Un menor nivel de riesgo para '{etf1['fund_name']}' indica mayor estabilidad y menor volatilidad.\n"
    else:
        explicacion += f"Un menor nivel de riesgo para '{etf2['fund_name']}' indica mayor estabilidad y menor volatilidad.\n"

    # Rating de rendimiento
    explicacion += f"- **Rating de rendimiento**: '{etf1['performance_rating']}' vs '{etf2['performance_rating']}'. "
    if etf1['performance_rating'] > etf2['performance_rating']:
        explicacion += f"Un rating más alto refleja una gestión eficiente en '{etf1['fund_name']}'.\n"
    else:
        explicacion += f"Un rating más alto refleja una gestión eficiente en '{etf2['fund_name']}'.\n"

    # ROE
    explicacion += f"- **ROE (Return on Equity)**: '{etf1['roe']}%' vs '{etf2['roe']}%'. "
    if etf1['roe'] > etf2['roe']:
        explicacion += f"Un mayor ROE en '{etf1['fund_name']}' indica mayor rentabilidad en relación al capital propio.\n"
    else:
        explicacion += f"Un mayor ROE en '{etf2['fund_name']}' indica mayor rentabilidad en relación al capital propio.\n"

    # Costos en curso
    explicacion += f"- **Costos del fondo**: '{etf1['ongoing_cost']}%' vs '{etf2['ongoing_cost']}%'. "
    if etf1['ongoing_cost'] < etf2['ongoing_cost']:
        explicacion += f"'{etf1['fund_name']}' tiene costos más bajos, lo cual puede impactar positivamente en el rendimiento neto.\n"
    else:
        explicacion += f"'{etf2['fund_name']}' tiene costos más bajos, lo cual puede impactar positivamente en el rendimiento neto.\n"

    # Comisiones de gestión
    explicacion += f"- **Comisiones de gestión**: '{etf1['management_fees']}%' vs '{etf2['management_fees']}%'. "
    if etf1['management_fees'] < etf2['management_fees']:
        explicacion += f"'{etf1['fund_name']}' tiene comisiones más bajas, reduciendo los costos para el inversor.\n"
    else:
        explicacion += f"'{etf2['fund_name']}' tiene comisiones más bajas, reduciendo los costos para el inversor.\n"

    # Retorno a 5 años
    explicacion += f"- **Retorno a 5 años**: '{etf1['fund_trailing_return_5years']}%' vs '{etf2['fund_trailing_return_5years']}%'. "
    if etf1['fund_trailing_return_5years'] > etf2['fund_trailing_return_5years']:
        explicacion += f"'{etf1['fund_name']}' ha demostrado mayor rentabilidad histórica a largo plazo.\n"
    else:
        explicacion += f"'{etf2['fund_name']}' ha demostrado mayor rentabilidad histórica a largo plazo.\n"

    # Crecimiento proyectado a largo plazo
    explicacion += f"- **Crecimiento proyectado a largo plazo**: '{etf1['long_term_projected_earnings_growth']}%' vs '{etf2['long_term_projected_earnings_growth']}%'. "
    if etf1['long_term_projected_earnings_growth'] > etf2['long_term_projected_earnings_growth']:
        explicacion += f"'{etf1['fund_name']}' tiene un potencial de crecimiento superior.\n"
    else:
        explicacion += f"'{etf2['fund_name']}' tiene un potencial de crecimiento superior.\n"

    # Crecimiento histórico de ganancias
    explicacion += f"- **Crecimiento histórico de ganancias**: '{etf1['historical_earnings_growth']}%' vs '{etf2['historical_earnings_growth']}%'. "
    if etf1['historical_earnings_growth'] > etf2['historical_earnings_growth']:
        explicacion += f"'{etf1['fund_name']}' muestra un historial de crecimiento más sólido.\n"
    else:
        explicacion += f"'{etf2['fund_name']}' muestra un historial de crecimiento más sólido.\n"

    return explicacion

def comparar_acciones(accion1, accion2):
    explicacion = f"Comparación entre acciones '{accion1['Symbol']}' y '{accion2['Symbol']}':\n"

    # Precio actual
    explicacion += f"- **Precio actual**: '{accion1['Symbol']}' tiene un precio de {accion1['Adj Close']} $, mientras que '{accion2['Symbol']}' tiene {accion2['Adj Close']} $.\n"

    # Volumen
    explicacion += f"- **Volumen de operaciones**: '{accion1['Symbol']}' tiene un volumen de {accion1['Volume']}, mientras que '{accion2['Symbol']}' tiene {accion2['Volume']}. "
    if accion1['Volume'] > accion2['Volume']:
        explicacion += f"Un mayor volumen indica un interés de mercado más alto para '{accion1['Symbol']}'.\n"
    else:
        explicacion += f"Un mayor volumen indica un interés de mercado más alto para '{accion2['Symbol']}'.\n"

    return explicacion

def comparar_criptomonedas(cripto1, cripto2):
    explicacion = f"Comparación entre criptomonedas '{cripto1['crypto_name']}' y '{cripto2['crypto_name']}':\n"

    # Cambio porcentual reciente
    explicacion += f"- **Cambio porcentual reciente**: '{cripto1['crypto_name']}' tuvo un cambio de {cripto1['close_pct_change']}%, mientras que '{cripto2['crypto_name']}' tuvo {cripto2['close_pct_change']}%.\n"

    # Volumen
    explicacion += f"- **Volumen de transacciones**: '{cripto1['crypto_name']}' tiene un volumen de {cripto1['volume']}, mientras que '{cripto2['crypto_name']}' tiene {cripto2['volume']}.\n"

    return explicacion

def seleccionar_combinaciones_unicas(data, name_field, n_combinaciones=150, max_apariciones=3):
    combinaciones = []
    contador_apariciones = Counter()

    while len(combinaciones) < n_combinaciones:
        # Seleccionar dos elementos aleatorios
        inv1, inv2 = random.sample(list(data[name_field]), 2)

        # Verificar que la combinación no exista y que no exceda el límite de apariciones
        if (inv1, inv2) not in combinaciones and (inv2, inv1) not in combinaciones:
            if contador_apariciones[inv1] < max_apariciones and contador_apariciones[inv2] < max_apariciones:
                combinaciones.append((inv1, inv2))
                contador_apariciones[inv1] += 1
                contador_apariciones[inv2] += 1

    return combinaciones

def generar_comparaciones(data, name_field, comparar_funcion, tipo, n_combinaciones=150):
    combinaciones = seleccionar_combinaciones_unicas(data, name_field, n_combinaciones)
    comparaciones = []

    for inv1, inv2 in combinaciones:
        data1 = data[data[name_field] == inv1].iloc[0]
        data2 = data[data[name_field] == inv2].iloc[0]
        comparacion = comparar_funcion(data1, data2)
        comparaciones.append({"inversion1": inv1, "inversion2": inv2, "tipo": tipo, "explicacion": comparacion})

    return pd.DataFrame(comparaciones)

# Cargar datasets
etf_data = pd.read_csv('../cleandata/eu_etf_dataset_predict.csv')
crypto_data = pd.read_csv('../cleandata/crypto/__combined_crypto_data.csv')
stocks_data = pd.read_csv('../cleandata/sp500Weekly.csv')

# Generar comparaciones
comparaciones_etfs = generar_comparaciones(etf_data, 'fund_name', comparar_etfs, 'ETF')
comparaciones_crypto = generar_comparaciones(crypto_data, 'crypto_name', comparar_criptomonedas, 'Criptomoneda')
comparaciones_stocks = generar_comparaciones(stocks_data, 'Symbol', comparar_acciones, 'Acción')

def generar_pregunta(inversion1, inversion2):
    plantillas = [
        f"¿Qué diferencia hay entre {inversion1} y {inversion2}?",
        f"¿En qué se diferencian {inversion1} y {inversion2}?",
        f"¿Cómo compararías {inversion1} y {inversion2}?",
        f"¿Podrías explicar las diferencias entre {inversion1} y {inversion2}?",
        f"¿Cuáles son las principales diferencias entre {inversion1} y {inversion2}?",
        f"¿Qué diferencias relevantes existen entre {inversion1} y {inversion2}?",
        f"¿En qué aspectos son diferentes {inversion1} y {inversion2}?"
    ]
    return random.choice(plantillas)

def combinar_comparaciones_jsonl(etf_data, stock_data, crypto_data, output_path):
    dataset_combinado = []

    # Procesar ETFs
    for _, row in etf_data.iterrows():
        pregunta = generar_pregunta(row["inversion1"], row["inversion2"])
        dataset_combinado.append({
            "tipo_activo": "ETF",
            "pregunta": pregunta,
            "respuesta": row["explicacion"]
        })

    # Procesar acciones
    for _, row in stock_data.iterrows():
        pregunta = generar_pregunta(row["inversion1"], row["inversion2"])
        dataset_combinado.append({
            "tipo_activo": "Acción",
            "pregunta": pregunta,
            "respuesta": row["explicacion"]
        })

    # Procesar criptomonedas
    for _, row in crypto_data.iterrows():
        pregunta = generar_pregunta(row["inversion1"], row["inversion2"])
        dataset_combinado.append({
            "tipo_activo": "Criptomoneda",
            "pregunta": pregunta,
            "respuesta": row["explicacion"]
        })

    # Guardar como JSONL
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in dataset_combinado:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# Combinar y guardar
output_jsonl_path = '../cleandata/q&a/q&a_comparaciones_esquematico.jsonl'
combinar_comparaciones_jsonl(comparaciones_etfs, comparaciones_stocks, comparaciones_crypto, output_jsonl_path)

print(f"Dataset combinado generado y guardado como '{output_jsonl_path}'.")