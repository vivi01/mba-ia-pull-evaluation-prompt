"""
Funções auxiliares para o projeto de otimização de prompts.

Responsabilidades:
- Gerenciamento de arquivo YAML e JSON
- Validação de variáveis de ambiente
- Inicialização de LLM com múltiplos providers
- Extração e formatação de respostas
"""

import os
import json
import logging
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional, List

import yaml
from dotenv import load_dotenv

# Configurar logger
logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Providers de LLM suportados."""
    OPENAI = "openai"
    GOOGLE = "google"


class PromptValidator:
    """Valida estrutura de prompts YAML."""
    
    REQUIRED_FIELDS = {"description", "system_prompt", "version"}
    MIN_TECHNIQUES = 2
    
    @staticmethod
    def validate(prompt_data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Valida estrutura básica de um prompt.
        
        Args:
            prompt_data: Dados do prompt a validar
            
        Returns:
            Tupla (é_válido, lista_de_erros)
        """
        errors = []
        
        # Verificar campos obrigatórios
        for field in PromptValidator.REQUIRED_FIELDS:
            if field not in prompt_data:
                errors.append(f"Campo obrigatório faltando: {field}")
        
        # Validar system_prompt
        system_prompt = prompt_data.get("system_prompt", "").strip()
        if not system_prompt:
            errors.append("system_prompt está vazio")
        elif "TODO" in system_prompt:
            errors.append("system_prompt ainda contém TODOs")
        
        # Validar técnicas aplicadas
        techniques = prompt_data.get("techniques_applied", [])
        if not isinstance(techniques, list) or len(techniques) < PromptValidator.MIN_TECHNIQUES:
            errors.append(
                f"Mínimo de {PromptValidator.MIN_TECHNIQUES} técnicas requeridas, "
                f"encontradas: {len(techniques)}"
            )
        
        return (len(errors) == 0, errors)


# Carregar .env apenas uma vez no módulo
load_dotenv()


def load_yaml(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Carrega arquivo YAML com tratamento robusto de erros.

    Args:
        file_path: Caminho do arquivo YAML

    Returns:
        Dicionário com conteúdo do YAML ou None se erro
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        logger.debug(f"YAML carregado com sucesso: {file_path}")
        return data
        
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {file_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Erro ao parsear YAML: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar arquivo: {e}")
        return None


def save_yaml(data: Dict[str, Any], file_path: str) -> bool:
    """
    Salva dados em arquivo YAML com validação de caminho.

    Args:
        data: Dados para salvar
        file_path: Caminho do arquivo de saída

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        output_file = Path(file_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(
                data, 
                f, 
                allow_unicode=True, 
                sort_keys=False, 
                indent=2,
                default_flow_style=False
            )

        logger.info(f"YAML salvo com sucesso: {file_path}")
        return True
        
    except IOError as e:
        logger.error(f"Erro I/O ao salvar arquivo: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao salvar arquivo: {e}")
        return False


def check_env_vars(required_vars: List[str]) -> bool:
    """
    Verifica se variáveis de ambiente obrigatórias estão configuradas.

    Args:
        required_vars: Lista de variáveis obrigatórias

    Returns:
        True se todas configuradas, False caso contrário
    """
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error("Variáveis de ambiente faltando:")
        for var in missing_vars:
            logger.error(f"  - {var}")
        logger.info("Configure-as no arquivo .env antes de continuar.")
        return False

    logger.debug("Todas as variáveis de ambiente necessárias estão configuradas.")
    return True


def format_score(score: float, threshold: float = 0.9) -> str:
    """
    Formata score com indicador visual de status.

    Args:
        score: Score entre 0.0 e 1.0
        threshold: Limite mínimo para aprovação (padrão: 0.9)

    Returns:
        String formatada com score e símbolo de status
    """
    score = max(0.0, min(1.0, score))  # Clamp entre 0 e 1
    symbol = "✓" if score >= threshold else "✗"
    return f"{score:.2f} {symbol}"


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Extrai JSON de uma resposta LLM que pode conter texto adicional.
    
    Estratégia:
    1. Tenta parse direto
    2. Tenta extrair JSON entre chaves
    3. Retorna None se nenhuma estratégia funcionar

    Args:
        response_text: Texto da resposta do LLM

    Returns:
        Dicionário extraído ou None se não encontrar JSON válido
    """
    if not response_text or not isinstance(response_text, str):
        logger.warning("Response text vazia ou não é string")
        return None
    
    # Estratégia 1: Parse direto
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Estratégia 2: Extrair JSON entre chaves
    start = response_text.find("{")
    end = response_text.rfind("}") + 1

    if start != -1 and end > start:
        try:
            json_str = response_text[start:end]
            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.warning(f"JSON inválido encontrado: {json_str[:100]}...")
            pass

    logger.warning(f"Não foi possível extrair JSON válido: {response_text[:200]}...")
    return None


def get_llm(model: Optional[str] = None, temperature: float = 0.0):
    """
    Factory para criar instância de LLM baseado no provider configurado.

    Suporta:
    - OpenAI (ChatOpenAI)
    - Google Gemini (ChatGoogleGenerativeAI)

    Args:
        model: Nome do modelo (usa LLM_MODEL do .env por padrão)
        temperature: Temperatura para geração (0.0 = determinístico)

    Returns:
        Instância de LLM configurada

    Raises:
        ValueError: Se provider não suportado ou credenciais ausentes
    """
    provider_str = os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    try:
        provider = LLMProvider(provider_str)
    except ValueError:
        raise ValueError(
            f"Provider '{provider_str}' não suportado. "
            f"Use: {', '.join(p.value for p in LLMProvider)}"
        )

    if provider == LLMProvider.OPENAI:
        return _create_openai_llm(model_name, temperature)
    elif provider == LLMProvider.GOOGLE:
        return _create_google_llm(model_name, temperature)


def _create_openai_llm(model_name: str, temperature: float):
    """Cria LLM OpenAI com validação de credenciais."""
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY não configurada no .env. "
            "Obtenha uma chave em: https://platform.openai.com/api-keys"
        )

    logger.info(f"Inicializando OpenAI LLM: {model_name}")
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=api_key,
        timeout=60
    )


def _create_google_llm(model_name: str, temperature: float):
    """Cria LLM Google Gemini com validação de credenciais."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY não configurada no .env. "
            "Obtenha uma chave em: https://aistudio.google.com/app/apikey"
        )

    logger.info(f"Inicializando Google Gemini LLM: {model_name}")
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key
    )


def get_eval_llm(temperature: float = 0.0):
    """
    Retorna LLM configurado especificamente para avaliação (usa EVAL_MODEL).
    
    Tipicamente usa modelo mais poderoso para avaliação (ex: gpt-4o vs gpt-4o-mini).

    Args:
        temperature: Temperatura para geração (0.0 = determinístico)

    Returns:
        Instância de LLM configurada para avaliação
    """
    eval_model = os.getenv("EVAL_MODEL", "gpt-4o")
    return get_llm(model=eval_model, temperature=temperature)


# =============================================================================
# Funções de compatibilidade com testes existentes
# =============================================================================

def validate_prompt_structure(prompt_data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    API de compatibilidade com versão anterior para testes.
    
    Delega para PromptValidator.
    
    Args:
        prompt_data: Dados do prompt
        
    Returns:
        Tupla (é_válido, lista_de_erros)
    """
    return PromptValidator.validate(prompt_data)
