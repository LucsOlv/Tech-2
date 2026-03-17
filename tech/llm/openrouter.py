"""
Cliente para a API do OpenRouter.
Envia dados de rotas VRP para uma LLM e retorna instruções detalhadas.
"""

import os
import requests
import streamlit as st
from dotenv import load_dotenv

from .prompts import SYSTEM_PROMPT, build_route_prompt

# Carrega arquivos .env
load_dotenv()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-2.0-flash-001"


def _get_api_key() -> str | None:
    """Busca a chave da API em st.secrets ou variáveis de ambiente."""
    # Tenta st.secrets primeiro (para deploy no Streamlit Cloud)
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    # Fallback para variável de ambiente
    return os.environ.get("OPENROUTER_API_KEY")


def generate_route_report(
    veiculos_data: list[dict],
    model: str = DEFAULT_MODEL,
) -> str:
    """
    Envia os dados das rotas otimizadas para o OpenRouter e retorna o
    relatório/cronograma gerado pela LLM.

    Args:
        veiculos_data: Lista de dicts com dados de cada veículo.
        model: Modelo a usar no OpenRouter.

    Returns:
        Texto markdown com as instruções geradas pela LLM.

    Raises:
        ValueError: Se a chave da API não estiver configurada.
        requests.HTTPError: Se a requisição falhar.
    """
    api_key = _get_api_key()
    if not api_key:
        raise ValueError(
            "Chave da API OpenRouter não encontrada. "
            "Configure OPENROUTER_API_KEY em .streamlit/secrets.toml ou como variável de ambiente."
        )

    user_prompt = build_route_prompt(veiculos_data)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/fiap-tech-challenge",
        "X-Title": "VRP Route Optimizer",
    }

    response = requests.post(
        OPENROUTER_API_URL,
        json=payload,
        headers=headers,
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]
