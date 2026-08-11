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
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """Baixa o prompt-base do Hub e o grava no formato YAML do projeto."""
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = "prompts/bug_to_user_story_v1.yml"

    try:
        print(f"Baixando prompt: {prompt_name}")
        prompt = hub.pull(prompt_name)

        if not isinstance(prompt, ChatPromptTemplate):
            raise TypeError(
                "O prompt obtido não é um ChatPromptTemplate e não pode ser "
                "convertido para o formato YAML esperado."
            )

        system_prompt = ""
        user_prompt = ""
        for message in prompt.messages:
            template = getattr(getattr(message, "prompt", None), "template", "")
            message_type = message.__class__.__name__.lower()
            if "system" in message_type:
                system_prompt = template
            elif "human" in message_type or "user" in message_type:
                user_prompt = template

        if not system_prompt or not user_prompt:
            raise ValueError("O prompt do Hub não contém mensagens system e user válidas.")

        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt original obtido do LangSmith Prompt Hub",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "source": prompt_name,
                "tags": ["bug-analysis", "user-story", "baseline"],
            }
        }

        if not save_yaml(prompt_data, output_path):
            return False

        print(f"✓ Prompt salvo em: {output_path}")
        return True
    except Exception as error:
        print(f"❌ Não foi possível fazer pull de '{prompt_name}': {error}")
        return False


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPT DO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    return 0 if pull_prompts_from_langsmith() else 1


if __name__ == "__main__":
    sys.exit(main())
