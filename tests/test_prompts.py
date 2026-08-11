"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    prompt_file = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

    def prompt(self):
        document = load_prompts(self.prompt_file)
        assert "bug_to_user_story_v2" in document
        return document["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert self.prompt()["system_prompt"].strip()

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt()["system_prompt"].lower()
        assert "você é" in system_prompt
        assert "product manager" in system_prompt

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        text = self.prompt()["system_prompt"].lower()
        assert "markdown" in text
        assert "como um" in text
        assert "critérios de aceitação" in text

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        examples = self.prompt().get("few_shot_examples", [])
        assert len(examples) >= 2
        assert all(example.get("input") and example.get("output") for example in examples)

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = self.prompt()
        text = " ".join(str(value) for value in prompt.values()).upper()
        assert "[TODO]" not in text

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt().get("techniques_applied", [])
        assert len(techniques) >= 2
        valid, errors = validate_prompt_structure(self.prompt())
        assert valid, errors

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
