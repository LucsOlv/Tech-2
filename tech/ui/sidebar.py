import math
import random

import osmnx as ox
import streamlit as st
from genetic_algorithm import run_genetic_algorithm
from utils.geocoding import get_coordinates
from utils.routing import get_city_graph

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
        
        # Parâmetros Numéricos do Algoritmo Genético
        st.divider()
        st.header("🧬 Parâmetros do Algoritmo Genético")
        population_size = st.number_input("Tamanho da População", min_value=10, max_value=500, value=100)
        n_generations = st.number_input("Número de Gerações", min_value=10, max_value=500, value=100)
        mutation_probability = st.slider("Probabilidade de Mutação", 0.0, 1.0, 0.3)
        num_destinos = st.slider("Qtd. de Destinos Gerados Aleatoriamente", 3, 20, 5)
        
        if st.button("🚀 Otimizar Rotas", type="primary"):
            st.info("Algoritmo Genético em execução...")
            
            # Gera pontos aleatórios nos arredores da coordenada atual para simular hospitais
            
            cd_lat = st.session_state.lat
            cd_lon = st.session_state.lon
            
            # Gerador de destinos aleatórios no entorno (+/- 0.05 lat/lon de offset)
            # Os pontos são ancorados no nó de rua mais próximo para nunca cair em
            # montanhas, áreas verdes ou dentro de quarteirosões.
            G = get_city_graph(st.session_state.city_display)
            destinations = []
            seen_nodes = set()  # evita duplicatas caso dois randomicos batam no mesmo nó
            attempts = 0
            while len(destinations) < num_destinos and attempts < num_destinos * 10:
                attempts += 1
                d_lat = cd_lat + random.uniform(-0.05, 0.05)
                d_lon = cd_lon + random.uniform(-0.05, 0.05)
                if G is not None:
                    node = ox.distance.nearest_nodes(G, X=d_lon, Y=d_lat)
                    if node in seen_nodes:
                        continue
                    seen_nodes.add(node)
                    # Substitui pelas coordenadas reais do nó (sempre numa rua)
                    d_lat = G.nodes[node]['y']
                    d_lon = G.nodes[node]['x']
                destinations.append((d_lat, d_lon))
            
            # Marca os primeiros 30% como destinos críticos (medicamentos prioritários)
            if prioridade:
                n_critical = max(1, math.ceil(len(destinations) * 0.3))
                critical_set = set(destinations[:n_critical])
            else:
                critical_set = set()
            st.session_state.critical_destinations = critical_set
            
            # Executa o algoritmo genético incluindo o Centro de Distribuição como um dos pontos (opcional, pode só mapear destinos)
            # Para o Caixeiro Viajante tradicional, a origem também faz parte do ciclo.
            all_points = [(cd_lat, cd_lon)] + destinations
            
            # Preparando a UI de feedback
            progress_bar = st.progress(0.0)
            status_text = st.empty()
            status_text.text("Inicializando população...")
            
            # Função de callback para ser chamada a cada geração pelo algoritmo genético
            def progress_callback(generation, best_fit, route=None):
                progress = (generation + 1) / n_generations
                progress_bar.progress(progress)
                status_text.text(f"Geração {generation+1}/{n_generations} - Melhor Distância: {best_fit:.4f} km")

            best_solutions, best_route = run_genetic_algorithm(
                cities_locations=all_points,
                population_size=population_size,
                n_generations=n_generations,
                mutation_probability=mutation_probability,
                callback=progress_callback
            )
            # best_route é a melhor rota global encontrada em todas as gerações (min fitness)
            
            # Divide os destinos entre os veículos, colocando críticos primeiro
            cd_point = (cd_lat, cd_lon)
            destinos_apenas_raw = [p for p in best_route if p != cd_point]
            if prioridade and critical_set:
                destinos_apenas = (
                    [p for p in destinos_apenas_raw if p in critical_set]
                    + [p for p in destinos_apenas_raw if p not in critical_set]
                )
            else:
                destinos_apenas = destinos_apenas_raw
            
            # Garantir que temos pelo menos a quantidade devida
            num_v = min(num_veiculos, len(destinos_apenas))
            if num_v < 1: num_v = 1
            
            chunk_size = len(destinos_apenas) // num_v
            remainder = len(destinos_apenas) % num_v
            
            veiculos_rotas = []
            idx = 0
            for i in range(num_v):
                take = chunk_size + (1 if i < remainder else 0)
                # O trajeto de cada veiculo é: CD -> Destinos -> CD
                sub_rota = [cd_point] + destinos_apenas[idx:idx+take] + [cd_point]
                veiculos_rotas.append(sub_rota)
                idx += take
            
            status_text.text("Pronto! Desenhando rotas da frota no mapa...")
            
            st.session_state.best_route = best_route
            st.session_state.veiculos_rotas = veiculos_rotas
            st.session_state.num_veiculos = num_v
            
        return num_veiculos, prioridade
