import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import plugins
from utils.routing import get_city_graph, get_osmnx_route
from utils.metrics import calculate_route_metrics, format_time


def render_main_area():
    # Grafo da malha viária carregado uma única vez — acessível em ambas as tabs
    city_name = st.session_state.get('city_display', "Nova Friburgo, RJ, Brasil")
    G = get_city_graph(city_name)

    cd_lat = st.session_state.lat
    cd_lon = st.session_state.lon

    cores_frota = ['blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'black', 'pink', 'lightgreen', 'gray']

    tab_mapa, tab_ia = st.tabs(["🗺️ Mapa de Rotas", "🤖 Resultado da IA"])

    # ──────────────────────────────────────────────
    # TAB 1 — MAPA
    # ──────────────────────────────────────────────
    with tab_mapa:
        st.subheader(f"Mapa de Rotas: {st.session_state.city_display}")

        veiculos_rotas = st.session_state.get('veiculos_rotas')

        # Filtro de frota compacto — multiselect ocupa uma única linha
        if veiculos_rotas:
            opcoes = [f"Veículo {i+1}" for i in range(len(veiculos_rotas))]
            selecionados = st.multiselect(
                "🚐 Veículos visíveis no mapa",
                options=opcoes,
                default=opcoes,
                key="filtro_frota"
            )
            # Legenda de cores inline
            legenda_html = "&nbsp;&nbsp;".join(
                f"<span style='color:{cores_frota[i % len(cores_frota)]};font-size:18px'>●</span> V{i+1}"
                for i in range(len(veiculos_rotas))
            )
            st.markdown(legenda_html, unsafe_allow_html=True)
            veiculo_ativo = [f"Veículo {i+1}" in selecionados for i in range(len(veiculos_rotas))]
        else:
            veiculo_ativo = []

        # Constrói o mapa
        m = folium.Map(location=[cd_lat, cd_lon], zoom_start=13)

        # Marcador do Centro de Distribuição
        folium.Marker(
            [cd_lat, cd_lon],
            popup="Centro de Distribuição",
            icon=folium.Icon(color='red', icon='hospital-o', prefix='fa')
        ).add_to(m)

        if veiculos_rotas:
            critical_destinations = st.session_state.get('critical_destinations', set())
            idx_destino_global = 1

            for v_idx, sub_rota in enumerate(veiculos_rotas):
                if not veiculo_ativo[v_idx]:
                    continue

                cor_atual = cores_frota[v_idx % len(cores_frota)]

                for dest in sub_rota:
                    if dest == (cd_lat, cd_lon):
                        continue
                    is_critical = dest in critical_destinations
                    folium.Marker(
                        [dest[0], dest[1]],
                        popup=f"V{v_idx+1} - {'⚠️ CRÍTICO - ' if is_critical else ''}Destino {idx_destino_global}",
                        icon=folium.Icon(
                            color='red' if is_critical else cor_atual,
                            icon='exclamation' if is_critical else 'user-md',
                            prefix='fa'
                        )
                    ).add_to(m)
                    idx_destino_global += 1

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
            st.info("Utilize a barra lateral para gerar e otimizar rotas com o Algoritmo Genético.")

        map_key = str(hash(str(st.session_state.get('veiculos_rotas', ''))))
        st_folium(m, width="100%", height=600, returned_objects=[], key=f"map_{map_key}")

    # ──────────────────────────────────────────────
    # TAB 2 — RESULTADO DA IA
    # ──────────────────────────────────────────────
    with tab_ia:
        veiculos_rotas = st.session_state.get('veiculos_rotas')

        # Métricas de eficiência no topo em destaque
        st.subheader("📊 Relatório de Eficiência")

        if veiculos_rotas:
            metrics = calculate_route_metrics(G, veiculos_rotas)
            dist_km   = metrics["total_distance_km"]
            time_min  = metrics["total_time_minutes"]
            num_v     = len(veiculos_rotas)
            total_destinos = sum(
                len([p for p in r if p != (cd_lat, cd_lon)]) - 1
                for r in veiculos_rotas
            )

            c1, c2, c3 = st.columns(3)
            c1.metric("🚐 Veículos em Rota", num_v)
            c2.metric("📍 Distância Total", f"{dist_km} km")
            c3.metric("⏱️ Tempo Estimado", format_time(time_min))
        else:
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("🚐 Veículos em Rota", "—")
            col_m2.metric("📍 Distância Total", "—")
            col_m3.metric("⏱️ Tempo Estimado", "—")

        st.divider()

        # Instruções de entrega por veículo
        st.subheader("📋 Instruções de Entrega por Veículo")

        if veiculos_rotas:
            city = st.session_state.get('city_display', 'cidade')
            critical_destinations = st.session_state.get('critical_destinations', set())

            for v_idx, sub_rota in enumerate(veiculos_rotas):
                destinos = [p for p in sub_rota if p != (cd_lat, cd_lon)]
                n = len(destinos)
                cor = cores_frota[v_idx % len(cores_frota)]

                with st.expander(
                    f"🚐 Veículo {v_idx+1}  —  {n} parada{'s' if n != 1 else ''}",
                    expanded=(v_idx == 0)
                ):
                    st.markdown(f"**Partida:** CD — {city}")
                    for i, dest in enumerate(destinos, start=1):
                        is_critical = dest in critical_destinations
                        badge = "🔴 **CRÍTICO**" if is_critical else f"<span style='color:{cor}'>●</span>"
                        st.markdown(
                            f"{i}. {badge} `({dest[0]:.5f}, {dest[1]:.5f})`",
                            unsafe_allow_html=True
                        )
                    st.markdown(f"**Retorno:** CD")
                    st.caption("⚠️ Em caso de bloqueio viário, contacte a central antes de desviar.")
        else:
            st.info("Execute a otimização na barra lateral para visualizar as instruções de entrega.")
