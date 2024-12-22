import json
import pandas as pd

def agrupar_datos(etfs, acciones, criptos):
    # Agrupar ETFs por nombre
    etfs_agrupados = etfs.groupby('fund_name').agg({
        'isin': 'first',
        'fund_trailing_return_5years': 'mean',
        'performance_rating': 'mean',
        'risk_rating': 'first'
    }).reset_index()

    # Agrupar acciones por símbolo
    acciones_agrupadas = acciones.groupby('Symbol').agg({
        'Volume': 'mean',
        'Adj Close': 'mean'
    }).reset_index()

    # Agrupar criptomonedas por nombre
    criptos_agrupados = criptos.groupby('crypto_name').agg({
        'close': 'mean',
        'volume': 'mean',
        'close_pct_change': 'mean',
        'risk_rating': 'first'
    }).reset_index()

    return etfs_agrupados, acciones_agrupadas, criptos_agrupados



def generar_recomendaciones(usuario, etfs, criptos, acciones, cuentas_ahorro):
    recomendaciones = []

    perfiles_riesgo = {
        1: "Muy Conservador",
        2: "Conservador",
        3: "Moderado",
        4: "Agresivo",
        5: "Muy Agresivo"
    }
    perfil_riesgo_texto = perfiles_riesgo.get(usuario['perfil_riesgo'])

    # Recomendación de cuentas de ahorro
    meses_ahorro = 6 if usuario['estabilidad_ingresos'] >= 3 else 3
    gasto_mensual_estimado = usuario['ingresos_mensuales'] - usuario['ahorro_mensual']
    ahorro_recomendado = gasto_mensual_estimado * meses_ahorro

    mejores_cuentas = cuentas_ahorro.sort_values(by='TAE', ascending=False).head(3)
    cuentas_recomendadas = [
        f"- {cuenta['bank']} - {cuenta['account_name']}: {cuenta['TAE']} TAE, saldo máximo remunerado {cuenta['max_remunerated_balance']}, comisiones {cuenta['commissions'].lower()}. {cuenta['details']}"
        for _, cuenta in mejores_cuentas.iterrows()
    ]
    if usuario['colchon_seguridad'] == 's':
        recomendaciones.append(
            f"Dado que ya cuentas con un colchón de seguridad, te recomiendo ingresarlo en una de las siguientes cuentas de ahorro:\n" +
            "\n".join(cuentas_recomendadas)
        )
    else:
        recomendaciones.append(
            f"Te recomiendo almacenar al menos {ahorro_recomendado:.2f} EUR, equivalentes a {meses_ahorro} meses de gastos mensuales, en una de las siguientes cuentas de ahorro:\n" +
            "\n".join(cuentas_recomendadas)
        )

    # Selección de ETFs
    etfs_filtrados = etfs[etfs['risk_rating'] <= usuario['perfil_riesgo']]
    if not etfs_filtrados.empty:
        mejor_etf = etfs_filtrados.sort_values(by=['fund_trailing_return_5years', 'performance_rating'], ascending=[False, False]).iloc[0]
        recomendaciones.append(
            f"Dado que tienes un perfil de riesgo {perfil_riesgo_texto} ({usuario['perfil_riesgo']}), te recomiendo invertir en el ETF '{mejor_etf['fund_name']}' con ISIN: '{mejor_etf['isin']}', "
            f"por su retorno promedio a 5 años de {mejor_etf['fund_trailing_return_5years']}% y su rating de rendimiento de {mejor_etf['performance_rating']}."
        )
        # ETFs adicionales
        mejores_etfs_adicionales = etfs_filtrados.iloc[1:5]  # 2 filas por si hay duplicados (no puede haber más de 2)
        procesados = set()
        resultado_adicionales = []

        for _, etf in mejores_etfs_adicionales.iterrows():
            if etf['isin'] in procesados:
                continue  # Ya procesado

            # Verificar si existe una versión del ETF que reparte o acumula dividendos
            etfs_similares = etfs_filtrados[
                (etfs_filtrados['fund_name'].str.contains(etf['fund_name'].split('UCITS')[0].strip(), case=False, na=False)) &
                (etfs_filtrados['isin'] != etf['isin'])
            ]

            if not etfs_similares.empty:
                similar = etfs_similares.iloc[0]  # Elegimos la primera coincidencia
                if etf['fund_trailing_return_5years'] >= similar['fund_trailing_return_5years']:
                    resultado_adicionales.append(
                        f"- {etf['fund_name']}: Retorno a 5 años de {etf['fund_trailing_return_5years']}%, con un rating de rendimiento de {etf['performance_rating']}. "
                        f"Además, tiene una versión que reparte dividendos, llamado {similar['fund_name']}, con un retorno a 5 años de {similar['fund_trailing_return_5years']}%, y un rating de rendimiento de {similar['performance_rating']}."
                    )
                else:
                    resultado_adicionales.append(
                        f"- {similar['fund_name']}: Retorno a 5 años de {similar['fund_trailing_return_5years']}%, con un rating de rendimiento de {similar['performance_rating']}. "
                        f"Además, tiene una versión de acumulación, que no reparte dividendos y reinvierte automáticamente tus ganancias, llamado {etf['fund_name']}, con un retorno a 5 años de {etf['fund_trailing_return_5years']}%, y un rating de rendimiento de {etf['performance_rating']}."
                    )
                procesados.add(similar['isin'])
            else:
                # Si no hay versiones similares, agregarlo directamente
                resultado_adicionales.append(
                    f"- {etf['fund_name']}: Retorno a 5 años de {etf['fund_trailing_return_5years']}%, con un rating de rendimiento de {etf['performance_rating']}."
                )

            procesados.add(etf['isin'])

        # Agregar las recomendaciones adicionales
        recomendaciones.append(
            "Además, estos otros ETFs también encajan muy bien con tu perfil:\n" + "\n".join(resultado_adicionales)
        )

    # Selección de acciones
    if not acciones.empty:
        mejor_accion = acciones.sort_values(by='Volume', ascending=False).iloc[0]
        recomendaciones.append(
            f"Si estás interesado en acciones, '{mejor_accion['Symbol']}' podría ser una buena opción. "
            f"Tiene un alto volumen de operaciones, de '{mejor_accion['Volume']}', lo que indica interés del mercado, pero recuerda que las acciones "
            f"pueden ser más volátiles que los ETFs."
        )
        mejores_acciones_adicionales = acciones.sort_values(by='Volume', ascending=False).iloc[1:3]
        recomendaciones.append(
            f"Además, estas otras acciones encajan bien con tu perfil:\n" +
			"\n".join(
				[f"- {accion['Symbol']}: Volumen reciente de {accion['Volume']}." for _, accion in mejores_acciones_adicionales.iterrows()]
			)
        )

    # Selección de criptomonedas
    criptos_filtrados = criptos[criptos['risk_rating'] <= usuario['perfil_riesgo']]
    if not criptos_filtrados.empty:
        mejor_cripto = criptos_filtrados.sort_values(by='close_pct_change', ascending=False).iloc[0]
        recomendaciones.append(
			f"Entre las criptomonedas, '{mejor_cripto['crypto_name']}' ha mostrado un rendimiento reciente "
			f"del {mejor_cripto['close_pct_change']}%. Sin embargo, recuerda que las criptomonedas son altamente volátiles "
			f"y conllevan un riesgo significativamente mayor que los ETFs o las acciones, incluso para perfiles de riesgo {perfil_riesgo_texto}."
		)
        mejores_criptos_adicionales = criptos_filtrados.sort_values(by='close_pct_change', ascending=False).iloc[1:3]
        recomendaciones.append(
            f"Además, estas otras criptomonedas encajan bien con tu perfil:\n" +
			"\n".join(
				[f"- {cripto['crypto_name']}: Cambio porcentual reciente de {cripto['close_pct_change']}%." for _, cripto in mejores_criptos_adicionales.iterrows()]
			)
        )

    return recomendaciones



def calcular_ratios_para_hash(datos_usuario):
    ascore = 0
    if datos_usuario['ingresos_mensuales'] > 0:
        ahorro_ratio = datos_usuario['ahorro_mensual'] / datos_usuario['ingresos_mensuales']
    else:
        ahorro_ratio = 0

    if ahorro_ratio > 0.3:
        ascore += 3
    elif ahorro_ratio > 0.2:
        ascore += 2
    elif ahorro_ratio > 0.1:
        ascore += 1

    dscore = 0
    if datos_usuario['deudas_mensuales'] > 0:
        dscore -= 1
    if datos_usuario['ingresos_mensuales'] > 0:
        deuda_ratio = datos_usuario['deudas_mensuales'] / datos_usuario['ingresos_mensuales']
    else:
        deuda_ratio = 0

    if deuda_ratio > 0.4:
        dscore -= 2
    elif deuda_ratio > 0.2:
        dscore -= 1

    return ascore, dscore



import pandas as pd
import json

def generar_dataset_sin_redundancia(users_data, etfs, criptos, acciones, cuentas_ahorro, output_path):
    rows = []
    usuarios_procesados = set()  # Para rastrear usuarios únicos basados en sus datos

    # Mensaje del sistema constante
    system_message = (
        "Eres un asistente financiero personal especializado en inversiones. "
        "Tu objetivo es ayudar a los usuarios a tomar decisiones financieras informadas. "
        "Primero, analiza el perfil del usuario y luego recomienda opciones de inversión precisas, claras y adaptadas a sus necesidades. "
        "Sé amable, profesional y enfocado únicamente en temas de inversión, finanzas y economía."
    )

    for _, usuario in users_data.iterrows():
        # Calcular ratios
        ascore, dscore = calcular_ratios_para_hash(usuario)
        usuario_modificado = usuario.copy()
        usuario_modificado['ahorro_ratio'] = ascore
        usuario_modificado['deuda_ratio'] = dscore
        usuario_modificado.drop(['ingresos_mensuales', 'ahorro_mensual', 'deudas_mensuales'], inplace=True)

        # Convertir el perfil de usuario modificado a un formato hashable
        usuario_hash = tuple(usuario_modificado.items())

        if usuario_hash in usuarios_procesados:
            continue  # Evitar duplicados

        # Marcar el usuario como procesado
        usuarios_procesados.add(usuario_hash)

        # Generar pregunta y respuesta
        user_profile = json.dumps({"user_profile": usuario.to_dict()}, ensure_ascii=False)
        recomendaciones = "\n".join(generar_recomendaciones(usuario, etfs, criptos, acciones, cuentas_ahorro))

        # Agregar en el formato deseado
        rows.append({
            "<|system|>": system_message,
            "<|user|>": user_profile,
            "<|assistant|>": recomendaciones
        })

    # Guardar el dataset en formato JSONL
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in rows:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Dataset reducido guardado en formato JSONL en {output_path}")
    return rows


# Cargar los datasets y agrupar
etf_data = pd.read_csv('../cleandata/eu_etf_dataset_predict.csv')
users_data = pd.read_csv('../cleandata/users_dataset_full.csv')
crypto_data = pd.read_csv('../cleandata/crypto/__combined_crypto_data.csv')
stocks_data = pd.read_csv('../cleandata/sp500Weekly.csv')
cuentas_ahorro = pd.read_csv('../cleandata/extraData/cuentas_ahorro.csv')

etfs_agrupados, acciones_agrupadas, criptos_agrupados = agrupar_datos(etf_data, stocks_data, crypto_data)

# Crear y guardar el dataset final
output_jsonl_path = "../cleandata/q&a/recomendaciones_iniciales.jsonl"
dataset_reducido = generar_dataset_sin_redundancia(users_data, etfs_agrupados, criptos_agrupados, acciones_agrupadas, cuentas_ahorro, output_jsonl_path)