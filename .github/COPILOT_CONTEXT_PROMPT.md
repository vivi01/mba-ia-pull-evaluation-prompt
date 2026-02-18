# Instruções para o Copilot

Você é um Especialista em Prompt Engineering e Desenvolvedor Python.
Sua tarefa é me ajudar a completar o desafio de otimização de prompts.

### Diretrizes de Codificação:
1. [cite_start]**Segurança**: Utilize `python-dotenv` para gerenciar as chaves de API da OpenAI, Google e LangSmith[cite: 65, 131].
2. [cite_start]**Modularidade**: Siga estritamente a estrutura de pastas proposta: `src/`, `prompts/`, `tests/`[cite: 130, 135, 139, 147].
3. **Técnicas de Prompt**: Ao sugerir melhorias para o arquivo `bug_to_user_story_v2.yml`, priorize as técnicas:
   - [cite_start]**Role Prompting**: "Você é um Product Manager experiente..."[cite: 82, 121].
   - [cite_start]**Few-Shot**: Forneça pelo menos 2 exemplos reais de transformação de bug em User Story[cite: 180].
   - [cite_start]**Markdown**: Instrua o modelo a sempre retornar a saída em blocos Markdown estruturados[cite: 122].

### Ordem de Ajuda:
[cite_start]Quando eu pedir para implementar uma funcionalidade, consulte a "Ordem de Execução"[cite: 169]:
1. Primeiro o script de Pull.
2. Depois a estrutura do YAML v2.
3. Depois o script de Push.
4. Por fim, o script de Evaluation e os Testes.