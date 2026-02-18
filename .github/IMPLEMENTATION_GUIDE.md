# Guia de Implementação Técnica

## 1. Scripts de Integração (src/)
- [cite_start]**src/pull_prompts.py**: Deve utilizar `langchain.hub.pull` para baixar o prompt original e salvá-lo em `prompts/bug_to_user_story_v1.yml`[cite: 45, 68, 70].
- **src/push_prompts.py**: Deve ler `prompts/bug_to_user_story_v2.yml` e usar `langchain.hub.push` para enviar ao LangSmith. [cite_start]Deve incluir metadados como tags e descrição das técnicas utilizadas[cite: 93, 95, 96, 101].
- [cite_start]**src/evaluate.py**: Deve utilizar o dataset de 15 bugs fornecido e a função `evaluate` do LangSmith para gerar o relatório de métricas[cite: 47, 142, 144].

## 2. Estrutura do Prompt Otimizado (YAML)
[cite_start]O arquivo `prompts/bug_to_user_story_v2.yml` deve seguir estas regras[cite: 84, 85, 86, 89]:
- Utilizar distinção clara entre **System Prompt** e **User Prompt**.
- [cite_start]Definir uma **Persona** clara (Role Prompting)[cite: 82].
- [cite_start]Incluir exemplos de entrada e saída (**Few-shot Learning**)[cite: 77, 87].
- [cite_start]Implementar **Chain of Thought (CoT)** para análise do bug[cite: 78, 181].
- [cite_start]Definir regras explícitas para tratamento de casos de borda (edge cases)[cite: 88].

## 3. Validação (tests/test_prompts.py)
[cite_start]Implementar testes com `pytest` para garantir a integridade do prompt v2[cite: 119]:
- [cite_start]`test_prompt_has_system_prompt`[cite: 120].
- [cite_start]`test_prompt_has_role_definition`[cite: 121].
- [cite_start]`test_prompt_mentions_format` (Markdown ou User Story)[cite: 122].
- [cite_start]`test_prompt_has_few_shot_examples`[cite: 123].
- [cite_start]`test_prompt_no_todos` (Garantir que não há marcadores vazios)[cite: 124].
- [cite_start]`test_minimum_techniques` (Validar metadados no YAML)[cite: 125].