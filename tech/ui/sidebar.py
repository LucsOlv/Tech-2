import streamlit as st
from utils.geocoding import get_coordinates

def render_sidebar():
    with st.sidebar:
        st.header("📍 Localização")
        city_input = st.text_input("Cidade da Operação", value=st.session_state.city_display)
        
        if st.button("Buscar Cidade"):
            new_lat, new_lon, full_address = get_coordinates(city_input)
            if new_lat:
                st.session_state.lat = new_lat
                st.session_state.lon = new_lon
                st.session_state.city_display = full_address
                st.success("Localização atualizada!")
            else:
                st.error("Cidade não encontrada. Tente ser mais específico.")

        st.divider()
        st.header("⚙️ Parâmetros da Frota")
        num_veiculos = st.slider("Veículos Disponíveis", 1, 10, 3)
        
        st.divider()
        st.header("⚖️ Prioridades")
        prioridade = st.checkbox("Priorizar Medicamentos Críticos", value=True)
        
        if st.button("🚀 Otimizar Rotas", type="primary"):
            st.info("Algoritmo Genético em execução...")
            
        return num_veiculos, prioridade
