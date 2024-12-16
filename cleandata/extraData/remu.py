import pandas as pd

mejores_cuentas = [
    {
        "bank": "Trade Republic",
        "account_name": "Cuenta de Ahorro",
        "TAE": "3.30%",
        "TIN": "N/D",
        "max_remunerated_balance": "50,000 €",
        "commissions": "Ninguna",
        "details": "Intereses ingresados mensualmente; sin requisitos adicionales."
    },
    {
        "bank": "Openbank",
        "account_name": "Cuenta Ahorro Bienvenida",
        "TAE": "2.27%",
        "TIN": "2.25%",
        "max_remunerated_balance": "100,000 €",
        "commissions": "Ninguna",
        "details": "Rentabilidad durante 12 meses; sin gastos de administración ni mantenimiento."
    },
    {
        "bank": "EVO Banco",
        "account_name": "Cuenta Inteligente Bienvenida",
        "TAE": "2.85%",
        "TIN": "N/D",
        "max_remunerated_balance": "30,000 €",
        "commissions": "Ninguna",
        "details": "Incluye tarjeta sin comisiones; transferencias inmediatas gratuitas."
    },
    {
        "bank": "MyInvestor",
        "account_name": "Cuenta Remunerada",
        "TAE": "2.00%",
        "TIN": "N/D",
        "max_remunerated_balance": "70,000 €",
        "commissions": "Ninguna",
        "details": "Sin necesidad de domiciliar la nómina; tarjeta de débito y crédito gratuita."
    },
    {
        "bank": "Banco Sabadell",
        "account_name": "Cuenta Online",
        "TAE": "2.50%",
        "TIN": "N/D",
        "max_remunerated_balance": "50,000 €",
        "commissions": "Ninguna",
        "details": "Devolución del 3% en recibos de luz y gas; tarjetas bancarias sin comisiones."
    },
    {
        "bank": "inbestMe",
        "account_name": "Cartera de Ahorro",
        "TAE": "3.10%",
        "TIN": "N/D",
        "max_remunerated_balance": "Sin límite",
        "commissions": "Ninguna",
        "details": "Rentabilidad variable ligada al BCE; depósitos a partir de 1,000 €."
    },
    {
        "bank": "Bunq",
        "account_name": "Cuenta Easy Savings",
        "TAE": "3.36%",
        "TIN": "N/D",
        "max_remunerated_balance": "Sin límite",
        "commissions": "Ninguna",
        "details": "Pago de intereses semanal; tarjeta prepago virtual gratuita."
    }
]

cuentas_df = pd.DataFrame(mejores_cuentas)
cuentas_csv_path = './cuentas_ahorro.csv'
cuentas_df.to_csv(cuentas_csv_path, index=False)