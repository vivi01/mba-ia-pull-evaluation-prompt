# Tarefas Temporárias - Verificação Rápida (base: desafio.md)

Lista de tarefas para validar o repositório e o pipeline. Atualizarei cada item após execução.

 - [x] 1) Testes unitários: `pytest tests/test_prompts.py` (6 testes)
 - [x] 2) Verificar estrutura de prompts: `prompts/bug_to_user_story_v1.yml` e `prompts/bug_to_user_story_v2.yml`
 - [x] 3) Pull script: `python src/pull_prompts.py` (deve usar fallback local se LANGSMITH não configurado) — OK (prompts/raw_prompts.yml criado)
- [ ] 4) Push script: `python src/push_prompts.py` (valida YAML e tenta publicar)
- [ ] 5) Pipeline de avaliação: `python src/evaluate.py` (cria dataset e executa métricas)
- [ ] 6) Multi-provider support: validar `config_provider.py` e variáveis `LLM_PROVIDER`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`
- [ ] 7) README: contém 3 seções obrigatórias (Técnicas Aplicadas, Resultados Finais, Instruções de Execução)
- [ ] 8) Dataset: `datasets/bug_to_user_story.jsonl` presente e legível
- [ ] 9) LLM factory: `get_llm` e `get_eval_llm` funcionando (sem chamadas externas quando apenas importadas)
- [ ] 10) Relatório de refatoração: `REFACTORING_REPORT.md` criado


Notas:
- Alguns passos dependem de chaves de API externas (LangSmith / OpenAI / Google). Quando ausentes, marcarei como "Skipped - missing credentials" e destacarei como reproduzir localmente.
