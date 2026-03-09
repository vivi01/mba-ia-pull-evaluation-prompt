# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

```bash
# Executar o pull dos prompts ruins do LangSmith
python src/pull_prompts.py

# Executar avaliação inicial (prompts ruins)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v1a
- Helpfulness: 0.45
- Correctness: 0.52
- F1-Score: 0.48
- Clarity: 0.50
- Precision: 0.46
================================
Status: FALHOU - Métricas abaixo do mínimo de 0.9

# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação final (prompts otimizados)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v2_optimized
- Helpfulness: 0.94
- Correctness: 0.96
- F1-Score: 0.93
- Clarity: 0.95
- Precision: 0.92
================================
Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull dos Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme instruções no `README.md` do repositório base)
2. Acessar o script `src/pull_prompts.py` que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompts:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva os prompts localmente em `prompts/raw_prompts.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **pelo menos duas** das seguintes técnicas:
   - **Few-shot Learning**: Fornecer exemplos claros de entrada/saída
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot)
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Criar o script `src/push_prompts.py` que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixa-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Tone Score >= 0.9
- Acceptance Criteria Score >= 0.9
- User Story Format Score >= 0.9
- Completeness Score >= 0.9

MÉDIA das 4 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 4 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml # Seu prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
├── tests/
│   └── test_prompts.py       # Testes de validação
│
```

**O que você vai criar:**

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompt.py` Script de pull do repositório da fullcycle
- `src/push_prompt.py` Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

**O que já vem pronto:**

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 4 métricas específicas para Bug to User Story
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Validação

- **Testes automatizados:** execute `pytest tests/test_prompts.py` para validar a estrutura do prompt otimizado. (6 testes esperados — `test_prompt_has_system_prompt`, `test_prompt_has_role_definition`, `test_prompt_mentions_format`, `test_prompt_has_few_shot_examples`, `test_prompt_no_todos`, `test_minimum_techniques`).
- **Arquivo validado:** `prompts/bug_to_user_story_v2.yml` contém `description`, `system_prompt`, `version`, `techniques_applied` e exemplos few-shot.
- **Observação:** A avaliação final via `src/evaluate.py` depende de chaves de API externas (LangSmith, OpenAI ou Google Gemini) e pode falhar por limites de cota. Verifique suas credenciais em `.env` antes de rodar.

### Avaliação com limite de tokens (máximo de exemplos)

O script `src/evaluate.py` suporta seleção automática do número máximo de exemplos sem ultrapassar um orçamento de tokens.

Variáveis suportadas:

- `EVAL_TOKEN_LIMIT`: orçamento total de tokens para a rodada de avaliação.
- `EVAL_TOKEN_RESERVE`: margem de segurança (default: `5000`).
- `EVAL_MAX_EXAMPLES` (opcional): teto manual adicional; quando informado, aplica `min(token_budget, manual_cap)`.

Exemplo de execução (Windows PowerShell):

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONUTF8='1'
$env:EVAL_TOKEN_LIMIT='180000'
$env:EVAL_TOKEN_RESERVE='10000'
python src/evaluate.py
```

Nesse modo, o script calcula automaticamente o maior `N` possível de exemplos do dataset que cabe no orçamento e exibe o resumo no terminal.

### Fluxo completo (pull → test → push → evaluate)

```bash
python src/pull_prompts.py
pytest tests/test_prompts.py -q
python src/push_prompts.py
python src/evaluate.py
```


## Técnicas Aplicadas (Fase 2)

### 1. **Role Prompting**

**O que é**: Definir uma persona específica para o modelo, estabelecendo contexto e expertise.

**Por que foi escolhida**: A transformação de bug reports em User Stories exige um entendimento profissional do processo de Product Management. Ao designar o modelo como "Product Manager experiente", elevamos a qualidade e profissionalismo das respostas.

**Como foi aplicada**:
```yaml
system_prompt: |
  Você é um Product Manager experiente. Sua tarefa é transformar...
```

**Impacto**: Melhora significativamente o tone profissional, clareza e contexto das User Stories geradas.

---

### 2. **Few-shot Learning**

**O que é**: Fornecer exemplos de entrada/saída para guiar o modelo sobre o comportamento esperado.

**Por que foi escolhida**: Exemplos concretos eliminam ambiguidade e mostram o formato exato esperado. Para bug→user story, exemplos claros são críticos pois melhoram:
- Consistência de formato
- Qualidade dos critérios de aceitação
- Tom e linguagem profissional

**Como foi aplicada**:
```yaml
few_shot_examples:
  - input: "Bug: Ao tentar salvar um comentário, aparece erro 500..."
    output: |
      ### User Story
      - **Como**: Usuário autenticado
      - **Eu quero**: salvar comentários sem erro
      - **Para que**: eu possa registrar feedback...
      
      **Critérios de Aceitação**:
      - O comentário é persistido sem erro 500
      - Mensagem de sucesso exibida ao usuário
```

**Impacto**: Aumenta drasticamente a precisão do formato, reduz hallucinations e garante que critérios de aceitação sejam sempre testáveis.

---

### Resultados das Técnicas

| Técnica | Métrica Impactada | Ganho Esperado |
|---------|------------------|-----------------|
| Role Prompting | Tone, Clarity | +30-40% |
| Few-shot Learning | Format, Criteria, Completeness | +25-35% |
| Combinadas | Média Geral | +50%+ |

---

## Como Executar

Fluxo recomendado (end-to-end):

1. **Pull dos prompts base**
   ```bash
   python src/pull_prompts.py
   ```
2. **Refatoração do prompt v2**
   - Edite manualmente `prompts/bug_to_user_story_v2.yml` com as técnicas aplicadas.
3. **Push do prompt otimizado para o Hub**
   ```bash
   python src/push_prompts.py
   ```
4. **Avaliação automática**
   ```bash
   python src/evaluate.py
   ```

---

## Resultados Finais

### Métricas de Avaliação - Prompt v2 Otimizado ✅

Resultado final obtido via execução real de `src/evaluate.py` (15/15 exemplos, LangSmith + Gemini).

#### Scorecard Final da v2 (Execução Real)

| Métrica | Score | Threshold | Status |
|---------|-------|-----------|--------|
| **Helpfulness** | 0.96 | >= 0.9 | ✅ APROVADO |
| **Correctness** | 0.94 | >= 0.9 | ✅ APROVADO |
| **F1-Score** | 0.94 | >= 0.9 | ✅ APROVADO |
| **Clarity** | 0.98 | >= 0.9 | ✅ APROVADO |
| **Precision** | 0.95 | >= 0.9 | ✅ APROVADO |
| **MÉDIA FINAL** | **0.9546** | **>= 0.9** | **✅ APROVADO** |

**Resumo Executivo:**
- ✅ Todas as métricas avaliadas ficaram >= 0.9
- ✅ Média geral 0.9546 — Prompt aprovado
- ✅ Técnicas aplicadas: **Role Prompting + Few-shot Learning + Skeleton of Thought**
- ✅ Prompt publicado no Hub em `viviane-pereira/viviane-pereira`

#### Evidência de Push Idempotente ✅

Execução validada de `src/push_prompts.py` sem alterações no prompt remoto:

- Mensagem retornada: `Prompt sem alterações desde o último commit no Hub. Nenhuma ação necessária (estado já publicado).`
- Comportamento esperado: conflito `409 Nothing to commit` tratado como sucesso (idempotência).

**Método de Avaliação:**
Avaliação real em `src/evaluate.py`, com dataset de 15 exemplos e execução registrada no LangSmith.

---

#### Descrição das Métricas Implementadas

**Métricas Gerais (3)**
- **F1-Score**: Balanceamento entre precision e recall da resposta
- **Clarity**: Clareza, estrutura e compreensibilidade
- **Precision**: Informações corretas, relevantes e sem hallucinations

**Métricas Específicas para Bug→UserStory (4)**
- **Tone Score**: Profissionalismo, empatia e linguagem apropriada
- **Acceptance Criteria Score**: Qualidade, testabilidade e especificidade dos critérios
- **User Story Format Score**: Conformidade com estrutura "Como... Eu quero... Para que..."
- **Completeness Score**: Contexto técnico, edge cases e informações suficientes

---

### Dashboard LangSmith

O projeto está integrado com LangSmith para:
- ✓ Armazenar prompts versionados no Hub
- ✓ Manter datasets de avaliação centralizados (`-eval` e `-eval-v2`, ambos com 15 exemplos)
- ✓ Registrar traces de cada execução
- ✓ Calcular métricas automaticamente
- ✓ Comparar v1 vs v2 side-by-side

**Acesso ao Dashboard:**
- Organização (principal - acesso interno/workspace): https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b
- Após abrir, acessar o projeto: `desafio-prompt-engineering_mba`

**Links públicos (usar estes para avaliação externa):**
- Compare público v1: https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d/compare?selectedSessions=ff0f7bce-c172-44ef-9eaf-ddebad3acc51
- Compare público v2: https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d/compare?selectedSessions=73aabcf6-c326-413d-89a1-7c383b94a505
- Dataset público v1: https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d
- Dataset público v2: https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d

**Prompt publicado no Hub:**
- US (canônico): https://smith.langchain.com/hub/viviane-pereira/viviane-pereira
- EU (fallback): https://eu.smith.langchain.com/hub/viviane-pereira/viviane-pereira

**Datasets de avaliação (organização):**
- `bug_to_user_story_v1`: https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b/datasets/e67caca1-6997-440e-98cf-84a567e6cbee
- `bug_to_user_story_v2`: https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b/datasets/38f7fd39-e3ab-48dd-acc5-f562fed8f62b

Observação: para dashboard/datasets, prefira links no formato `/o/<organization_id>/...` no seu workspace.

---

### Iterações e Melhoria

Para atingir scores >= 0.9 em todas as métricas:

**Ciclo Iterativo (3-5 iterações esperadas)**:

```bash
# Ciclo 1: Rodar avaliação
python src/evaluate.py

# Analisar resultados
# Identificar qual métrica está baixa e por quê

# Ciclo 2: Editar prompt
# Melhorar instruções, exemplos ou critérios
vim prompts/bug_to_user_story_v2.yml

# Push atualizado
python src/push_prompts.py

# Avaliar novamente
python src/evaluate.py

# Continuar até >= 0.9 em TODAS métricas
```

---

## Evidências + Checklist de Capturas

Avaliação executada: **REAL (LangSmith + LLM)** ✅

**Resultado final da execução:**
- Prompt: `viviane-pereira/viviane-pereira`
- Dataset: `bug_to_user_story_v1` (15 exemplos)
- Dataset v2: `bug_to_user_story_v2` (15 exemplos)
- Média: **0.9546** (APROVADO)

**Experimentos públicos (compare):**
- Dataset `bug_to_user_story_v1`: https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d/compare?selectedSessions=ff0f7bce-c172-44ef-9eaf-ddebad3acc51
- Dataset `bug_to_user_story_v2`: https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d/compare?selectedSessions=73aabcf6-c326-413d-89a1-7c383b94a505

### Checklist objetivo para screenshots do LangSmith

Marque como concluído somente se todos os itens visuais estiverem presentes na captura:

- [ ] `screenshots/langsmith_project_overview.png`  
   Exibe visão geral do projeto `desafio-prompt-engineering_mba` (tracing/runs/prompts). Nesta tela os datasets podem não aparecer.
- [ ] `screenshots/langsmith_dataset.png`  
   Exibe dataset `bug_to_user_story_v1` com 15 exemplos.
- [ ] `screenshots/langsmith_prompt_hub.png`  
   Exibe prompt publicado `viviane-pereira/viviane-pereira` no Hub (visível como público).
- [ ] `screenshots/langsmith_run_metrics.png`  
   Exibe métricas da execução final (Helpfulness, Correctness, F1, Clarity, Precision) com scores >= 0.9.
- [ ] `screenshots/langsmith_public_compare_eval.png`  
   Exibe comparação pública do experimento no dataset `-eval` (link público com `selectedSessions`).
- [ ] `screenshots/langsmith_public_compare_eval_v2.png`  
   Exibe comparação pública do experimento no dataset `-eval-v2` (link público com `selectedSessions`).
- [ ] `screenshots/langsmith_trace_example_1.png`  
   Exibe trace completo de um exemplo (entrada + saída + avaliação).
- [ ] `screenshots/langsmith_trace_example_2.png`  
   Exibe segundo trace completo.
- [ ] `screenshots/langsmith_trace_example_3.png`  
   Exibe terceiro trace completo.
- [ ] `screenshots/langsmith_push_idempotent_log.png`  
   Exibe evidência do push idempotente: mensagem de "nenhuma ação necessária" / `Nothing to commit`.

### Links de origem para cada screenshot

Use os links abaixo para abrir a tela correta de cada item do checklist:

- `screenshots/langsmith_project_overview.png`  
   Fonte (interna/workspace): https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b
   Observação: esta página é apenas overview do projeto; evidências de datasets devem ser capturadas pelos links de dataset público abaixo.

- `screenshots/langsmith_dataset.png`  
   Fonte (dataset v1):https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d
  <img width="1667" height="617" alt="image" src="https://github.com/user-attachments/assets/92899c11-211c-4ba9-b9e2-7b6a2ec0c309" />

  Fonte (dataset v2): https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d
 <img width="1672" height="647" alt="image" src="https://github.com/user-attachments/assets/c710b37e-b434-4de8-a2a0-bbb265d6c36a" />

- `screenshots/langsmith_prompt_hub.png`  
   Fonte: https://smith.langchain.com/hub/viviane-pereira/viviane-pereira
  <img width="1321" height="865" alt="image" src="https://github.com/user-attachments/assets/cb2c646f-1014-4207-ba45-30a744a08684" />

- `screenshots/langsmith_run_metrics.png`  
   Fonte (compare v2): https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d/compare?selectedSessions=73aabcf6-c326-413d-89a1-7c383b94a505
  <img width="1701" height="707" alt="image" src="https://github.com/user-attachments/assets/f62901fa-e6a3-4175-ae15-735415cf19ac" />

- `screenshots/langsmith_public_compare_eval.png`  
   Fonte: https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d/compare?selectedSessions=ff0f7bce-c172-44ef-9eaf-ddebad3acc51
  <img width="1663" height="713" alt="image" src="https://github.com/user-attachments/assets/e1c7986a-4ac4-4373-a77a-39f386a3d209" />

- `screenshots/langsmith_public_compare_eval_v2.png`  
   Fonte: https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d/compare?selectedSessions=73aabcf6-c326-413d-89a1-7c383b94a505
  <img width="1666" height="706" alt="image" src="https://github.com/user-attachments/assets/a7d83f9b-974b-4042-bcdc-8c4aa4c9b1ad" />

- `screenshots/langsmith_trace_example_1.png`, `screenshots/langsmith_trace_example_2.png`, `screenshots/langsmith_trace_example_3.png`  
   Fonte: abra uma das páginas de compare acima e clique em linhas diferentes para abrir os traces individuais.

- `screenshots/langsmith_push_idempotent_log.png`  
   Fonte (terminal local): execute `python src/push_prompts.py` e capture a linha com "Prompt sem alterações desde o último commit no Hub. Nenhuma ação necessária (estado já publicado)."
<img width="1134" height="301" alt="image" src="https://github.com/user-attachments/assets/c4f19b97-b4e3-4c42-a58c-ec700a188882" />

**Comando usado para gerar avaliação final:**

```bash
python src/evaluate.py
```
<img width="671" height="496" alt="image" src="https://github.com/user-attachments/assets/5a6eaac7-29d3-4482-af83-7fc89abdbef2" />

### Roteiro rápido de captura (2–3 minutos)

Use esta ordem para gerar todas as evidências sem retrabalho:

1. Abra o projeto no dashboard (`desafio-prompt-engineering_mba`) e capture `screenshots/langsmith_project_overview.png`.
2. No mesmo projeto, abra o dataset `bug_to_user_story_v1` e capture `screenshots/langsmith_dataset.png`.
3. Abra o prompt publicado no Hub (`viviane-pereira/viviane-pereira`) e capture `screenshots/langsmith_prompt_hub.png`.
4. Volte para a execução final do `evaluate.py` e capture a tela de métricas agregadas em `screenshots/langsmith_run_metrics.png`.
5. Abra os links públicos de compare e capture:
   - `screenshots/langsmith_public_compare_eval.png`
   - `screenshots/langsmith_public_compare_eval_v2.png`
6. Na página da run, abra três traces diferentes (um por vez) e capture:
   - `screenshots/langsmith_trace_example_1.png`
   - `screenshots/langsmith_trace_example_2.png`
   - `screenshots/langsmith_trace_example_3.png`
7. No terminal após `python src/push_prompts.py`, capture a mensagem de push idempotente em `screenshots/langsmith_push_idempotent_log.png`.

Dica: mantenha o mesmo zoom/navegador em todas as capturas para padronizar a evidência visual do entregável.

### Checklist operacional (copiar e colar)

```text
[ ] 1) Project overview → screenshots/langsmith_project_overview.png
[ ] 2) Dataset (15 exemplos) → screenshots/langsmith_dataset.png
[ ] 3) Prompt no Hub (público) → screenshots/langsmith_prompt_hub.png
[ ] 4) Run metrics finais (>=0.9) → screenshots/langsmith_run_metrics.png
[ ] 5) Public compare (eval) → screenshots/langsmith_public_compare_eval.png
[ ] 6) Public compare (eval-v2) → screenshots/langsmith_public_compare_eval_v2.png
[ ] 7) Trace exemplo 1 → screenshots/langsmith_trace_example_1.png
[ ] 8) Trace exemplo 2 → screenshots/langsmith_trace_example_2.png
[ ] 9) Trace exemplo 3 → screenshots/langsmith_trace_example_3.png
[ ] 10) Log de push idempotente (Nothing to commit) → screenshots/langsmith_push_idempotent_log.png
```

**Link do dashboard LangSmith (quando disponível):**
- Organização (principal - interna/workspace): https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b
- Após abrir, acessar o projeto: `desafio-prompt-engineering_mba`

**Links públicos recomendados (sem necessidade de acesso ao workspace):**
- Compare público v1: https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d/compare?selectedSessions=ff0f7bce-c172-44ef-9eaf-ddebad3acc51
- Compare público v2: https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d/compare?selectedSessions=73aabcf6-c326-413d-89a1-7c383b94a505
- Dataset público v1: https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d
- Dataset público v2: https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d

**Links diretos dos datasets:**
- `bug_to_user_story_v1` (interna/workspace): https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b/datasets/e67caca1-6997-440e-98cf-84a567e6cbee
- `bug_to_user_story_v2` (interna/workspace): https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b/datasets/38f7fd39-e3ab-48dd-acc5-f562fed8f62b

**Links públicos dos datasets:**
- `bug_to_user_story_v1`: https://smith.langchain.com/public/0986a4fd-90f6-4ac1-be94-e033d966ec3f/d
- `bug_to_user_story_v2`: https://smith.langchain.com/public/2fccd07c-4090-474a-a179-355dfb4d7526/d

**Prompts no Hub:**
- US (canônico): https://smith.langchain.com/hub/viviane-pereira/viviane-pereira
- EU (fallback): https://eu.smith.langchain.com/hub/viviane-pereira/viviane-pereira


### Estrutura do Projeto

```
mba-ia-pull-evaluation-prompt/
├── prompts/
│   ├── bug_to_user_story_v1.yml    # Original (após pull)
│   └── bug_to_user_story_v2.yml    # Otimizado (v2)
│
├── datasets/
│   └── bug_to_user_story.jsonl     # 15 exemplos para avaliação
│
├── src/
│   ├── pull_prompts.py             # Pull de prompts do Hub
│   ├── push_prompts.py             # Push ao Hub
│   ├── evaluate.py                 # Pipeline de avaliação (7 métricas)
│   ├── metrics.py                  # Implementação das 7 avaliadores
│   └── utils.py                    # Funções auxiliares
│
├── tests/
│   └── test_prompts.py             # 6 testes de validação
│
├── requirements.txt                # Dependências Python
├── .env                            # Variáveis de ambiente
└── README.md                       # Este arquivo
```

---

## Guia Detalhado de Execução

### Pré-requisitos

- **Python 3.9+**
- **pip** (gerenciador de pacotes)
- **Git**
- **Credenciais configuradas**:
  - `LANGSMITH_API_KEY` (obrigatório)
  - `OPENAI_API_KEY` ou `GOOGLE_API_KEY` (para LLM)

### Setup Inicial

```bash
# 1. Clone o repositório
git clone https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt
cd mba-ia-pull-evaluation-prompt

# 2. Crie um ambiente virtual
python -m venv venv

# 3. Ative o ambiente
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure as variáveis de ambiente
# Copie .env.example para .env e preencha suas chaves
cp .env.example .env

# Configure no arquivo .env:
LANGSMITH_API_KEY=lsv2_pt_...
OPENAI_API_KEY=sk-...  # OU
GOOGLE_API_KEY=AIzaSy...

# Escolha um provider (recomendado: openai para melhor quota)
LLM_PROVIDER=openai
```

---

### Executar o Pipeline Completo

```bash
# 1. Pull do prompt original (v1)
python src/pull_prompts.py
# Saída: prompts/bug_to_user_story_v1.yml

# 2. Refatorar/Otimizar (manual)
# Edite: prompts/bug_to_user_story_v2.yml
# Aplique as técnicas de prompt engineering

# 3. Push da versão otimizada (v2)
python src/push_prompts.py
# Saída: Publicado em LangSmith Hub

# 4. Executar avaliação
python src/evaluate.py
# Saída: Métricas para cada exemplo e média geral
```

---

### Rodar Testes

```bash
# Executar todos os 6 testes de validação
pytest tests/test_prompts.py -v

# Esperado: 6 PASSED
```

---

### Solução de Problemas

#### Problema: "LANGSMITH_API_KEY não configurada"
```bash
# Solução:
# 1. Gere chave em https://smith.langchain.com/settings/keys
# 2. Adicione ao .env:
LANGSMITH_API_KEY=lsv2_pt_seu_token_aqui
```

#### Problema: "Quota excedida do Gemini Free"
```bash
# Google Gemini Free Tier: 20 req/dia
# Solução: Trocar para OpenAI
# No .env:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

#### Problema: "Scores ainda baixos"
```bash
# Cicle as iterações:
1. Analisar feedback das métricas no LangSmith Trace
2. Editar prompts/bug_to_user_story_v2.yml
3. python src/push_prompts.py
4. python src/evaluate.py
5. Repetir até todas métricas >= 0.9
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"** ✓
      - [x] Quais técnicas avançadas foram aplicadas
      - [x] Justificativa de escolha
      - [x] Exemplos práticos de aplicação

   B) **Seção "Resultados Finais"** ✓
      - [x] Dashboard LangSmith e como acessar
      - [x] Métricas implementadas (7)
      - [x] Instruções de iteração

   C) **Seção "Como Executar"** ✓
      - [x] Instruções claras e detalhadas
      - [x] Pré-requisitos e dependências
      - [x] Setup inicial completo
      - [x] Comandos em ordem
      - [x] Troubleshooting

3. **Evidências no LangSmith**:
   - Organização: https://smith.langchain.com/o/05cbad01-75e8-484c-ba5f-7323b40af45b
   - Dataset principal: `bug_to_user_story_v1` (15 exemplos)
   - Dataset v2: `bug_to_user_story_v2` (15 exemplos)
   - Prompts publicados em seu perfil do LangSmith Hub

---

## Resumo das Implementações

### ✅ Todos os Requisitos Técnicos Implementados

| Componente | Status | Arquivo |
|-----------|--------|---------|
| Pull de prompts | ✅ | `src/pull_prompts.py` |
| Prompt original v1 | ✅ | `prompts/bug_to_user_story_v1.yml` |
| Prompt otimizado v2 | ✅ | `prompts/bug_to_user_story_v2.yml` |
| Push de prompts | ✅ | `src/push_prompts.py` |
| Pipeline de avaliação | ✅ | `src/evaluate.py` |
| 7 Métricas LLM-as-Judge | ✅ | `src/metrics.py` |
| 6 Testes de validação | ✅ | `tests/test_prompts.py` |
| Multi-provider (OpenAI + Gemini) | ✅ | `src/utils.py` |
| Dataset (15 exemplos) | ✅ | `datasets/bug_to_user_story.jsonl` |
| Documentação completa | ✅ | `README.md` |

---

## Próximos Passos para Produção

1. **Trocar para OpenAI** (melhor quota que Gemini Free):
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-...
   ```

2. **Executar primeira avaliação**:
   ```bash
   python src/evaluate.py
   ```

3. **Se scores < 0.9**, iterar o prompt:
   - Analisar feedback no LangSmith Trace
   - Editar `prompts/bug_to_user_story_v2.yml`
   - Fazer push e avaliar novamente
   - Repetir 3-5 vezes até >= 0.9

4. **Publicar no GitHub** com evidências finais

---

## Referências e Recursos

- **LangSmith Documentation**: https://docs.smith.langchain.com/
- **Prompt Engineering Guide**: https://www.promptingguide.ai/
- **LangChain Documentation**: https://python.langchain.com/
- **OpenAI API**: https://platform.openai.com/
- **Google Gemini API**: https://ai.google.dev/

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de PRs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final
