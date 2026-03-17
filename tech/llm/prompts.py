"""
Templates de prompt para interpretação de rotas VRP via LLM.
"""

SYSTEM_PROMPT = """Você é um coordenador logístico especializado em distribuição hospitalar.
Sua função é analisar rotas otimizadas de entrega de medicamentos e insumos médicos
e gerar instruções claras e detalhadas para cada motorista da frota.

Regras:
- Seja objetivo e direto nas instruções.
- Destaque entregas CRÍTICAS com ⚠️ e instrua o motorista a priorizá-las.
- Estime horários de chegada a partir do horário de partida (07:00).
- Inclua dicas operacionais úteis (ex: verificar temperatura de medicamentos refrigerados).
- Formate a resposta em Markdown estruturado, com seções por veículo.
- Responda sempre em português brasileiro.
"""


def build_route_prompt(veiculos_data: list[dict]) -> str:
    """
    Constrói o prompt do usuário com os dados processados de cada veículo.

    Cada item de veiculos_data deve conter:
        - veiculo_id: int
        - destinos: list[dict] com {coordenada, endereco, ordem, is_critico}
        - distancia_km: float
        - tempo_estimado_min: float
        - num_paradas: int
    """
    linhas = [
        "Aqui estão as rotas otimizadas pelo algoritmo genético para entrega de medicamentos.\n",
        f"**Total de veículos:** {len(veiculos_data)}\n",
    ]

    for v in veiculos_data:
        linhas.append(f"### Veículo {v['veiculo_id']}")
        linhas.append(f"- **Paradas:** {v['num_paradas']}")
        linhas.append(f"- **Distância total:** {v['distancia_km']:.2f} km")
        linhas.append(f"- **Tempo estimado:** {v['tempo_estimado_min']:.0f} min")
        linhas.append("- **Itinerário:**")

        for d in v["destinos"]:
            critico = " ⚠️ CRÍTICO" if d["is_critico"] else ""
            linhas.append(
                f"  {d['ordem']}. {d['endereco']} ({d['coordenada'][0]:.5f}, {d['coordenada'][1]:.5f}){critico}"
            )
        linhas.append("")

    linhas.append(
        "Para cada veículo, gere um cronograma detalhado com:\n"
        "1. Horário estimado de partida e chegada em cada parada (partida às 07:00)\n"
        "2. Prioridades de entrega (destinos críticos primeiro)\n"
        "3. Instruções operacionais para o motorista\n"
        "4. Um resumo final de eficiência da rota"
    )

    return "\n".join(linhas)
