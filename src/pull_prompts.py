"""
Script para hacer pull de prompts do LangSmith Prompt Hub.

Responsabilidades:
- Conectar ao LangSmith usando credenciais do .env
- Fazer pull dos prompts do Hub
- Salvar localmente em prompts/

Estratégia de Fallback:
- Se pull do Hub falhar, usa arquivo local como fallback
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from langchain import hub

from utils import check_env_vars, save_yaml

# Configurar logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


class PromptPuller:
    """Responsável por fazer pull e salvar prompts do LangSmith Hub."""
    
    def __init__(self, prompt_name: str, output_path: str):
        """
        Inicializa o PullPrompts.
        
        Args:
            prompt_name: Nome do prompt no Hub
            output_path: Caminho de saída para salvar localmente
        """
        self.prompt_name = prompt_name
        self.output_path = output_path
    
    def pull_from_hub(self) -> bool:
        """
        Faz pull do prompt do LangSmith Hub.
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            logger.info(f"Puxando prompt do Hub: {self.prompt_name}")
            prompt_obj = hub.pull(self.prompt_name)
            
            # Converter para estrutura serializável
            data = self._serialize_prompt(prompt_obj, self.prompt_name)
            
            if save_yaml(data, self.output_path):
                logger.info(f"✓ Prompt salvo em: {self.output_path}")
                return True
            else:
                logger.error("Falha ao salvar prompt puxado")
                return False
                
        except (ImportError, RuntimeError, FileNotFoundError) as e:
            logger.error(f"Não foi possível puxar do Hub: {e}")
            return False
    
    def _serialize_prompt(self, prompt_obj: Any, prompt_name: str) -> Dict[str, Any]:
        """
        Converte objeto de prompt para estrutura serializável.
        
        Args:
            prompt_obj: Objeto do prompt retornado pelo hub
            prompt_name: Nome do prompt (para referência)
            
        Returns:
            Dicionário com dados do prompt
        """
        # Tentar extrair conforme o tipo de objeto
        if hasattr(prompt_obj, "to_dict"):
            return prompt_obj.to_dict()
        elif hasattr(prompt_obj, "prompt"):
            return {"prompt": str(prompt_obj.prompt)}
        else:
            return {
                "name": prompt_name,
                "representation": repr(prompt_obj),
                "note": "Prompt importado do LangSmith Hub"
            }
    
    def use_local_fallback(self, local_path: str) -> bool:
        """
        Usa arquivo local como fallback se pull falhar.
        
        Args:
            local_path: Caminho do arquivo local
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            if not Path(local_path).exists():
                logger.warning(f"Arquivo local não existe: {local_path}")
                return False
            
            logger.info(f"Usando fallback local: {local_path}")
            with open(local_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            data = {
                "source": "local_fallback",
                "original_file": local_path,
                "content": content
            }
            
            if save_yaml(data, self.output_path):
                logger.info(f"✓ Fallback salvo em: {self.output_path}")
                return True
            
            logger.error("Falha ao salvar fallback local")
            return False
            
        except (FileNotFoundError, IOError, OSError) as e:
            logger.error(f"Erro ao usar fallback local: {e}")
            return False


def main() -> int:
    """
    Função principal - orquestra o pull de prompts.
    
    Returns:
        0 se sucesso, 1 se erro
    """
    logger.info("=" * 70)
    logger.info("PULL PROMPTS")
    logger.info("=" * 70 + "\n")
    
    # Verificar variáveis obrigatórias
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1
    
    # Configurar parâmetros
    prompt_name = os.getenv("PULL_PROMPT_NAME", "leonanluppi/bug_to_user_story_v1")
    output_path = "prompts/raw_prompts.yml"
    local_fallback = "prompts/bug_to_user_story_v1.yml"
    
    # Executar pull
    puller = PromptPuller(prompt_name, output_path)
    
    if puller.pull_from_hub():
        return 0
    
    # Tentar fallback local se pull falhou
    logger.warning("\nTentando usar arquivo local como fallback...")
    if puller.use_local_fallback(local_fallback):
        return 0
    
    logger.error("\n❌ Falha total: Hub indisponível e sem fallback local")
    logger.info(
        "\nResolução:\n"
        "1. Verifique LANGSMITH_API_KEY no .env\n"
        "2. Certifique-se de que o arquivo local existe\n"
        "3. Consulte README.md para instruções completas"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
