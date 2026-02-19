# 🎬 Exemplos Práticos: Code Review da Skill em Ação

## Cenário 1: Revisar Script de Avaliação (LangChain Integration)

### Comando
```bash
python src/code_review.py src/evaluate.py
```

### Resultado Esperado (Exemplo)
```
================================================================================
🔍 CODE REVIEW REPORT
================================================================================

📊 RESUMO
  - Critical:  0 issue(ns)
  - High:      2 issue(ns)
  - Medium:    1 issue(ns)
  - Low:       0 issue(ns)
  - Suggestion: 0 issue(ns)
  - TOTAL:     3 issue(ns)


🟠 HIGH (2 issues)
─────────────────────────────────────────────────────────────────────────────

📄 src\evaluate.py:120
   Categoria: LangChain Integration
   Título: hub.pull sem tratamento de erro
   Descrição: hub.pull() pode falhar se prompt não existir
   Código: prompt = hub.pull(prompt_name)
   ✨ Sugestão: Envolver em try-except com mensagem de erro clara

📄 src\evaluate.py:175
   Categoria: LangChain Integration
   Título: Cliente LangSmith sem validação
   Descrição: Deve validar LANGSMITH_API_KEY antes
   ✨ Sugestão: Adicionar check_env_vars() antes de Client()


🟡 MEDIUM (1 issues)
─────────────────────────────────────────────────────────────────────────────

📄 src\evaluate.py:280
   Categoria: Documentation
   Título: Docstring ausente
   Descrição: Função sem documentação
   ✨ Sugestão: Adicionar docstring no formato Google/NumPy

================================================================================
✅ Relatório salvo em: code_review_report.json
```

### Como Corrigir - Hub Pull Sem Try-Except

**Antes (Problema):**
```python
def load_prompt_from_hub(prompt_name: str):
    prompt = hub.pull(prompt_name)  # ❌ Pode falhar
    return prompt
```

**Depois (Corrigido):**
```python
def load_prompt_from_hub(prompt_name: str) -> RunnableSequence:
    """
    Carrega prompt do LangSmith Hub com validação de erro.
    
    Args:
        prompt_name: Nome do prompt (formato: "username/prompt_v2")
    
    Returns:
        RunnableSequence do LangChain
    
    Raises:
        ValueError: Se prompt não encontrada no Hub
    """
    try:
        prompt = hub.pull(prompt_name)
        logger.info(f"Prompt '{prompt_name}' carregado com sucesso")
        return prompt
    except Exception as e:
        error_msg = f"Falha ao carregar prompt '{prompt_name}' do Hub: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
```

---

### Como Corrigir - Validação de Credenciais

**Antes:**
```python
client = Client()  # ❌ Pode falhar silenciosamente
```

**Depois:**
```python
# 1. Adicionar função helper em utils.py
def validate_langsmith_credentials() -> Client:
    """Valida e retorna cliente LangSmith autenticado."""
    api_key = os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        raise ValueError(
            "LANGSMITH_API_KEY não configurada.\n"
            "1. Crie chave em: https://smith.langchain.com/settings/keys\n"
            "2. Adicione ao .env: LANGSMITH_API_KEY=lsv2_pt_...\n"
            "3. Reinicie a aplicação"
        )
    return Client()

# 2. Usar no código
try:
    client = validate_langsmith_credentials()
    logger.info("LangSmith cliente autenticado")
except ValueError as e:
    logger.error(f"Erro de autenticação: {e}")
    sys.exit(1)
```

---

## Cenário 2: Revisar Novo Prompt YAML

### Comando
```bash
python src/code_review.py prompts/bug_to_user_story_v2.yml
```

### Resultado Esperado (Exemplo)
```
================================================================================
🔍 CODE REVIEW REPORT
================================================================================

📊 RESUMO
  - Critical:  1 issue(ns)
  - High:      1 issue(ns)
  - Medium:    0 issue(ns)
  - Low:       0 issue(ns)
  - Suggestion: 0 issue(ns)
  - TOTAL:     2 issue(ns)


🔴 CRITICAL (1 issues)
─────────────────────────────────────────────────────────────────────────────

📄 prompts\bug_to_user_story_v2.yml
   Categoria: Prompt Structure
   Título: Campo obrigatório ausente: 'techniques_applied'
   Descrição: Prompt YAML deve conter: system_prompt, version, techniques_applied, description
   ✨ Sugestão: Adicionar campo 'techniques_applied' ao prompt YAML


🟠 HIGH (1 issues)
─────────────────────────────────────────────────────────────────────────────

📄 prompts\bug_to_user_story_v2.yml
   Categoria: Few-Shot Learning
   Título: Few-shot examples insuficientes
   Descrição: Recomenda-se 2-3 exemplos para melhor performance
   ✨ Sugestão: Expandir exemplos para cobrir casos comuns e edge cases

================================================================================
✅ Relatório salvo em: code_review_report.json
```

### Como Corrigir - Adicionar Técnicas

**Antes:**
```yaml
version: v2
system_prompt: "Você é um Product Manager..."
description: "Converte bugs em user stories"
# ❌ Ausente: techniques_applied
```

**Depois:**
```yaml
version: v2
system_prompt: "Você é um Product Manager..."
description: "Converte bugs em user stories usando técnicas avançadas"

techniques_applied:
  - "Few-shot Learning"           # 2-3 exemplos claros de input/output
  - "Chain of Thought"             # Instruir modelo a pensar passo a passo
  - "Role Prompting"               # Definir persona detalhada

examples:
  - name: "Simple bug fix"
    input: "Button not clickable on mobile"
    output: |
      ## User Story
      As a mobile user
      I want clickable buttons
      So my interactions are processed
      
      ## Acceptance Criteria
      - [ ] Button responds to touch within 50ms
      - [ ] Works on iOS 14+, Android 11+
```

---

### Como Corrigir - Adicionar Few-Shot Examples

**Antes:**
```yaml
examples:
  - input: "Fix authentication bug"
    output: "User Story format..."
# ❌ Apenas 1 exemplo, sem clareza
```

**Depois:**
```yaml
examples:
  # Exemplo 1: Bug Simples (Happy Path)
  - name: "Simple Critical Bug"
    input: "Login button is broken on homepage"
    output: |
      ## User Story
      As a user trying to login
      I want the login button to be clickable
      So I can access my account
      
      ## Acceptance Criteria
      - [ ] Button is visible and enabled
      - [ ] Clicking navigates to login page
      - [ ] Works on Chrome, Firefox, Safari
      
      ## Tasks
      - [ ] Check button HTML elements
      - [ ] Verify onClick handler
      - [ ] Update CSS if needed

  # Exemplo 2: Bug Ambíguo (Com Clarificações)
  - name: "Ambiguous Performance Issue"
    input: "Dashboard is very slow"
    output: |
      ## User Story (Clarifications Needed)
      As a power user viewing the dashboard
      I want the dashboard to load in < 2 seconds
      So I can quickly monitor system status
      
      ## Acceptance Criteria
      - [ ] Initial load: < 2000ms
      - [ ] Interactions responsive: < 500ms
      - [ ] Works with 1000+ data points
      - [ ] Tested on Chrome DevTools throttling
      
      **Questions to Ask:**
      - Which dashboard view is slow? (list, charts, etc)
      - What data volume? (small test, production)
      - Browser/device constraints?

  # Exemplo 3: Bug Complexo (Refactoring)
  - name: "Complex Architectural Change"
    input: "Rewrite authentication module to use OAuth2"
    output: |
      ## User Story
      As a security-conscious user
      I want OAuth2 authentication
      So my credentials are protected and shared safely
      
      ## Acceptance Criteria
      - [ ] OAuth2 flow implemented (Google, GitHub)
      - [ ] Legacy auth methods deprecated
      - [ ] User migration script created
      - [ ] All tests passing (coverage > 90%)
      - [ ] Security audit completed
      
      ## Tasks
      - [ ] Design OAuth2 integration
      - [ ] Implement provider connectors
      - [ ] Create migration job
      - [ ] Update documentation
      
      ## Risks
      - User migration downtime
      - Third-party service dependency
      - Legacy system compatibility
```

---

## Cenário 3: Revisar Testes

### Comando
```bash
python src/code_review.py tests/test_prompts.py
```

### Resultado Esperado (Exemplo)
```
================================================================================
🔍 CODE REVIEW REPORT
================================================================================

📊 RESUMO
  - Critical:  0 issue(ns)
  - High:      0 issue(ns)
  - Medium:    0 issue(ns)
  - Low:       1 issue(ns)
  - Suggestion: 0 issue(ns)
  - TOTAL:     1 issue(ns)


🟢 LOW (1 issues)
─────────────────────────────────────────────────────────────────────────────

📄 tests\test_prompts.py:45
   Categoria: Type Hints
   Título: Type hints ausentes
   Descrição: Função deveria ter anotações de tipo
   ✨ Sugestão: Adicionar type hints: def func(param: str) -> dict:

================================================================================
✅ Todos os testes implementados corretamente!
✅ Relatório salvo em: code_review_report.json
```

---

## Cenário 4: Revisar Todo Repositório (Full Scan)

### Comando
```bash
python src/code_review.py .
```

### Resultado Esperado (Exemplo Resumido)
```
================================================================================
🔍 CODE REVIEW REPORT - FULL REPOSITORY SCAN
================================================================================

📊 RESUMO GERAL
  - Critical:  0 issue(ns)
  - High:      2 issue(ns)
  - Medium:    5 issue(ns)
  - Low:       8 issue(ns)
  - Suggestion: 3 issue(ns)
  - TOTAL:     18 issue(ns)

📊 BREAKDOWN POR ARQUIVO
  - src/evaluate.py:        2 HIGH, 1 MEDIUM
  - src/metrics.py:         1 MEDIUM, 2 LOW
  - src/utils.py:           4 LOW, 1 SUGGESTION
  - prompts/*.yml:          2 MEDIUM, 3 SUGGESTION
  - tests/test_prompts.py:  2 LOW

🎯 AÇÃO IMEDIATA
  1. Revisar 2 issues HIGH em src/evaluate.py
  2. Implementar fixes e re-rodar
  
✅ Relatório salvo em: code_review_report.json
```

---

## Cenário 5: Integração em GitHub Actions (Automática)

### Setup
```bash
# 1. Criar arquivo
touch .github/workflows/code-review-ci.yml

# 2. Copiar conteúdo do template (veja code-review-skill.md)

# 3. Fazer commit
git add .github/workflows/code-review-ci.yml
git commit -m "CI: Add automated code review"
```

### Resultado ao Fazer PR
```
PR #42: "Feat: Improve prompt evaluation"

✅ Checks
├─ Code Review        PASS
├─ Security Scan      PASS
├─ Unit Tests         PASS (45/45)
├─ Coverage           PASS (86%)
└─ All checks passed

📝 Comment by GitHub Actions:

## 🔍 Code Review Results
```
$REPORT_CONTENT
```

:heavy_check_mark: APPROVED - Ready to merge!
```

---

## Cenário 6: Corrigir Segurança (API Keys)

### Problema Detectado
```
python src/code_review.py src/

🔴 CRITICAL: Hardcoded OpenAI API key detected
   Arquivo: src/config_provider.py (linha 25)
   Código: api_key = "sk-proj-xxxxx"
   RISCO: Chave exposta em repositório público!
```

### Solução Passo a Passo

**Passo 1: Criar .env (se não existir)**
```bash
cp .env.example .env
# Editar .env com suas chaves (já está em .gitignore)
```

**Passo 2: Refatorar código**
```python
# Antes (ERRADO)
openai.api_key = "sk-proj-xxxxx"

# Depois (CORRETO)
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Com validação
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY não configurada no .env")
```

**Passo 3: Revogar chaves comprometidas**
```
1. OpenAI: https://platform.openai.com/account/api-keys
2. Google: https://aistudio.google.com/app/apikey
3. LangSmith: https://smith.langchain.com/settings/keys
```

**Passo 4: Gerar chaves novas e atualizar .env**

**Passo 5: Verificar se foi removida do histórico git**
```bash
# Verificar se a chave aparece em commits anteriores
git log -p | grep "sk-proj-\|AIzaSy"

# Se aparecer, usar BFG Repo-Cleaner
# (https://rtyley.github.io/bfg-repo-cleaner/)
```

**Passo 6: Re-rodar code review**
```bash
python src/code_review.py src/

# Esperado: ✅ Sem CRITICAL issues
```

---

## Cenário 7: Melhorar Documentação

### Problema Detectado
```
📄 src/evaluate.py:85
   Categoria: Documentation
   Título: Docstring ausente
   Descrição: Função 'calculate_metrics' sem documentação
```

### Solução

**Antes (sem docstring):**
```python
def calculate_metrics(prompt_output, expected_output, evaluator_llm):
    # Calcula métricas
    f1_score = 2 * (precision * recall) / (precision + recall)
    return {"f1": f1_score, "clarity": 0.8}
```

**Depois (com docstring completa):**
```python
def calculate_metrics(
    prompt_output: str,
    expected_output: str,
    evaluator_llm: BaseLanguageModel
) -> Dict[str, float]:
    """
    Calcula métricas de avaliação do prompt usando LLM como juiz.
    
    Implementa avaliação multi-dimensional baseada em:
    - F1-Score: Precisão e recall da resposta
    - Clarity: Qualidade e estrutura da resposta
    - Tone: Tom e profissionalismo apropriado
    - Completeness: Cobertura de critérios de aceitação
    
    Args:
        prompt_output: Resposta gerada pelo modelo
        expected_output: Output esperado (ground truth)
        evaluator_llm: LLM para fazer avaliação (ex: GPT-4)
    
    Returns:
        Dict com métricas normalizadas [0, 1]:
        {
            "f1_score": float,
            "clarity": float,
            "tone": float,
            "completeness": float
        }
    
    Raises:
        ValueError: Se outputs vazios ou LLM falha
    
    Example:
        >>> metrics = calculate_metrics(
        ...     prompt_output="User story...",
        ...     expected_output="User story...",
        ...     evaluator_llm=ChatOpenAI()
        ... )
        >>> print(metrics["f1_score"])
        0.92
    """
    # Implementação...
    return {"f1": f1_score, "clarity": 0.8}
```

---

## Cenário 8: Daily Workflow com Code Review

### Morning: Começar Feature

```bash
# 1. Atualizar repositório
git checkout main && git pull

# 2. Criar branch
git checkout -b feat/improve-prompts

# 3. Ativar environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Começar desenvolvimento
# editar arquivo X
```

### During: Testar Alterações

```bash
# 1. Rodar testes locais
pytest tests/ -v

# 2. Testar funcionalidade
python src/evaluate.py

# 3. Code review local
python src/code_review.py src/
python src/code_review.py prompts/

# 4. Revisar saída
# Corrigir issues se houver
```

### Evening: Fazer Commit

```bash
# 1. Verificar mudanças
git diff

# 2. Segurança final
grep -r "sk-proj-\|AIzaSy\|lsv2_pt_" src/ prompts/ tests/ && echo "ISSUES!" || echo "✅ OK"

# 3. Testes finais
pytest tests/ -v --cov=src

# 4. Code review final
python src/code_review.py .

# 5. Se tudo ok
git add .
git commit -m "feat: Implement improved prompts with better examples"
git push origin feat/improve-prompts
```

### Results: GitHub Actions Automático

```
PR criado → GitHub Actions executa:
1. ✅ Code Review automático
2. ✅ Testes com coverage
3. ✅ Security scan
4. ✅ Comentário com resultados

Se tudo PASS → Você aprova e faz merge
```

---

## 🎯 Resumo dos Cenários

| Cenário | Comando | Tempo | Benefício |
|---------|---------|-------|-----------|
| **1. Script Python** | `code_review.py src/evaluate.py` | 5s | Issues LangChain |
| **2. YAML Prompt** | `code_review.py prompts/*.yml` | 5s | Validação Estrutura |
| **3. Testes** | `code_review.py tests/` | 3s | Coverage feedback |
| **4. Scan Completo** | `code_review.py .` | 15s | Overview geral |
| **5. GitHub Actions** | Push PR | Auto | Automático |
| **6. Segurança** | `code_review.py src/` | < 1s | API keys detectadas |
| **7. Documentação** | `code_review.py src/` | < 1s | Docstrings |
| **8. Daily Workflow** | Integrado | Normal | Fluxo naturalizado |

---

## ✅ Checklist: Skill em Ação

Quando terminar desenvolvimento:

- [ ] Rodei `python src/code_review.py src/`
- [ ] Rodei `python src/code_review.py prompts/`
- [ ] Arrumei issues HIGH/CRITICAL
- [ ] Testes passam: `pytest tests/ -v`
- [ ] Sem secrets expostas: `grep -r "sk-proj"` = vazio
- [ ] Documentação atualizada: Docstrings presentes
- [ ] Comiteei com message clara
- [ ] Pushei para PR
- [ ] GitHub Actions passou
- [ ] Aprovei e mergesei

**Resultado:** Código de produção excelente! 🚀

