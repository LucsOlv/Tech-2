import streamlit as st
from streamlit_folium import st_folium
import folium
from utils.routing import get_osrm_route

def render_main_area():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Mapa de Rotas: {st.session_state.city_display}")
        
        # Criamos o mapa sempre usando o estado atual
        cd_lat = st.session_state.lat
        cd_lon = st.session_state.lon
        
        m = folium.Map(location=[cd_lat, cd_lon], zoom_start=13)
        
        # Marcador do Centro de Distribuição
        folium.Marker(
            [cd_lat, cd_lon], 
            popup="Centro de Distribuição", 
            icon=folium.Icon(color='red', icon='hospital-o', prefix='fa')
        ).add_to(m)

        # Mock: 3 Hospitais/Clínicas de destino próximos para gerar rotas (adicionando offset na lat/lon)
        destinations = [
            (cd_lat + 0.015, cd_lon + 0.015),
            (cd_lat - 0.010, cd_lon + 0.020),
            (cd_lat + 0.005, cd_lon - 0.015),
        ]
        
        colors = ['blue', 'green', 'purple']
        
        for idx, dest in enumerate(destinations):
            # Marcador do Destino
            folium.Marker(
                [dest[0], dest[1]], 
                popup=f"Destino {idx+1}", 
                icon=folium.Icon(color=colors[idx], icon='user-md', prefix='fa')
            ).add_to(m)
            
            # Buscar a rota real via OSRM
            route_coords = get_osrm_route((cd_lat, cd_lon), dest)
            
            if route_coords:
                # Desenhar a rota real seguindo as ruas
                folium.PolyLine(
                    locations=route_coords,
                    color=colors[idx],
                    weight=4,
                    opacity=0.8,
                    tooltip=f"Rota para Destino {idx+1}"
                ).add_to(m)
            else:
                # Fallback: se a API falhar, desenha linha reta para evitar que o mapa fique vazio
                folium.PolyLine(
                    locations=[(cd_lat, cd_lon), dest],
                    color='gray',
                    weight=4,
                    opacity=0.5,
                    dash_array='5, 5',
                    tooltip=f"Rota Reta (Fallback) para Destino {idx+1}"
                ).add_to(m)

        # O segredo do st_folium atualizar é a 'key'. Mudando a key, o componente renderiza de novo.
        st_folium(m, width="100%", height=550, key=f"map_{st.session_state.lat}_{st.session_state.lon}")

    with col2:
        st.subheader("📋 Instruções de Entrega (LLM)")
        st.markdown("> As instruções geradas pela IA para os motoristas aparecerão aqui.")
        
        st.divider()
        
        st.subheader("📊 Relatório de Eficiência")
        st.metric("Distância Total", "0 km", "0%")
        st.metric("Tempo Estimado", "0h 0m", "0%")
