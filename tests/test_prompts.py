"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path as P

# Adicionar src ao path
sys.path.insert(0, str(P(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        path = P(__file__).parents[1] / "prompts" / "bug_to_user_story_v2.yml"
        data = load_prompts(str(path))
        assert data is not None
        assert "system_prompt" in data and str(data["system_prompt"]).strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        path = P(__file__).parents[1] / "prompts" / "bug_to_user_story_v2.yml"
        data = load_prompts(str(path))
        system = data.get("system_prompt", "")
        assert "Você é" in system or "Você é um" in system or "Product Manager" in system

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        path = P(__file__).parents[1] / "prompts" / "bug_to_user_story_v2.yml"
        data = load_prompts(str(path))
        system = data.get("system_prompt", "").lower()
        assert "markdown" in system or "user story" in system

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        path = P(__file__).parents[1] / "prompts" / "bug_to_user_story_v2.yml"
        data = load_prompts(str(path))
        examples = data.get("few_shot_examples") or data.get("few_shot") or []
        assert isinstance(examples, list) and len(examples) >= 1

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        path = P(__file__).parents[1] / "prompts" / "bug_to_user_story_v2.yml"
        text = open(path, 'r', encoding='utf-8').read()
        assert "TODO" not in text and "[TODO]" not in text

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        path = P(__file__).parents[1] / "prompts" / "bug_to_user_story_v2.yml"
        data = load_prompts(str(path))
        tech = data.get("techniques_applied", [])
        assert isinstance(tech, list) and len(tech) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])