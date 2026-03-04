import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins
from utils.routing import get_city_graph, get_osmnx_route
from utils.metrics import calculate_route_metrics, format_time

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
        
        # Puxamos a malha viária da cidade atual armazenada no Streamlit session (ou o default Friburgo)
        city_name = st.session_state.get('city_display', "Nova Friburgo, RJ, Brasil")
        G = get_city_graph(city_name)
        
        if 'veiculos_rotas' in st.session_state:
            veiculos_rotas = st.session_state.veiculos_rotas
            cores_frota = ['blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'black', 'pink', 'lightgreen', 'gray']
            
            # Adicionar toggle para cada veículo (Checkbox no Streamlit)
            st.write("### Filtrar Frota")
            cols = st.columns(len(veiculos_rotas))
            veiculo_ativo = []
            
            for i in range(len(veiculos_rotas)):
                cor = cores_frota[i % len(cores_frota)]
                with cols[i]:
                    ativo = st.checkbox(f"Veículo {i+1}", value=True, key=f"v_{i}")
                    veiculo_ativo.append(ativo)
                    if ativo:
                        # Exibe a cor como uma bolinha ou texto colorido
                        st.markdown(f"**<span style='color:{cor}'>● Cor no mapa</span>**", unsafe_allow_html=True)
            
            idx_destino_global = 1
            for v_idx, sub_rota in enumerate(veiculos_rotas):
                if not veiculo_ativo[v_idx]:
                    continue  # Se o usuário desmarcou esse veículo, pula o desenho dele
                    
                cor_atual = cores_frota[v_idx % len(cores_frota)]
                
                # Renderiza marcadores para os destinos dessa sub_rota particular
                for dest in sub_rota:
                    if dest == (cd_lat, cd_lon):
                        continue
                        
                    folium.Marker(
                        [dest[0], dest[1]], 
                        popup=f"V{v_idx+1} - Destino {idx_destino_global}", 
                        icon=folium.Icon(color=cor_atual, icon='user-md', prefix='fa')
                    ).add_to(m)
                    idx_destino_global += 1
                
                # Renderiza as linhas dessa rota
                for i in range(len(sub_rota) - 1):
                    p1 = sub_rota[i]
                    p2 = sub_rota[i + 1]
                    
                    route_coords = get_osmnx_route(G, p1, p2)
                    
                    if route_coords:
                        plugins.AntPath(
                            locations=route_coords,
                            color=cor_atual,
                            weight=5,
                            opacity=0.8,
                            delay=800, 
                            dash_array=[10, 20],
                            tooltip=f"V{v_idx+1} Tr. {i+1}"
                        ).add_to(m)
                        
                        route_line = folium.PolyLine(locations=route_coords, color="transparent", weight=0)
                        route_line.add_to(m)
                        
                        plugins.PolyLineTextPath(
                            route_line,
                            "  ►  ",
                            repeat=True,
                            offset=5,
                            attributes={'fill': 'white', 'font-weight': 'bold', 'font-size': '15'}
                        ).add_to(m)
                    else:
                        folium.PolyLine(
                            locations=[p1, p2],
                            color=cor_atual,
                            weight=4,
                            opacity=0.5,
                            dash_array='5, 5',
                            tooltip=f"V{v_idx+1} Reta {i+1}"
                        ).add_to(m)
        else:
            # Caso ainda não exista rota gerada, apenas mostramos uma mensagem na UI ou os mockados do CD vazio
            st.info("Utilize a barra lateral para gerar e otimizar rotas com o Algoritmo Genético.")

        # O segredo do st_folium atualizar é a 'key'. Mudando a key, o componente renderiza de novo.
        st_folium(m, width="100%", height=550, returned_objects=[])

    with col2:
        st.subheader("📋 Instruções de Entrega (LLM)")
        st.markdown("> As instruções geradas pela IA para os motoristas aparecerão aqui.")
        
        st.divider()
        
        st.subheader("📊 Relatório de Eficiência")
        
        # Calcular ou Resgatar as Métricas Reais do OSMnx
        distancia_txt = "0 km"
        tempo_txt = "0h 0m"
        
        if 'veiculos_rotas' in st.session_state:
            # Chama o módulo de utilidade de cálculo
            metrics = calculate_route_metrics(G, st.session_state.veiculos_rotas)
            
            dist_km = metrics["total_distance_km"]
            time_min = metrics["total_time_minutes"]
            
            distancia_txt = f"{dist_km} km"
            tempo_txt = format_time(time_min)

        st.metric("Distância Total", distancia_txt)
        st.metric("Tempo Estimado", tempo_txt)
