# Desafio: Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo Geral
[cite_start]Desenvolver um software em Python 3.9+ que automatiza o ciclo de vida de um prompt: captura (pull), otimização, publicação (push) e avaliação de qualidade[cite: 1, 3, 39].

## Requisitos de Performance
[cite_start]O objetivo final é que o prompt otimizado atinja uma **pontuação mínima de 0.9 (90%)** em todas as métricas abaixo[cite: 8, 117]:
- [cite_start]**Tone Score** [cite: 112]
- [cite_start]**Acceptance Criteria Score** [cite: 113]
- [cite_start]**User Story Format Score** [cite: 114]
- [cite_start]**Completeness Score** [cite: 115]

## Fluxo de Trabalho
1. [cite_start]**Pull**: Utilizar o prompt `prompt/bug_to_user_story_v1` do LangSmith Prompt Hub[cite: 68, 69].
2. [cite_start]**Otimização**: Refatorar o prompt aplicando técnicas avançadas (mínimo de 2)[cite: 75, 76].
3. [cite_start]**Push**: Enviar a versão v2 para o Hub do usuário[cite: 96, 98].
4. [cite_start]**Avaliação**: Executar o script de avaliação e iterar até atingir os scores necessários[cite: 107, 110].

## Tecnologias Obrigatórias
- [cite_start]**Framework**: LangChain[cite: 40].
- [cite_start]**Plataforma**: LangSmith (Client e Prompt Hub)[cite: 41, 42].
- [cite_start]**Formato de Prompt**: YAML[cite: 43].
- [cite_start]**LLMs**: GPT-4o-mini (resposta) e GPT-4o (avaliação), ou Gemini-2.5-flash[cite: 52, 53, 57, 58].