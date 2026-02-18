#!/usr/bin/env python3
"""
Script para configurar o provider de LLM (OpenAI ou Google Gemini).

Uso:
    python config_provider.py openai sk-...
    python config_provider.py google AIzaSy...
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def update_env_file(provider: str, api_key: str):
    """
    Atualiza o arquivo .env com o provider e chave API.
    
    Args:
        provider: 'openai' ou 'google'
        api_key: Chave de API do provider
    """
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ Arquivo .env não encontrado!")
        return False
    
    # Ler arquivo atual
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Atualizar linhas
    new_lines = []
    provider_found = False
    openai_key_found = False
    google_key_found = False
    
    for line in lines:
        if line.startswith("LLM_PROVIDER="):
            new_lines.append(f"LLM_PROVIDER={provider}\n")
            provider_found = True
        elif provider == "openai" and line.startswith("OPENAI_API_KEY="):
            new_lines.append(f'OPENAI_API_KEY="{api_key}"\n')
            openai_key_found = True
        elif provider == "google" and line.startswith("GOOGLE_API_KEY="):
            new_lines.append(f'GOOGLE_API_KEY="{api_key}"\n')
            google_key_found = True
        else:
            new_lines.append(line)
    
    # Escrever arquivo atualizado
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    # Mensagem de sucesso
    print(f"✅ Configuração atualizada com sucesso!")
    print(f"   Provider: {provider}")
    print(f"   API Key: {api_key[:20]}...")
    print()
    print("📝 Configure em .env:")
    if provider == "openai":
        print(f"   LLM_PROVIDER=openai")
        print(f"   LLM_MODEL=gpt-4o-mini")
        print(f"   EVAL_MODEL=gpt-4o")
    else:
        print(f"   LLM_PROVIDER=google")
        print(f"   LLM_MODEL=gemini-2.5-flash")
        print(f"   EVAL_MODEL=gemini-2.5-flash")
    
    return True


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Uso: python config_provider.py <provider> <api_key>")
        print()
        print("Exemplos:")
        print("  python config_provider.py openai sk-...")
        print("  python config_provider.py google AIzaSy...")
        print()
        print("Para obter chaves:")
        print("  OpenAI: https://platform.openai.com/api-keys")
        print("  Google Gemini: https://aistudio.google.com/app/apikey")
        return 1
    
    provider = sys.argv[1].lower()
    api_key = sys.argv[2]
    
    if provider not in ["openai", "google"]:
        print(f"❌ Provider inválido: {provider}")
        print("Escolha entre: openai, google")
        return 1
    
    if not api_key:
        print("❌ API Key não pode estar vazia!")
        return 1
    
    return 0 if update_env_file(provider, api_key) else 1


if __name__ == "__main__":
    sys.exit(main())
