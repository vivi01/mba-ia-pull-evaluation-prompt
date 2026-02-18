"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        print_section_header(f"PUSH: {prompt_name}")

        is_valid, errors = validate_prompt(prompt_data)
        if not is_valid:
            print("❌ Prompt inválido:")
            for e in errors:
                print(f"  - {e}")
            return False

        # Convert YAML data to ChatPromptTemplate
        try:
            system_prompt = prompt_data.get("system_prompt", "")
            
            # Create a ChatPromptTemplate with the system prompt and bug_report input variable
            chat_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{bug_report}")
            ])
            
            # Add metadata to the template
            chat_template.metadata = {
                "description": prompt_data.get("description", ""),
                "version": prompt_data.get("version", ""),
                "techniques_applied": prompt_data.get("techniques_applied", []),
                "few_shot_examples": prompt_data.get("few_shot_examples", []),
                "notes": prompt_data.get("notes", "")
            }
            
            # Push to LangChain hub
            hub.push(prompt_name, chat_template)
            print(f"✓ Prompt publicado: {prompt_name}")
            return True
        except Exception as e:
            print(f"⚠️  Não foi possível publicar automaticamente: {e}")
            print("Instrua manualmente: abra https://smith.langchain.com/prompts e crie um novo prompt público com o YAML.")
            return False

    except Exception as e:
        print(f"❌ Erro no push: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []
    if not isinstance(prompt_data, dict):
        return False, ["prompt_data deve ser um dicionário"]

    # Basic required fields
    required = ["description", "system_prompt", "version", "techniques_applied"]
    for r in required:
        if r not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {r}")

    # techniques_applied must be a list with at least 2 entries
    tech = prompt_data.get("techniques_applied", [])
    if not isinstance(tech, list) or len(tech) < 2:
        errors.append("Campo 'techniques_applied' deve conter pelo menos 2 técnicas")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH PROMPT")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    prompt_path = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(prompt_path)
    if not data:
        print(f"❌ Não foi possível carregar: {prompt_path}")
        return 1

    prompt_name = os.getenv("PUSH_PROMPT_NAME", "Viviane Pereira/bug_to_user_story_v2")

    success = push_prompt_to_langsmith(prompt_name, data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
