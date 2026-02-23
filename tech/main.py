import streamlit as st
from streamlit_folium import st_folium
import folium

# Configuração da página
st.set_page_config(page_title="Otimizador de Rotas Médicas", layout="wide")

st.title("🏥 Tech Challenge - Otimização de Logística Hospitalar")

PARAMS_INPUT = {
    "city_name": "Nova Friburgo, RJ, Brasil",
    "num_veiculos": 3,
    "capacidade": 50,
    "autonomia": 100,
    "prioridade_critica": True
}

# --- SIDEBAR: Parâmetros e Restrições ---
with st.sidebar:
    st.header("Configurações da Frota")
    
    # --- PARÂMETROS DE ENTRADA ---
    city_name = st.text_input("Nome da Cidade", PARAMS_INPUT["city_name"]) #    
    num_veiculos = st.slider("Quantidade de Veículos", 1, 10, PARAMS_INPUT["num_veiculos"]) # 
    capacidade = st.number_input("Capacidade de Carga (unidades)", 10, 100, PARAMS_INPUT["capacidade"]) # 
    autonomia = st.number_input("Autonomia Máxima (km)", 10, 500, PARAMS_INPUT["autonomia"]) # 
    PARAMS_INPUT["city_name"] = city_name
    PARAMS_INPUT["num_veiculos"] = num_veiculos
    PARAMS_INPUT["capacidade"] = capacidade
    PARAMS_INPUT["autonomia"] = autonomia
    # --- PARÂMETROS DE ENTRADA ---
    
    st.divider()
    st.header("Prioridades")
    prioridade_critica = st.checkbox("Priorizar Medicamentos Críticos", value=True) # 
    
    st.divider()
    if st.button("🚀 Otimizar Rotas", type="primary"):
        st.write("Rodando Algoritmo Genético...")

# --- ÁREA PRINCIPAL ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mapa de Entregas") # 
    # Placeholder para o mapa real (Folium)
    m = folium.Map(location=[-23.5505, -46.6333], zoom_start=12) # Exemplo: SP
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("Instruções da IA (LLM)") # [cite: 68]
    st.info("As rotas otimizadas aparecerão aqui em formato de texto para os motoristas.")
    
    st.subheader("Relatório de Eficiência") # [cite: 69]
    st.write("Métricas de tempo e economia serão listadas abaixo.")