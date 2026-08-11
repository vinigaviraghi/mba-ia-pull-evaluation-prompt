# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Este projeto busca um prompt-base do LangSmith Hub, publica uma versão otimizada e avalia a conversão de relatos de bugs em User Stories.

## Técnicas Aplicadas (Fase 2)

| Técnica | Aplicação | Motivo |
| --- | --- | --- |
| Few-shot Learning | Dois pares de relato e User Story foram incluídos no prompt de sistema. | Estabelece o formato e o nível de detalhe esperados. |
| Role Prompting | O modelo recebe a persona de Product Manager sênior. | Direciona a saída para valor do usuário e critérios verificáveis. |
| Skeleton of Thought | O prompt orienta a estruturar internamente usuário, contexto, evento e resultado antes de escrever. | Reduz omissões sem expor raciocínio interno na resposta. |

A versão v2 exige Markdown, a estrutura “Como um/uma..., eu quero..., para que...” e de três a cinco critérios Gherkin. Ela também proíbe a invenção de fatos e define como tratar relatos incompletos.

## Pré-requisitos

- Python 3.9 ou superior (recomendado: Python 3.11 para as versões fixadas das dependências)
- Conta e API key do LangSmith
- Uma chave de OpenAI ou Google Gemini

Crie `.env` a partir de `.env.example` e informe, no mínimo:

```dotenv
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=prompt-optimization-challenge
USERNAME_LANGSMITH_HUB=seu_usuario
LLM_PROVIDER=google
GOOGLE_API_KEY=...
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

Para OpenAI, configure `LLM_PROVIDER=openai`, `OPENAI_API_KEY`, `LLM_MODEL=gpt-4o-mini` e `EVAL_MODEL=gpt-4o`.

## Como Executar

```bash
/usr/local/bin/python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Validação local e sem chamadas remotas
pytest tests/test_prompts.py -v

# Busca o prompt inicial e o serializa em prompts/bug_to_user_story_v1.yml
python src/pull_prompts.py

# Publica publicamente <USERNAME_LANGSMITH_HUB>/bug_to_user_story_v2
python src/push_prompts.py

# Cria/usa o dataset com 15 exemplos e exibe as cinco métricas
python src/evaluate.py

```

Após cada avaliação, ajuste `prompts/bug_to_user_story_v2.yml`, faça novo push e reexecute a avaliação. A aprovação requer Helpfulness, Correctness, F1-Score, Clarity e Precision individualmente maiores ou iguais a 0,8.

## Resultados Finais

==================================================
AVALIAÇÃO DE PROMPTS OTIMIZADOS
==================================================

Provider: openai
Modelo Principal: gpt-4o-mini
Modelo de Avaliação: gpt-4o

Criando dataset de avaliação: default-eval...
   ✓ Carregados 15 exemplos do arquivo datasets/bug_to_user_story.jsonl
   ✓ Dataset 'default-eval' já existe, usando existente

======================================================================
PROMPTS PARA AVALIAR
======================================================================

Este script irá puxar prompts do LangSmith Hub.
Certifique-se de ter feito push dos prompts antes de avaliar:
  python src/push_prompts.py


🔍 Avaliando: fullcycle-myfirstprompt/bug_to_user_story_v2
   Puxando prompt do LangSmith Hub: fullcycle-myfirstprompt/bug_to_user_story_v2
   ✓ Prompt carregado com sucesso
   Dataset: 15 exemplos
   Avaliando exemplos...
      [1/15] F1:0.85 Clarity:0.90 Precision:0.90
      [2/15] F1:0.75 Clarity:0.90 Precision:0.90
      [3/15] F1:0.75 Clarity:0.90 Precision:0.90
      [4/15] F1:0.69 Clarity:0.85 Precision:0.90
      [5/15] F1:0.55 Clarity:0.85 Precision:0.67
      [6/15] F1:0.75 Clarity:0.90 Precision:0.90
      [7/15] F1:1.00 Clarity:1.00 Precision:1.00
      [8/15] F1:0.75 Clarity:0.90 Precision:0.90
      [9/15] F1:0.80 Clarity:0.85 Precision:0.83
      [10/15] F1:0.69 Clarity:0.80 Precision:0.67
      [11/15] F1:1.00 Clarity:0.90 Precision:0.90
      [12/15] F1:0.80 Clarity:0.80 Precision:0.90
      [13/15] F1:1.00 Clarity:0.95 Precision:1.00
      [14/15] F1:1.00 Clarity:1.00 Precision:1.00
      [15/15] F1:1.00 Clarity:0.90 Precision:0.67

==================================================
Prompt: fullcycle-myfirstprompt/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.88 ✓
  - Correctness: 0.85 ✓

Métricas Base:
  - F1-Score: 0.82 ✓
  - Clarity: 0.89 ✓
  - Precision: 0.87 ✓

--------------------------------------------------
📊 MÉDIA GERAL: 0.8627
--------------------------------------------------

✅ STATUS: APROVADO - Todas as métricas >= 0.8

==================================================
RESUMO FINAL
==================================================

Prompts avaliados: 1
Aprovados: 1
Reprovados: 0

✅ Todos os prompts atingiram todas as métricas >= 0.8!


## Evidências Visuais

Adicione as capturas do LangSmith na pasta `docs/images/` com os nomes abaixo. Os links serão renderizados no GitHub após os arquivos serem incluídos.

- [Resultado final da avaliação](docs/images/langsmith-evaluation-approved.png)
- [Experiment no LangSmith](docs/images/langsmith-experiment.png)
- [Traces de execução](docs/images/langsmith-traces.png)
