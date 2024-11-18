# FinancialAdvisorLLM

Este proyecto tiene como objetivo fine-tunear un modelo NLP para el asesoramiento fiscal, 
con el objetivo de ofrecer recomendaciones personalizadas de inversión basadas en el contexto de cada usuario, 
teniendo en cuenta características como el perfil de riesgo, la edad, la situación financiera, etc.

Para su realización, es necesario seguir una serie de pasos:
* Preprocesamiento y limpieza de datos
* Desarrollo del algoritmo de perfil de riesgo de los usuarios
* Desarrollo del algoritmo para predecir el perfil de riesgo de nuevos usuarios 
* Desarrollo del sistema de preguntas y respuestas para generar datos de este tipo 
* Entrenamiento y validación del modelo NLP Zephyr 7b Beta

## Preprocesamiento y limpieza de datos

Para reproducir este paso, primero es necesario descargar los archivos de datos localmente, ya que no es posible subirlo al repositorio por su tamaño elevado:

* [crypto W1](https://www.kaggle.com/datasets/olegshpagin/crypto-coins-prices-ohlcv?select=W1): Descargar el comprimido y descomprimirlo en la carpeta crypto W1.
* [eu etf](https://www.kaggle.com/datasets/stefanoleone992/european-funds-dataset-from-morningstar?select=Morningstar+-+European+ETFs.csv): Descargar el archivo y colocarlo en la carpeta eu etf.
* [sp500](https://www.kaggle.com/datasets/andrewmvd/sp-500-stocks?select=sp500_stocks.csv): Descargar el archivo y colocarlo en la carpeta sp500.

Una vez descargados, ya es posible ejecutar los scripts desde la carpeta /scripts:

### ETF

Primero, es necesario limpiar el dataset de ETF, ya que este nos servirá de referencia los demas datasets. Primero se ejecuta *'clean_etf.py'*, el cual realizará
la limpieza inicial de los datos. Después, se debe ejecuta *'procesar_etf.py'*, el cual principalmente tiene como objetivo entrenar el algoritmo RandomForestRegressor
para, dados los valores sin ningun campo nulo, pueda rellenar de la forma más precisa posible los campos nulos tanto de risk_rating como de performance_rating. 

El campo de risk_rating es especialmente importante, ya que este campo es el que relaciona el perfil de riesgo del usuario con el nivel de riesgo del fondo. Por otro lado,
performance_rating tiene exactamente el mismo número de valores nulos que risk_rating, y por lo tanto son las mismas filas las que se ven afectadas por esto, y se puede hacer
lo mismo con este campo sin ningun paso adicional, tan solo entrenar de nuevo otro algoritmo RandomForestRegressor.

Una vez ejecutados estos dos scripts, nos dejará el archivo final *'eu_etf_dataset_predict.csv'*, con los datos ya completamente procesados, bajo la carpeta /cleandata.

### Crypto

Para la limpieza de los datos de criptomonedas, tan solo es necesario ejecutar el archivo *'clean_crypto.py'*, ya que el risk_rating de este dataset será de 5 para todas y no necesita de
procesamiento adicional. Este script además agrupará los datos de manera semanal en vez de diaria, para de esta forma reducir el volumen de datos significativamente
sin perder prácticamente nada de información. Esto nos dejará el archivo *'__combined_crypto_data.csv'*.

### S&P 500

Para el dataset del sp500, es necesario ejecutar *'clean_sp500.py'*, el cual realizará la limpieza inicial de estos datos y agrupandolos semanalmente también. 
Después, se debe ejecuta *'sp500_risk_rating.py'*, el cual, basándose en el risk_rating de los ETFs, calculará un risk_rating para cada acción según el rendimiento
que haya tenido cada acción, buscando similitudes con el rendimiento del ETF y su risk_rating.

Una vez ejecutados estos dos scripts, nos dejará el archivo final *'sp500riskrating.csv'*, con los datos ya completamente procesados, también bajo la carpeta /cleandata.

## Desarrollo del algoritmo de perfil de riesgo 

Este algoritmo ha sido implementado teniendo en cuenta valores muy importantes como la edad, ingresos mensuales, gastos, deuda, objetivo finanicero, horizonte de inversión, tolerancia al riesgo...
Hace un recuento de la puntuación final según la respuesta a cada una de las preguntas sobre los campos importantes, y según esta puntuación se le asigna al usuario un valor del 1 al 5, 
tal como están valorados todos los tipos de inversión. Para poder acceder a una prueba de este algoritmo, tan solo es necesario descomentar las últimas lineas del archivo ubicado en
*'/scripts/user_risk_rating.py'* y ejecutarlo.

Ahora, es posible generar un dataset de usuarios, cubriendo todos los posibles casos de usuarios. Este dataset se ha generado de manera automática, de un total de 2000 usuarios, siguiendo una serie
de restricciones y normas para que sean casos de usuarios reales:
* Ingresos: A la mayoría de usuarios (90%), se le han establecido unos ingresos de entre 800 y 3000€, teniendo algunos casos (10%) de ingresos más elevados, de entre 3000 y 8000€. 
* Gastos: A la mayoría de los usuarios (70%), se le han establecido unos gastos de entre 500 y 1500€ mensuales, pero con algunos casos de 0 gastos (20%) y otros tienen gastos elevados (10%) entre 1500 y 2500 EUR.
* Ahorro: El ahorro mensual, se calcula como la diferencia entre los ingresos y los gastos, con restricciones:
	* No puede ser negativo.
	* Debe ser al menos 100€, para evitar casos irreales de gasto total.
* Deuda: La mayoría de los usuarios no tienen una deuda (70%), pero el resto (30%) tienen una deuda de entre 200 y 1500€ mensuales. Como deuda, se cuentan una hipoteca, un préstamo personal…
* Para el resto de campos necesarios para el algoritmo, se han generado valores aleatorios para todos ellos, ya que estos no son los que generar casos imposibles, y un usuario con cualquier valor de estos campos puede ser real.

