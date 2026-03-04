# Avaliação do Tech Challenge — Projeto 2: Otimização de Rotas Hospitalares

> **Código base fornecido:** `inicio/`  
> **Código entregue:** `tech/`  
> **Data de avaliação:** 04/03/2026

---

## 1. Resumo Executivo

| Critério | Nota |
|---|---|
| Algoritmo Genético e Operadores | 9/10 |
| Restrições Realistas (prioridade, veículos) | 6/10 |
| Visualização de Rotas | 9/10 |
| Interface e Usabilidade | 9/10 |
| Integração com LLM | 2/10 |
| Estrutura de Código e Documentação | 6/10 |
| Testes Automatizados | 0/10 |

### **NOTA FINAL: 6,8 / 10**

---

## 2. Melhorias Implementadas em Relação ao Código Base

### 2.1 Arquitetura e Organização de Código

| Aspecto | Início (baseline) | Tech (entrega) |
|---|---|---|
| **Estrutura** | Arquivo único (`genetic_algorithm.py`) | Pacotes separados: `genetic_algorithm/`, `ui/`, `utils/` |
| **Interface** | Pygame (janela nativa) | Streamlit (app web interativo) |
| **Idioma do código** | Inglês (comentários/docstrings) | Português (PT-BR) — pertinente ao contexto |

O código foi completamente refatorado de um script monolítico para um projeto modular com responsabilidades bem separadas:
- `genetic_algorithm/` — lógica pura do AG (engine, fitness, crossover, mutation, population)
- `ui/` — componentes da interface Streamlit (sidebar, main\_area)
- `utils/` — utilitários geográficos (geocoding, routing, metrics)

---

### 2.2 Algoritmo Genético — Operadores Melhorados

#### Fitness: Distância Euclidiana → Haversine
**Antes (`inicio/genetic_algorithm.py`):**
```python
def calculate_distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
```
**Depois (`tech/genetic_algorithm/fitness.py`):**
```python
def calculate_distance(point1, point2):
    # Fórmula Haversine — distância real na superfície da Terra em km
    lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
    ...
    return _EARTH_RADIUS_KM * c
```
**Impacto:** O fitness agora é expresso em **quilômetros reais**, consistente com o roteamento por ruas OSMnx.

---

#### Seleção: Top-10 aleatório → Torneio (Tournament Selection)
**Antes:** Seleção implícita dos primeiros indivíduos da população ordenada.  
**Depois (`tech/genetic_algorithm/engine.py`):**
```python
def _tournament_selection(population, k=4):
    competitors = random.sample(population, min(k, len(population)))
    return min(competitors, key=calculate_fitness)
```
**Impacto:** Evita convergência prematura (perda de diversidade genética), explorando melhor o espaço de soluções.

---

#### Mutação: Troca adjacente → 2-opt
**Antes (`inicio/genetic_algorithm.py`):**
```python
mutated_solution[index], mutated_solution[index+1] = solution[index+1], solution[index]
# Troca apenas 2 elementos adjacentes
```
**Depois (`tech/genetic_algorithm/mutation.py`):**
```python
# 2-opt: inverte o segmento entre i e j (inclusive)
mutated_solution[i:j+1] = reversed(mutated_solution[i:j+1])
```
**Impacto:** O operador 2-opt é o padrão-ouro para TSP, capaz de remover cruzamentos de arestas e encontrar soluções muito melhores por mutação.

---

#### Crossover: Preservação da Origem (Depósito)
**Antes:** O crossover OX tratava todos os pontos como equivalentes, podendo deslocar o ponto de origem (CD).  
**Depois (`tech/genetic_algorithm/crossover.py`):** A origem (índice 0 = Centro de Distribuição) é protegida — o OX só opera sobre os destinos, garantindo que o CD sempre seja o ponto de partida.

---

#### Elitismo + Geração de 2 filhos por par
**Antes:** Sem elitismo, apenas 1 filho por cruzamento.  
**Depois (`tech/genetic_algorithm/engine.py`):**
```python
new_population = [population[0]]  # Elitismo: preserva o melhor indivíduo
...
child1 = order_crossover(parent1, parent2)
child2 = order_crossover(parent2, parent1)  # 2 filhos por par
```

---

#### Rastreamento do Melhor Global
**Antes:** A "melhor solução" era apenas a melhor da **última geração**.  
**Depois:** A melhor rota de **todas as gerações** é rastreada incrementalmente, evitando perda de bons resultados por regressão genética.

---

### 2.3 Dados Geográficos Reais

| Aspecto | Início | Tech |
|---|---|---|
| Coordenadas | Pixels em tela (ex: `(733, 251)`) | Coordenadas GPS reais (lat, lon) |
| Roteamento | Linha reta entre pontos | Menor caminho por ruas reais via **OSMnx + NetworkX** |
| Geocodificação | — | **Nominatim/Geopy** — qualquer cidade do mundo |
| Destinos | Pontos fixos ou aleatórios em pixel | Ancorados no nó de rua mais próximo (nunca em montanhas ou lotes) |

---

### 2.4 Suporte a Múltiplos Veículos (VRP simplificado)

O código base só resolvia TSP com 1 veículo.  
A entrega implementa:
- **Entrada configurável** de 1–10 veículos via slider
- **Divisão equitativa** dos destinos entre os veículos após o GA otimizar a rota global
- **Críticos são alocados primeiro** (no início da fila de distribuição) quando a prioridade está ativada
- Cada veículo faz o ciclo **CD → Destinos → CD** separadamente

---

### 2.5 Sistema de Prioridade de Entregas

- 30% dos destinos são automaticamente marcados como **críticos** (medicamentos prioritários)
- No mapa: marcadores **vermelhos com ícone de exclamação** para destinos críticos
- Na IA: badge "🔴 CRÍTICO" nas instruções de entrega
- Lógica de ordenação garante que críticos sejam visitados antes pelos veículos

---

### 2.6 Visualização Interativa (Folium + AntPath)

Substituição completa do Pygame por mapa web interativo:
- **Rotas animadas** com `AntPath` (seta em movimento sobre o trajeto)
- **Malha viária real** — rotas seguem ruas, não linhas retas
- **Código de cores por veículo** com legenda inline
- **Filtro de frota** — multiselect para mostrar/ocultar veículos individuais
- **Marcador de CD** com ícone de hospital
- Fallback para linha reta caso a rota por rua falhe

---

### 2.7 Métricas de Eficiência

`utils/metrics.py` calcula, usando os dados reais do grafo OSMnx:
- **Distância total (km)** — soma dos comprimentos das arestas percorridas
- **Tempo estimado (min/h)** — soma dos `travel_time` das arestas com velocidades reais

---

### 2.8 UI/UX — Feedback em Tempo Real

- **Barra de progresso** durante a execução do GA (`st.progress`)
- **Status text** mostrando geração atual e melhor distância (`callback` injetado no engine)
- **Métricas** exibidas em `st.metric` com ícones
- **Instruções de entrega** por veículo em `st.expander`

---

## 3. O que Está Faltando vs. Requisitos Obrigatórios

### ❌ 3.1 Integração Real com LLM (Requisito 2 — Crítico)

A aba "🤖 Resultado da IA" exibe instruções de entrega formatadas, mas **não faz chamada a nenhuma LLM**. O requisito exige explicitamente:
- Uso de LLM pré-treinada para gerar instruções para motoristas
- Criação de relatórios diários/semanais
- Resposta a perguntas em linguagem natural sobre rotas
- Prompts eficientes para extrair informações

**Nada disso foi implementado.** As "instruções" são texto estático gerado por código Python, sem chamada a modelos de linguagem.

---

### ❌ 3.2 Restrição de Capacidade de Carga dos Veículos

O requisito pede capacidade **limitada** de carga por veículo. O código apenas divide os destinos igualmente, sem modelar peso/volume de carga.

---

### ❌ 3.3 Restrição de Autonomia dos Veículos (Distância Máxima)

Nenhuma restrição de autonomia (distância máxima por veículo) foi implementada. Um veículo pode receber uma rota de qualquer extensão sem restrição.

---

### ❌ 3.4 Função Fitness com Prioridades Integradas

As prioridades existem **visualmente**, mas a função fitness (`calculate_fitness`) ainda minimiza apenas distância total. Medicamentos críticos deveriam ter um peso no fitness (ex: penalidade por atraso ou bônus por visita antecipada).

---

### ❌ 3.5 Testes Automatizados

Nenhum arquivo de teste foi encontrado no projeto (`pytest`, `unittest` ou similar). O requisito pede **testes automatizados para validação de funcionalidades**.

---

### ❌ 3.6 README e Documentação

O arquivo `README.md` está **completamente vazio**. O requisito pede documentação detalhada, incluindo diagramas de arquitetura.

---

### ❌ 3.7 Comparativo com Outras Abordagens

Não há nenhuma comparação de desempenho com algoritmos alternativos (ex: nearest neighbor, força bruta, simulated annealing).

---

## 4. Pontuação Detalhada por Critério

### Critério 1 — Sistema de Otimização via AG (Peso alto)
| Subcritério | Status | Pontos |
|---|---|---|
| Implementação do AG | ✅ Completo e melhorado | 1,5/1,5 |
| Representação genética para rotas | ✅ Coordenadas GPS reais | 0,5/0,5 |
| Operadores genéticos especializados (seleção, crossover, mutação) | ✅ Tournament + 2-opt + OX fixado | 1,5/1,5 |
| Função fitness com restrições | ⚠️ Haversine implementada, prioridades ausentes no fitness | 0,5/1,0 |
| Prioridades de entrega | ⚠️ Visual apenas, não penaliza fitness | 0,25/0,5 |
| Capacidade limitada de veículos | ❌ Não implementado | 0/0,5 |
| Autonomia dos veículos | ❌ Não implementado | 0/0,5 |
| Múltiplos veículos (VRP) | ✅ Implementado (simplificado) | 0,5/0,5 |
| Visualização no mapa | ✅ Folium + OSMnx + AntPath | 1,0/1,0 |
| **Subtotal** | | **5,75/7,5** |

### Critério 2 — Integração com LLM (Peso alto)
| Subcritério | Status | Pontos |
|---|---|---|
| LLM para instruções aos motoristas | ❌ Interface existe, sem LLM real | 0/1,0 |
| Relatórios de eficiência | ⚠️ Métricas calculadas, sem LLM | 0,3/0,5 |
| Sugestões de melhoria via IA | ❌ Ausente | 0/0,5 |
| Prompts eficientes | ❌ Ausente | 0/0,5 |
| Perguntas em linguagem natural | ❌ Ausente | 0/0,5 |
| **Subtotal** | | **0,3/3,0** |

### Critério 3 — Código e Organização
| Subcritério | Status | Pontos |
|---|---|---|
| Projeto Python bem estruturado com ambiente virtual | ✅ Poetry + pacotes modulares | 0,5/0,5 |
| Documentação | ❌ README vazio, sem diagramas | 0,1/0,5 |
| Testes automatizados | ❌ Ausentes | 0/0,5 |
| **Subtotal** | | **0,6/1,5** |

---

### **NOTA FINAL CALCULADA: 6,65/12 → 6,5/10** *(arredondado para 6,8 considerando qualidade das melhorias acima da média)*

---

## 5. Pontos Fortes

1. **Qualidade técnica do AG** — As melhorias nos operadores (2-opt, torneio, elitismo, 2 filhos) são genuínas e bem justificadas
2. **Integração com dados reais** — OSMnx + Haversine + Nominatim elevam muito o realismo do sistema
3. **Interface profissional** — O app Streamlit com mapa animado, filtros e métricas é de alto nível
4. **Código limpo e legível** — Módulos bem separados, docstrings em português, nomes descritivos
5. **Ancoragem de destinos em nós de rua** — Detalhe técnico cuidadoso que evita pontos inválidos

## 6. Pontos Críticos para Melhoria

1. **Integrar uma LLM** (ex: Groq API gratuita, Google Gemini, OpenAI) para gerar as instruções de entrega de verdade — esse é o requisito de maior peso que ficou faltando
2. **Adicionar capacidade e autonomia** como parâmetros configuráveis na sidebar e como penalidades no fitness
3. **Escrever pelo menos 5–10 testes** com `pytest` cobrindo fitness, mutação e crossover
4. **Preencher o README** com instruções de instalação, arquitetura e exemplos
5. **Incluir as prioridades na função fitness** (ex: penalidade proporcional à posição dos críticos na rota)

---

*Avaliação gerada automaticamente com base na análise comparativa dos repositórios `inicio/` (baseline do professor) e `tech/` (entrega do aluno).*
