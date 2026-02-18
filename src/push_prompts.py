"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Responsabilidades:
- Ler prompts otimizados do YAML
- Validar estrutura de prompts
- Converter para ChatPromptTemplate
- Fazer push com versionagem e metadados
- Suportar múltiplos providers de LLM

Requisito de Segurança:
- Prompts são publicados PUBLICAMENTE no Hub
- Não incluir dados sensíveis ou chaves de API
"""

import os
import sys
import logging
from typing import Dict, Any, Tuple, List

from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

from utils import load_yaml, check_env_vars

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


class PromptValidator:
    """Valida estrutura de prompts antes do push."""
    
    REQUIRED_FIELDS = {"description", "system_prompt", "version", "techniques_applied"}
    MIN_TECHNIQUES = 2
    
    @staticmethod
    def validate(prompt_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida estrutura de prompt YAML.
        
        Args:
            prompt_data: Dados do prompt a validar
            
        Returns:
            Tupla (é_válido, lista_de_erros)
        """
        errors = []
        
        if not isinstance(prompt_data, dict):
            return False, ["prompt_data deve ser um dicionário"]
        
        # Verificar campos obrigatórios
        for field in PromptValidator.REQUIRED_FIELDS:
            if field not in prompt_data:
                errors.append(f"Campo obrigatório faltando: {field}")
        
        # Validar técnicas
        techniques = prompt_data.get("techniques_applied", [])
        if not isinstance(techniques, list) or len(techniques) < PromptValidator.MIN_TECHNIQUES:
            errors.append(
                f"Campo 'techniques_applied' deve conter pelo menos "
                f"{PromptValidator.MIN_TECHNIQUES} técnicas"
            )
        
        # Validar system_prompt não está vazio
        system_prompt = prompt_data.get("system_prompt", "").strip()
        if not system_prompt:
            errors.append("system_prompt está vazio")
        
        return (len(errors) == 0, errors)


class PromptPusher:
    """Responsável por fazer push de prompts ao LangSmith Hub."""
    
    def __init__(self, prompt_name: str, prompt_data: Dict[str, Any]):
        """
        Inicializa o PushPrompts.
        
        Args:
            prompt_name: Nome para publish no Hub (ex: "username/prompt_name_v2")
            prompt_data: Dados do prompt YAML
        """
        self.prompt_name = prompt_name
        self.prompt_data = prompt_data
    
    def push(self) -> bool:
        """
        Faz push do prompt para LangSmith Hub.
        
        Returns:
            True se sucesso, False caso contrário
        """
        logger.info(f"Iniciando push: {self.prompt_name}")
        
        # Validar prompt
        is_valid, errors = PromptValidator.validate(self.prompt_data)
        if not is_valid:
            logger.error("Prompt inválido:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        try:
            # Criar ChatPromptTemplate
            chat_template = self._create_chat_template()
            
            # Fazer push
            hub.push(self.prompt_name, chat_template)
            logger.info(f"✓ Prompt publicado com sucesso: {self.prompt_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao fazer push: {e}")
            logger.warning("Verifique LANGSMITH_API_KEY no .env")
            return False
    
    def _create_chat_template(self) -> ChatPromptTemplate:
        """
        Cria ChatPromptTemplate a partir dos dados YAML.
        
        Returns:
            ChatPromptTemplate configurado com metadados
        """
        system_prompt = self.prompt_data.get("system_prompt", "")
        
        # Criar template com sistema e entrada de usuário
        chat_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{bug_report}")  # Variável de entrada
        ])
        
        # Adicionar metadados (preserved no Hub)
        chat_template.metadata = {
            "description": self.prompt_data.get("description", ""),
            "version": self.prompt_data.get("version", ""),
            "techniques_applied": self.prompt_data.get("techniques_applied", []),
            "few_shot_examples": self.prompt_data.get("few_shot_examples", []),
            "notes": self.prompt_data.get("notes", "")
        }
        
        logger.debug(f"ChatPromptTemplate criado com metadados")
        return chat_template


def main() -> int:
    """
    Função principal - orquestra push de prompts.
    
    Returns:
        0 se sucesso, 1 se erro
    """
    logger.info("=" * 70)
    logger.info("PUSH PROMPT - PUBLICAR NO LANGSMITH HUB")
    logger.info("=" * 70 + "\n")
    
    # Verificar variáveis obrigatórias
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1
    
    # Configurar parâmetros
    prompt_path = "prompts/bug_to_user_story_v2.yml"
    prompt_name = os.getenv(
        "PUSH_PROMPT_NAME", 
        "Viviane Pereira/bug_to_user_story_v2"
    )
    
    # Carregar YAML
    logger.info(f"Carregando prompt: {prompt_path}")
    prompt_data = load_yaml(prompt_path)
    if not prompt_data:
        logger.error(f"Falha ao carregar: {prompt_path}")
        return 1
    
    logger.info(f"✓ Prompt carregado com sucesso")
    
    # Fazer push
    pusher = PromptPusher(prompt_name, prompt_data)
    success = pusher.push()
    
    if success:
        logger.info(
            f"\n✓ Pronto! Acesse seu prompt em:\n"
            f"  https://smith.langchain.com/prompts"
        )
        return 0
    else:
        logger.error("\n❌ Falha ao publicar prompt")
        logger.info(
            "Passos para resolver:\n"
            "1. Verifique LANGSMITH_API_KEY no .env\n"
            "2. Valide estrutura do YAML\n"
            "3. Consulte README.md para instruções completas"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
