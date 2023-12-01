import streamlit as st
import pandas as pd
import statsmodels.api as sm
import shelve
from datetime import datetime

s = shelve.open("./ARIMA_model.db")
arima_model = s.get("model")
s.close()

def predict_energy_consumption(year, month, steps=1):
    prediction_dates = []
    prediction_values = []
    start_date = f"{year}-{month:02d}-01"

    start_date = pd.to_datetime(start_date)

    for _ in range(steps):
        prediction = arima_model.get_forecast(steps=3)
        predicted_value = prediction.predicted_mean.iloc[1]
        rounded_value = round(predicted_value, 2)
        prediction_dates.append(start_date.strftime('%Y-%m-%d'))
        prediction_values.append(rounded_value)
        start_date = start_date + pd.DateOffset(months=1)

    return prediction_dates, prediction_values

st.set_page_config(
    page_title="Consumo Eléctrico",
    page_icon="💡",
    layout="wide"
)

st.markdown("# 👋 Bienvenido a la Aplicación de Consumo Eléctrico")

with st.expander("Hacer una predicción", expanded=True):
    year = st.number_input("Ingresa el año", value=datetime.today().year, min_value=2010, max_value=datetime.today().year + 10)
    month = st.number_input("Ingresa el mes", value=datetime.today().month, min_value=1, max_value=12)
    predicted = st.button("Predecir")
    if predicted:
        steps = 1
        prediction_dates, prediction_values = predict_energy_consumption(year, month, steps)
        st.success(f"La predicción de consumo de energía para el próximo año es: {prediction_values}")

st.markdown("## Consumo de Energia en Tetuán, Marruecos.")

st.write("""
    <style>
        @keyframes slide-in {
            0% {
                transform: translateX(-100%);
            }
            100% {
                transform: translateX(0);
            }
        }
        .slide-in-animation {
            animation: slide-in 1.5s ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

st.write('<div class="slide-in-animation">Tetuán, es una ciudad costera en el norte de Marruecos que abarca 10,375 km² con una población de 550,374 habitantes. Marruecos, con un consumo per cápita de energía de 0.56 toneladas en 2020, importa todos sus productos petroleros desde el cierre de su refinería en 2015. La red eléctrica de Tetuán, alimentada por tres estaciones, es gestionada por Amendis, asegurando la distribución desde la Oficina Nacional de Electricidad. Investigar el impacto en el consumo de energía en Tetuán es crucial dada su relevancia en el panorama eléctrico nacional 💡.</div>', unsafe_allow_html=True)

st.sidebar.title("Páginas")
page_list = ["Inicio"]
page_selection = st.sidebar.selectbox("Selecciona una página", page_list)
if page_selection == "Inicio":
    pass