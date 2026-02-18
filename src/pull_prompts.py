"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """Attempt to pull the base prompt from LangSmith Hub and save locally.

    Behavior:
    - Requires `LANGSMITH_API_KEY` in env and `LLM_PROVIDER` set (utils.check_env_vars used).
    - Tries to pull `leonanluppi/bug_to_user_story_v1` from the hub.
    - If pull fails, and a local `prompts/bug_to_user_story_v1.yml` exists, copies it to `prompts/raw_prompts.yml`.
    """
    required = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required):
        return False

    prompt_name = os.getenv("PULL_PROMPT_NAME", "leonanluppi/bug_to_user_story_v1")
    dest = "prompts/raw_prompts.yml"

    try:
        print_section_header(f"PULL: {prompt_name}")
        prompt_obj = hub.pull(prompt_name)

        # Try to convert to a serializable structure. If prompt_obj has 'to_dict', prefer it.
        data = None
        if hasattr(prompt_obj, "to_dict"):
            data = prompt_obj.to_dict()
        elif hasattr(prompt_obj, "prompt"):
            data = {"prompt": str(prompt_obj.prompt)}
        else:
            # Fallback: store a small wrapper
            data = {"name": prompt_name, "repr": repr(prompt_obj)}

        saved = save_yaml(data, dest)
        if saved:
            print(f"✓ Prompt salvo em: {dest}")
            return True
        else:
            print("❌ Falha ao salvar prompt puxado")
            return False

    except Exception as e:
        print(f"⚠️  Não foi possível puxar do Hub: {e}")
        # Fallback: try to copy existing v1 file if present
        local_v1 = "prompts/bug_to_user_story_v1.yml"
        try:
            if os.path.exists(local_v1):
                with open(local_v1, "r", encoding="utf-8") as f:
                    content = f.read()
                # Save as raw_prompts.yml
                saved = save_yaml({"source": "local_v1", "content": content}, dest)
                if saved:
                    print(f"✓ Copiado {local_v1} → {dest}")
                    return True
        except Exception:
            pass

        print("Consulte README.md para instruções de configuração do LangSmith e verifique suas credenciais.")
        return False


def main():
    """Função principal"""
    print_section_header("PULL PROMPTS")
    ok = pull_prompts_from_langsmith()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
