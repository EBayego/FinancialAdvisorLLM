def obtener_datos_usuario():
    print("Por favor, proporciona la siguiente información:")
    
    edad = int(input("Edad: "))
    ingresos_mensuales = float(input("Ingresos mensuales (en EUR): "))
    ahorro_mensual = float(input("Ahorro mensual neto (en EUR): "))
    deudas_mensuales = float(input("Deudas mensuales (en EUR): "))
    
    horizonte_inversion = input("Horizonte de inversión (corto/medio/largo plazo): ").lower()
    
    print("Objetivos financieros: ")
    print("1. Preservación de capital")
    print("2. Generación de ingresos pasivos")
    print("3. Crecimiento del capital")
    objetivo_financiero = int(input("Selecciona una opción (1, 2 o 3): "))
    
    print("¿Cómo describirías tu tolerancia al riesgo?")
    print("1. Me estreso fácilmente con pérdidas pequeñas.")
    print("2. Puedo tolerar fluctuaciones moderadas.")
    print("3. Me siento cómodo asumiendo riesgos grandes.")
    tolerancia_riesgo = int(input("Selecciona una opción (1, 2 o 3): "))
    
    print("¿Cómo describirías tus ingresos?")
    print("1. Muy estables (empleo fijo o ingresos garantizados)")
    print("2. Moderadamente estables (freelance o ingresos variables bajos)")
    print("3. Altamente variables (empresario o ingresos inestables)")
    estabilidad_ingresos = int(input("Selecciona una opción (1, 2 o 3): "))
    
    print("¿Cuál es tu nivel de conocimiento sobre inversiones y mercados financieros?")
    print("1. No tengo conocimientos.")
    print("2. Tengo conocimientos básicos.")
    print("3. Estoy familiarizado y tengo algo de experiencia.")
    print("4. Tengo conocimientos avanzados y experiencia.")
    conocimiento_inversiones = int(input("Selecciona una opción (1, 2, 3 o 4): "))

    colchon_seguridad = input("¿Tienes un colchón de seguridad equivalente a al menos 3-6 meses de gastos? (s/n): ").lower()
    
    return {
        'edad': edad,
        'ingresos_mensuales': ingresos_mensuales,
        'ahorro_mensual': ahorro_mensual,
        'deudas_mensuales': deudas_mensuales,
        'horizonte_inversion': horizonte_inversion,
        'objetivo_financiero': objetivo_financiero,
        'tolerancia_riesgo': tolerancia_riesgo,
        'estabilidad_ingresos': estabilidad_ingresos,
        'conocimiento_inversiones': conocimiento_inversiones,
        'colchon_seguridad': colchon_seguridad
    }

def calcular_perfil_riesgo(datos_usuario):
    score = 0
    
    if datos_usuario['edad'] < 35:
        score += 3
    elif datos_usuario['edad'] < 55:
        score += 2
    else:
        score += 1

    # Ratio de ahorro
    ahorro_ratio = datos_usuario['ahorro_mensual'] / datos_usuario['ingresos_mensuales']
    if ahorro_ratio > 0.3:
        score += 3
    elif ahorro_ratio > 0.2:
        score += 2
    elif ahorro_ratio > 0.1:
        score += 1

    # Nivel de endeudamiento
    if datos_usuario['deudas_mensuales'] > 0:
        score -=1
    deuda_ratio = datos_usuario['deudas_mensuales'] / datos_usuario['ingresos_mensuales']
    if deuda_ratio > 0.4:
        score -= 2
    elif deuda_ratio > 0.2:
        score -= 1
    
    if datos_usuario['horizonte_inversion'] == 'largo plazo':
        score += 3
    elif datos_usuario['horizonte_inversion'] == 'medio plazo':
        score += 2
    else:
        score += 1
    
    if datos_usuario['objetivo_financiero'] == 3:
        score += 3
    elif datos_usuario['objetivo_financiero'] == 2:
        score += 2
    else:
        score += 1
    
    if datos_usuario['tolerancia_riesgo'] == 3:
        score += 3
    elif datos_usuario['tolerancia_riesgo'] == 2:
        score += 2
    else:
        score += 1
    
    if datos_usuario['estabilidad_ingresos'] == 1:
        score += 2  # Ingresos muy estables
    elif datos_usuario['estabilidad_ingresos'] == 2:
        score += 1  # Moderadamente estables
    else:
        score -= 1  # Altamente variables
    
    if datos_usuario['conocimiento_inversiones'] == 4:
        score += 3  # Conocimientos avanzados
    elif datos_usuario['conocimiento_inversiones'] == 3:
        score += 2  # Familiarizado
    elif datos_usuario['conocimiento_inversiones'] == 2:
        score += 1  # Conocimientos básicos
    else:
        score -= 2  # Sin conocimientos
    
    if datos_usuario['colchon_seguridad'] == 'n':
        score -= 3  # Penalización significativa si no tiene colchón de seguridad.
    #print("score", score)
    
    # Score total
    if score >= 15:
        perfil_riesgo = 5  # Muy agresivo
    elif score >= 12:
        perfil_riesgo = 4  # Agresivo
    elif score >= 8:
        perfil_riesgo = 3  # Moderado
    elif score >= 4:
        perfil_riesgo = 2  # Conservador
    else:
        perfil_riesgo = 1  # Muy conservador
    
    return perfil_riesgo

#datos_usuario = obtener_datos_usuario()
#perfil_riesgo = calcular_perfil_riesgo(datos_usuario)
#print(f"Perfil de riesgo calculado: {perfil_riesgo}")