import streamlit as st
from PIL import Image
from conversor import mol_a_gramos, litros_a_moles, celsius_a_kelvin

st.set_page_config(page_title="ChemIA — Conversor de Unidades", page_icon="⚗️", layout="centered")

st.markdown(
    """
    <style>
        :root { --green: #1a4731; --green-light: #2d7a4f; --green-soft: #e8f5ee; }

        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f4faf7;
        }
        [data-testid="stSidebar"] { background-color: #1a4731; }

        h1 { color: #1a4731 !important; font-weight: 800; letter-spacing: -0.5px; }
        h3 { color: #2d7a4f !important; }

        div[data-baseweb="select"] > div {
            border: 2px solid #2d7a4f !important;
            border-radius: 8px !important;
        }
        input[type="number"] {
            border: 2px solid #2d7a4f !important;
            border-radius: 8px !important;
        }

        div.stButton > button {
            background-color: #1a4731;
            color: white;
            font-size: 1.1rem;
            font-weight: 700;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 2.5rem;
            width: 100%;
            transition: background 0.2s;
        }
        div.stButton > button:hover {
            background-color: #2d7a4f;
            color: white;
        }

        .result-box {
            background: #1a4731;
            color: #ffffff;
            font-size: 2rem;
            font-weight: 800;
            text-align: center;
            padding: 1.2rem 1.5rem;
            border-radius: 14px;
            margin-top: 1.2rem;
            letter-spacing: 0.5px;
        }
        .section-card {
            background: #ffffff;
            border: 1.5px solid #b7dfc8;
            border-radius: 14px;
            padding: 1.5rem 1.8rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(26,71,49,0.07);
        }
        hr { border-color: #b7dfc8; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚗️ ChemIA — Conversor de Unidades")
st.markdown("Conversiones químicas rápidas y precisas.")
st.markdown("---")

CONVERSIONES = [
    "Mol → Gramos",
    "Litros → Moles",
    "Celsius → Kelvin",
]

with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Selecciona la conversión")
    conversion = st.selectbox("", CONVERSIONES, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    resultado = None
    unidad = ""

    if conversion == "Mol → Gramos":
        st.markdown("### Parámetros")
        col1, col2 = st.columns(2)
        with col1:
            moles = st.number_input("Moles (mol)", min_value=0.0, value=1.0, step=0.1, format="%.4f")
        with col2:
            masa_molar = st.number_input("Masa molar (g/mol)", min_value=0.001, value=18.015, step=0.001, format="%.3f")

        if st.button("Calcular"):
            resultado = mol_a_gramos(moles, masa_molar)
            unidad = "g"
            detalle = f"{moles} mol × {masa_molar} g/mol"

    elif conversion == "Litros → Moles":
        st.markdown("### Parámetros")
        col1, col2, col3 = st.columns(3)
        with col1:
            litros = st.number_input("Volumen (L)", min_value=0.0, value=1.0, step=0.1, format="%.4f")
        with col2:
            densidad = st.number_input("Densidad (g/mL)", min_value=0.001, value=1.0, step=0.001, format="%.3f")
        with col3:
            masa_molar = st.number_input("Masa molar (g/mol)", min_value=0.001, value=18.015, step=0.001, format="%.3f")

        if st.button("Calcular"):
            resultado = litros_a_moles(litros, densidad, masa_molar)
            unidad = "mol"
            detalle = f"{litros} L · {densidad} g/mL ÷ {masa_molar} g/mol"

    elif conversion == "Celsius → Kelvin":
        st.markdown("### Parámetros")
        celsius = st.number_input("Temperatura (°C)", value=25.0, step=0.1, format="%.2f")

        if st.button("Calcular"):
            resultado = celsius_a_kelvin(celsius)
            unidad = "K"
            detalle = f"{celsius} °C + 273.15"

    if resultado is not None:
        st.markdown(
            f'<div class="result-box">Resultado: {resultado:.4f} {unidad}</div>',
            unsafe_allow_html=True,
        )
        st.caption(f"Fórmula aplicada: {detalle} = {resultado:.4f} {unidad}")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Propiedades termodinámicas del agua")
st.caption("Temperatura vs Presión de vapor — generada con `analisis.py`")

try:
    img = Image.open("grafica.png")
    st.image(img, use_container_width=True)
except FileNotFoundError:
    st.warning("No se encontró `grafica.png`. Ejecuta `analisis.py` primero para generarla.")

st.markdown("---")
st.caption("ChemIA · Conversiones de unidades químicas · Datos termodinámicos reales del agua")
