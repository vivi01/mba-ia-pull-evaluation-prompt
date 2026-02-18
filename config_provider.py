#!/usr/bin/env python3
"""
Script para configurar o provider de LLM (OpenAI ou Google Gemini).

Permite alternar entre providers de forma simples atualizando o arquivo .env

Uso:
    python config_provider.py openai sk-proj-xxxxx
    python config_provider.py google AIzaSyxxxxx

Requisitos de Segurança:
- Chaves de API são armazenadas em .env (nunca fazer commit)
- .env está no .gitignore
"""

import os
import sys
import logging
from pathlib import Path
from typing import Tuple
from enum import Enum

from dotenv import load_dotenv

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

load_dotenv()


class LLMProvider(Enum):
    """Providers de LLM suportados."""
    OPENAI = "openai"
    GOOGLE = "google"
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Verifica se provider é válido."""
        return value.lower() in [p.value for p in cls]
    
    @classmethod
    def get_default_models(cls, provider: str) -> Tuple[str, str]:
        """
        Retorna modelos padrão para um provider.
        
        Returns:
            Tupla (LLM_MODEL, EVAL_MODEL)
        """
        models = {
            LLMProvider.OPENAI.value: ("gpt-4o-mini", "gpt-4o"),
            LLMProvider.GOOGLE.value: ("gemini-2.5-flash", "gemini-2.5-flash")
        }
        return models.get(provider, ("gpt-4o-mini", "gpt-4o"))


class EnvConfigManager:
    """Gerencia configuração do arquivo .env."""
    
    def __init__(self, env_path: str = ".env"):
        """
        Inicializa o gerenciador.
        
        Args:
            env_path: Caminho do arquivo .env
        """
        self.env_path = Path(env_path)
    
    def validate_exists(self) -> bool:
        """
        Valida que o arquivo .env existe.
        
        Returns:
            True se existe, False caso contrário
        """
        if not self.env_path.exists():
            logger.error(f"Arquivo não encontrado: {self.env_path}")
            logger.info("Execute setup do projeto primeiro (venv, pip install, etc)")
            return False
        return True
    
    def update_provider(self, provider: str, api_key: str) -> bool:
        """
        Atualiza arquivo .env com novo provider e chave de API.
        
        Args:
            provider: 'openai' ou 'google'
            api_key: Chave de API
            
        Returns:
            True se sucesso, False caso contrário
        """
        if not self.validate_exists():
            return False
        
        try:
            # Ler arquivo atual
            with open(self.env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Processar linhas
            new_lines = []
            for line in lines:
                if line.startswith("LLM_PROVIDER="):
                    new_lines.append(f"LLM_PROVIDER={provider}\n")
                elif provider == "openai" and line.startswith("OPENAI_API_KEY="):
                    new_lines.append(f'OPENAI_API_KEY="{api_key}"\n')
                elif provider == "google" and line.startswith("GOOGLE_API_KEY="):
                    new_lines.append(f'GOOGLE_API_KEY="{api_key}"\n')
                else:
                    new_lines.append(line)
            
            # Salvar arquivo atualizado
            with open(self.env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            
            return True
            
        except IOError as e:
            logger.error(f"Erro I/O ao atualizar .env: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return False


def display_success(provider: str, api_key: str) -> None:
    """Exibe mensagem de sucesso com configuração."""
    logger.info(f"✓ Configuração atualizada com sucesso!")
    logger.info(f"  Provider: {provider}")
    logger.info(f"  API Key: {api_key[:25]}..." if len(api_key) > 25 else f"  API Key: {api_key}")
    
    # Obter modelos padrão
    llm_model, eval_model = LLMProvider.get_default_models(provider)
    
    logger.info("\nModelos padrão configurados no .env:")
    logger.info(f"  LLM_MODEL={llm_model}")
    logger.info(f"  EVAL_MODEL={eval_model}")
    
    logger.info("\nProximo passo:")
    logger.info(f"  python src/evaluate.py")


def display_usage() -> None:
    """Exibe instruções de uso."""
    logger.info("Uso: python config_provider.py <provider> <api_key>\n")
    
    logger.info("Exemplos:")
    logger.info("  python config_provider.py openai sk-proj-xxxxxx")
    logger.info("  python config_provider.py google AIzaSyxxxxxx\n")
    
    logger.info("Para obter chaves de API:")
    logger.info("  OpenAI: https://platform.openai.com/api-keys")
    logger.info("  Google: https://aistudio.google.com/app/apikey")


def main() -> int:
    """
    Função principal.
    
    Returns:
        0 se sucesso, 1 se erro
    """
    # Validar argumentos
    if len(sys.argv) < 3:
        display_usage()
        return 1
    
    provider = sys.argv[1].lower()
    api_key = sys.argv[2]
    
    # Validar provider
    if not LLMProvider.is_valid(provider):
        logger.error(f"Provider inválido: {provider}")
        logger.info(f"Escolha entre: {', '.join(p.value for p in LLMProvider)}")
        return 1
    
    # Validar API key
    if not api_key or len(api_key) < 10:
        logger.error("API Key inválida ou muito curta")
        return 1
    
    # Atualizar .env
    manager = EnvConfigManager()
    if not manager.update_provider(provider, api_key):
        logger.error("Falha ao atualizar arquivo .env")
        return 1
    
    # Exibir sucesso
    display_success(provider, api_key)
    return 0


if __name__ == "__main__":
    sys.exit(main())
