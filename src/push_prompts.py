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
        metadata = {
            "description": prompt_data["description"],
            "tags": prompt_data.get("tags", []),
            "techniques_applied": prompt_data.get("techniques_applied", []),
            "version": prompt_data["version"],
        }
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"]),
        ])
        prompt.metadata = metadata

        hub.push(
            prompt_name,
            prompt,
            new_repo_is_public=True,
            new_repo_description=prompt_data["description"],
            tags=metadata["tags"],
        )
        print(f"✓ Prompt público publicado: {prompt_name}")
        print(f"  Técnicas: {', '.join(metadata['techniques_applied'])}")
        return True
    except Exception as error:
        print(f"❌ Não foi possível publicar '{prompt_name}': {error}")
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
    required_fields = ["description", "system_prompt", "user_prompt", "version"]
    for field in required_fields:
        if not str(prompt_data.get(field, "")).strip():
            errors.append(f"Campo obrigatório ausente ou vazio: {field}")

    techniques = prompt_data.get("techniques_applied", [])
    if not isinstance(techniques, list) or len(techniques) < 2:
        errors.append("São necessárias ao menos duas técnicas em techniques_applied.")

    examples = prompt_data.get("few_shot_examples", [])
    if not isinstance(examples, list) or not examples:
        errors.append("O prompt deve declarar ao menos um exemplo few-shot.")

    combined_text = " ".join(
        str(prompt_data.get(key, "")) for key in ("system_prompt", "user_prompt")
    )
    if "[TODO]" in combined_text.upper():
        errors.append("O prompt contém [TODO].")

    return (not errors, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPT PARA O LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    document = load_yaml("prompts/bug_to_user_story_v2.yml")
    if not document or "bug_to_user_story_v2" not in document:
        print("❌ Estrutura inválida em prompts/bug_to_user_story_v2.yml")
        return 1

    prompt_data = document["bug_to_user_story_v2"]
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ O prompt não passou na validação:")
        for error in errors:
            print(f"  - {error}")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/bug_to_user_story_v2"
    return 0 if push_prompt_to_langsmith(prompt_name, prompt_data) else 1


if __name__ == "__main__":
    sys.exit(main())
