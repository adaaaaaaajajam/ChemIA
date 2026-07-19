import streamlit as st
from PIL import Image
from conversor import mol_a_gramos, litros_a_moles, celsius_a_kelvin
from vle_model import generate_txy_diagram, bubble_point_T
from ethanol_water_params import ANTOINE, VAN_LAAR
import matplotlib.pyplot as plt

st.set_page_config(page_title="ChemIA — Discovery Engine", page_icon="⚗️", layout="centered")
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

st.title("⚗️ ChemIA — Discovery Engine")
st.markdown("Conversiones químicas y predicción de propiedades de mezclas.")
st.markdown("---")

tab_conversor, tab_mezclas, tab_agua = st.tabs(
    ["🔁 Conversor de unidades", "🧪 Propiedades de mezclas", "💧 Datos del agua"]
)

# ---------------------------------------------------------------------------
# TAB 1: Conversor de unidades (tu codigo original, sin cambios funcionales)
# ---------------------------------------------------------------------------
with tab_conversor:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Selecciona la conversión")
    CONVERSIONES = ["Mol → Gramos", "Litros → Moles", "Celsius → Kelvin"]
    conversion = st.selectbox("", CONVERSIONES, label_visibility="collapsed", key="conv_select")
    st.markdown("<br>", unsafe_allow_html=True)
    resultado = None
    unidad = ""
    detalle = ""

    if conversion == "Mol → Gramos":
        st.markdown("### Parámetros")
        col1, col2 = st.columns(2)
        with col1:
            moles = st.number_input("Moles (mol)", min_value=0.0, value=1.0, step=0.1, format="%.4f")
        with col2:
            masa_molar = st.number_input("Masa molar (g/mol)", min_value=0.001, value=18.015, step=0.001, format="%.3f")
        if st.button("Calcular", key="btn_mol_g"):
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
        if st.button("Calcular", key="btn_l_mol"):
            resultado = litros_a_moles(litros, densidad, masa_molar)
            unidad = "mol"
            detalle = f"{litros} L · {densidad} g/mL ÷ {masa_molar} g/mol"

    elif conversion == "Celsius → Kelvin":
        st.markdown("### Parámetros")
        celsius = st.number_input("Temperatura (°C)", value=25.0, step=0.1, format="%.2f")
        if st.button("Calcular", key="btn_c_k"):
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

# ---------------------------------------------------------------------------
# TAB 2: Propiedades de mezclas (nuevo - motor VLE, primera pieza del
# discovery engine). Por ahora solo etanol-agua; se ira ampliando.
# ---------------------------------------------------------------------------
with tab_mezclas:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Sistema binario: Etanol — Agua")
    st.caption("Modelo clásico (Antoine + van Laar) — línea base del discovery engine")

    P_total = st.slider("Presión total (mmHg)", 400, 1520, 760, step=10)
    df = generate_txy_diagram(ANTOINE["ethanol"], ANTOINE["water"], VAN_LAAR, P_total_mmHg=P_total)

    fig, ax = plt.subplots()
    ax.plot(df["x1"], df["T_celsius"], label="Líquido (x1)", color="#1a4731")
    ax.plot(df["y1"], df["T_celsius"], label="Vapor (y1)", color="#2d7a4f")
    ax.set_xlabel("Fracción molar de etanol")
    ax.set_ylabel("Temperatura (°C)")
    ax.set_title(f"Diagrama T-x-y — P = {P_total} mmHg")
    ax.legend()
    st.pyplot(fig)

    st.markdown("### Consulta puntual")
    x1_input = st.slider("Fracción molar de etanol en el líquido (x1)", 0.01, 0.99, 0.5)
    T, y1 = bubble_point_T(x1_input, P_total, ANTOINE["ethanol"], ANTOINE["water"], VAN_LAAR)
    col1, col2 = st.columns(2)
    col1.markdown(f'<div class="result-box">{T:.2f} °C</div>', unsafe_allow_html=True)
    col1.caption("Temperatura de ebullición")
    col2.markdown(f'<div class="result-box">{y1:.3f}</div>', unsafe_allow_html=True)
    col2.caption("Fracción molar de etanol en el vapor")

    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(
        "Siguiente paso: sustituir/ampliar este modelo con datos reales del NIST/DDB "
        "y con la API de Claude para razonar sobre sistemas nuevos."
    )

# ---------------------------------------------------------------------------
# TAB 3: Datos del agua (tu grafica.png original, sin cambios)
# ---------------------------------------------------------------------------
with tab_agua:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Propiedades termodinámicas del agua")
    st.caption("Temperatura vs Presión de vapor — generada con `analisis.py`")
    try:
        img = Image.open("grafica.png")
        st.image(img, use_container_width=True)
    except FileNotFoundError:
        st.warning("No se encontró `grafica.png`. Ejecuta `analisis.py` primero para generarla.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("ChemIA · Conversiones de unidades · Datos termodinámicos · Discovery engine de mezclas")
