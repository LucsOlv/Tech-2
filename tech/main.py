import streamlit as st
from ui.sidebar import render_sidebar
from ui.main_area import render_main_area

# Configuração da página
st.set_page_config(page_title="Otimizador de Rotas Médicas", layout="wide")

# Inicializa o estado para não perder as coordenadas entre interações
if 'lat' not in st.session_state:
    st.session_state.lat = -22.2819 # Default: Nova Friburgo
    st.session_state.lon = -42.5311
    st.session_state.city_display = "Nova Friburgo, RJ, Brasil"

st.title("🏥 Tech Challenge - Otimização de Logística Hospitalar")

# --- SIDEBAR: Parâmetros e Localização ---
num_veiculos, prioridade = render_sidebar()

# --- ÁREA PRINCIPAL ---
render_main_area()