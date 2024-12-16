import pandas as pd
import random
from collections import Counter
import json

def seleccionar_combinaciones_unicas(data, name_field, n_combinaciones=300, max_apariciones=3):
    combinaciones = []
    contador_apariciones = Counter()

    while len(combinaciones) < n_combinaciones:
        inv1, inv2 = random.sample(list(data[name_field]), 2)

        if (inv1, inv2) not in combinaciones and (inv2, inv1) not in combinaciones:
            if contador_apariciones[inv1] < max_apariciones and contador_apariciones[inv2] < max_apariciones:
                combinaciones.append((inv1, inv2))
                contador_apariciones[inv1] += 1
                contador_apariciones[inv2] += 1

    return combinaciones

def generar_pregunta(inversion1, inversion2):
    preguntas = [
        f"¿Qué diferencia hay entre {inversion1} y {inversion2}?",
        f"¿En qué se diferencian {inversion1} y {inversion2}?",
        f"¿Cuáles son las principales diferencias entre {inversion1} y {inversion2}?",
        f"¿Podrías explicar las diferencias entre {inversion1} y {inversion2}?",
        f"¿Cómo se comparan {inversion1} y {inversion2}?",
        f"¿En qué aspectos son diferentes {inversion1} y {inversion2}?",
        f"¿Qué diferencias relevantes existen entre {inversion1} y {inversion2}?"
    ]
    return random.choice(preguntas)

def generar_respuesta_conversacional_etfs(inversion1, inversion2, data1, data2):
    respuesta = f"Las diferencias entre '{inversion1}' y '{inversion2}' son las siguientes:\n"

    if data1['dividend_frequency'] != data2['dividend_frequency']:
        if data1['dividend_frequency'] == "Acc":
            respuesta += f"El ETF '{inversion1}' es de acumulación y reinvierte automáticamente los dividendos, mientras que '{inversion2}' distribuye dividendos {traducir_frecuencia_dividendos(data2['dividend_frequency'])}.\n"
        elif data2['dividend_frequency'] == "Acc":
            respuesta += f"El ETF '{inversion2}' es de acumulación y reinvierte automáticamente los dividendos, mientras que '{inversion1}' distribuye dividendos {traducir_frecuencia_dividendos(data1['dividend_frequency'])}.\n"
        else:
            respuesta += f"El ETF '{inversion1}' distribuye dividendos {traducir_frecuencia_dividendos(data1['dividend_frequency'])}, mientras que '{inversion2}' lo hace {traducir_frecuencia_dividendos(data2['dividend_frequency'])}.\n"

    if data1['risk_rating'] != data2['risk_rating']:
        respuesta += f"El nivel de riesgo varía: '{inversion1}' tiene un nivel de {data1['risk_rating']}, mientras que '{inversion2}' tiene un nivel de {data2['risk_rating']}.\n"

    if data1['performance_rating'] != data2['performance_rating']:
        respuesta += f"El rating de rendimiento es diferente: '{inversion1}' tiene un rating de {data1['performance_rating']}, mientras que '{inversion2}' tiene un rating de {data2['performance_rating']}.\n"

    if data1['fund_trailing_return_5years'] != data2['fund_trailing_return_5years']:
        respuesta += f"En cuanto al retorno a 5 años, '{inversion1}' ha generado un {data1['fund_trailing_return_5years']}%, mientras que '{inversion2}' ha generado un {data2['fund_trailing_return_5years']}%.\n"

    if data1['ongoing_cost'] != data2['ongoing_cost']:
        respuesta += f"Los costos en curso son distintos: '{inversion1}' tiene un costo de {data1['ongoing_cost']}%, mientras que '{inversion2}' tiene un costo de {data2['ongoing_cost']}%.\n"

    if data1['management_fees'] != data2['management_fees']:
        respuesta += f"Las comisiones de gestión varían: '{inversion1}' tiene comisiones de {data1['management_fees']}%, mientras que '{inversion2}' tiene {data2['management_fees']}%.\n"

    if data1['roe'] != data2['roe']:
        respuesta += f"El ROE (Return on Equity) también es diferente: '{inversion1}' tiene un ROE de {data1['roe']}%, mientras que '{inversion2}' tiene un ROE de {data2['roe']}%.\n"

    if data1['long_term_projected_earnings_growth'] != data2['long_term_projected_earnings_growth']:
        respuesta += f"El crecimiento proyectado a largo plazo difiere: '{inversion1}' tiene un crecimiento estimado de {data1['long_term_projected_earnings_growth']}%, mientras que '{inversion2}' tiene un {data2['long_term_projected_earnings_growth']}%.\n"

    if data1['historical_earnings_growth'] != data2['historical_earnings_growth']:
        respuesta += f"El crecimiento histórico de ganancias también varía: '{inversion1}' muestra un crecimiento histórico de {data1['historical_earnings_growth']}%, mientras que '{inversion2}' tiene un crecimiento de {data2['historical_earnings_growth']}%.\n"

    return respuesta

def traducir_frecuencia_dividendos(valor):
    if valor == "Acc":
        return "acumulados"
    elif valor == "Annually":
        return "anualmente"
    elif valor == "Quarterly":
        return "trimestralmente"
    else:
        return "mensualmente"
    
def generar_respuesta_conversacional_stocks(inversion1, inversion2, data1, data2):
    respuesta = f"Las diferencias entre las acciones '{inversion1}' y '{inversion2}' son las siguientes:\n"

    if data1['Adj Close'] != data2['Adj Close']:
        respuesta += f"El precio actual es diferente: '{inversion1}' tiene un precio de {data1['Adj Close']} USD, mientras que '{inversion2}' tiene un precio de {data2['Adj Close']} USD.\n"

    if data1['Volume'] != data2['Volume']:
        respuesta += f"El volumen de operaciones varía: '{inversion1}' tiene un volumen de {data1['Volume']}, mientras que '{inversion2}' tiene un volumen de {data2['Volume']}.\n"

    return respuesta

def generar_respuesta_conversacional_cryptos(inversion1, inversion2, data1, data2):
    respuesta = f"Las diferencias entre las criptomonedas '{inversion1}' y '{inversion2}' son las siguientes:\n"

    if data1['close_pct_change'] != data2['close_pct_change']:
        respuesta += f"El cambio porcentual reciente es diferente: '{inversion1}' tuvo un cambio de {data1['close_pct_change']}%, mientras que '{inversion2}' tuvo un cambio de {data2['close_pct_change']}%.\n"

    if data1['volume'] != data2['volume']:
        respuesta += f"El volumen de transacciones también varía: '{inversion1}' tiene un volumen de {data1['volume']}, mientras que '{inversion2}' tiene un volumen de {data2['volume']}.\n"

    return respuesta    

def generar_dataset_conversacional(data, name_field, comparar_funcion, n_combinaciones=300, max_apariciones=3):
    combinaciones = seleccionar_combinaciones_unicas(data, name_field, n_combinaciones, max_apariciones)
    preguntas_respuestas = []

    for inv1, inv2 in combinaciones:
        data1 = data[data[name_field] == inv1].iloc[0]
        data2 = data[data[name_field] == inv2].iloc[0]
        pregunta = generar_pregunta(inv1, inv2)
        respuesta = comparar_funcion(inv1, inv2, data1, data2)
        preguntas_respuestas.append({"pregunta": pregunta, "respuesta": respuesta})

    return pd.DataFrame(preguntas_respuestas)

etf_data = pd.read_csv('../cleandata/eu_etf_dataset_predict.csv')
crypto_data = pd.read_csv('../cleandata/crypto/__combined_crypto_data.csv')
stocks_data = pd.read_csv('../cleandata/sp500Weekly.csv')

dataset_etfs = generar_dataset_conversacional(etf_data, 'fund_name', generar_respuesta_conversacional_etfs)
dataset_stocks = generar_dataset_conversacional(stocks_data, 'Symbol', generar_respuesta_conversacional_stocks)
dataset_cryptos = generar_dataset_conversacional(crypto_data, 'crypto_name', generar_respuesta_conversacional_cryptos)

def combinar_datasets(etf_data, stock_data, crypto_data):
    dataset_combinado = []

    # Procesar ETFs
    for _, row in etf_data.iterrows():
        dataset_combinado.append({
            "tipo_activo": "ETF",
            "pregunta": row["pregunta"],
            "respuesta": row["respuesta"]
        })

    # Procesar acciones
    for _, row in stock_data.iterrows():
        dataset_combinado.append({
            "tipo_activo": "Acción",
            "pregunta": row["pregunta"],
            "respuesta": row["respuesta"]
        })

    # Procesar criptomonedas
    for _, row in crypto_data.iterrows():
        dataset_combinado.append({
            "tipo_activo": "Criptomoneda",
            "pregunta": row["pregunta"],
            "respuesta": row["respuesta"]
        })

    return dataset_combinado

# Guardar como JSONL
def guardar_jsonl(dataset, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# Combinar y guardar
dataset_combinado = combinar_datasets(dataset_etfs, dataset_stocks, dataset_cryptos)
guardar_jsonl(dataset_combinado, "../cleandata/q&a/q&a_comparaciones_conversacionales.jsonl")

print("Dataset combinado generado y guardado.")