# 🚀 Como Usar a Skill de Code Review - Guia Prático

## Visão Geral

A **Code Review Skill** implementada neste projeto oferece uma abordagem sistemática e especializada para análise de código, aplicável imediatamente no desenvolvimento diário.

---

## 1. Uso Rápido do Script Automático

### 1.1 Instalação (Se necessário)

```bash
# As dependências já estão em requirements.txt
pip install -r requirements.txt
```

### 1.2 Executar Code Review

#### Opção A: Analisar um arquivo específico

```bash
# Arquivo Python
python src/code_review.py src/evaluate.py

# Arquivo YAML (Prompt)
python src/code_review.py prompts/bug_to_user_story_v2.yml
```

#### Opção B: Analisar todo um diretório

```bash
# Todos os .py em src/
python src/code_review.py src/

# Todos os prompts em prompts/
python src/code_review.py prompts/
```

### 1.3 Saída Esperada

```
🔍 Analisando: src/evaluate.py

================================================================================
🔍 CODE REVIEW REPORT
================================================================================

📊 RESUMO
  - Critical:  0 issue(ns)
  - High:      2 issue(ns)
  - Medium:    1 issue(ns)
  - Low:       1 issue(ns)
  - Suggestion: 0 issue(ns)
  - TOTAL:     4 issue(ns)

🔴 CRITICAL (0 issues)
─────────────────────────────────────────────────────────────────────────────

🟠 HIGH (2 issues)
─────────────────────────────────────────────────────────────────────────────

📄 src/evaluate.py:45
   Categoria: LangChain Integration
   Título: hub.pull sem tratamento de erro
   Descrição: hub.pull() pode falhar se prompt não existir
   Código: prompt = hub.pull(prompt_name)
   ✨ Sugestão: Envolver em try-except com mensagem de erro clara

[... mais issues ...]

✅ Relatório salvo em: code_review_report.json
```

---

## 2. Fluxo de Trabalho Integrado

### 2.1 Antes de Comitar: Checklist Local

```bash
#!/bin/bash
# scripts/pre-commit-review.sh

echo "🔍 Iniciando Code Review pré-commit..."

# 1. Executar code review automático
python src/code_review.py src/
python src/code_review.py prompts/

# 2. Rodas os testes
pytest tests/ -v --cov=src

# 3. Verificar linting (se tiver black/flake8)
# black --check src/ tests/
# flake8 src/ tests/

# 4. Se tudo passou
echo "✅ Pronto para commit!"
```

**Executar antes de cada commit:**
```bash
bash scripts/pre-commit-review.sh
```

### 2.2 Fluxo: Desenvolvimento → Review → Commit

```
1. Implementar Feature
   └─> python src/evaluate.py
       python src/push_prompts.py
       
2. Rodar Code Review
   └─> python src/code_review.py src/
       python src/code_review.py prompts/
       
3. Resolver Issues
   └─> Editar arquivos conforme feedback
       
4. Verificar Testes
   └─> pytest tests/ -v
       
5. Committar
   └─> git add .
       git commit -m "Feat: descrição clara"
       git push
```

---

## 3. Exemplos Reais de Uso

### Exemplo 1: Revisar o script de avaliação

```bash
python src/code_review.py src/evaluate.py
```

**Issues encontrados (hipotéticos):**

```markdown
🟠 HIGH: hub.pull sem try-except
- Arquivo: src/evaluate.py (linha 120)
- Problema: Se o prompt não existir, garante ValueError
- Sugestão:
  try:
      prompt = hub.pull(prompt_name)
  except Exception as e:
      logger.error(f"Falha ao fazer pull: {e}")
      raise

🟡 MEDIUM: Docstring ausente
- Arquivo: src/evaluate.py (linha 85)
- Função: calculate_metrics()
- Sugestão: Adicionar docstring explicando cálculos

💡 SUGGESTION: Type hints incompletos
- Linha 200: Adicionar return type hint
```

**Ação:** Corrigir issues HIGH/MEDIUM e documentar sugestões

---

### Exemplo 2: Revisar novo prompt YAML

```bash
python src/code_review.py prompts/bug_to_user_story_v2.yml
```

**Output:**

```markdown
🔴 CRITICAL: Campo obrigatório ausente
- Campo: 'techniques_applied'
- Solução: Adicionar ao YAML

🟠 HIGH: Few-shot examples insuficientes
- Problema: Apenas 1 exemplo fornecido
- Recomendação: Adicionar mais 2-3 exemplos

🟡 MEDIUM: Versão inconsistente
- Arquivo: bug_to_user_story_v2.yml
- Versão no YAML: v1
- Sugestão: Mudar para v2 para match com nome do arquivo
```

**Ação:** Editar arquivo YAML antes de fazer push

---

### Exemplo 3: Encontrar problemas de segurança

```bash
python src/code_review.py src/
```

**Se API keys estiverem hardcoded:**

```markdown
🔴 CRITICAL: Hardcoded OpenAI API key detected
- Arquivo: src/utils.py (linha 75)
- Código: api_key = "sk-proj-xxxxxx"
- RISCO: Chave exposta em repositório público!
- Ação: 
  1. Revogar chave em OpenAI console
  2. Gerar nova chave
  3. Adicionar ao .env (já em .gitignore)
  4. Usar: api_key = os.getenv("OPENAI_API_KEY")
```

---

## 4. Integração com GitHub Actions

### 4.1 Criar Workflow Automático

Criar arquivo: `.github/workflows/code-review-ci.yml`

```yaml
name: Automated Code Review

on:
  pull_request:
    branches: [ main, develop ]
  push:
    branches: [ main ]

jobs:
  code-review:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run Code Review
      run: |
        python src/code_review.py src/ > code-review-src.txt 2>&1
        python src/code_review.py prompts/ > code-review-prompts.txt 2>&1
        python src/code_review.py tests/ > code-review-tests.txt 2>&1
    
    - name: Check for Critical Issues
      run: |
        if grep -q "🔴 CRITICAL" code-review-*.txt; then
          echo "❌ CRITICAL issues found!"
          cat code-review-*.txt
          exit 1
        fi
        echo "✅ No critical issues found"
    
    - name: Run Tests
      run: pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload Review Report
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: code-review-reports
        path: code-review-*.txt
    
    - name: Comment PR with Results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const review = fs.readFileSync('code-review-src.txt', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '## 🔍 Code Review Results\n```\n' + review + '\n```'
          });
```

### 4.2 Resultado no GitHub

Quando você criar um PR, automaticamente:
1. ✅ Code review é executado
2. ✅ Testes rodam
3. ✅ Se houver CRITICAL issues, PR é bloqueado
4. ✅ Comentário é adicionado com feedback

---

## 5. Usando com Copilot

### 5.1 Code Review Interativo

```bash
# Em VS Code
1. Abra arquivo: src/evaluate.py
2. Pressione Ctrl+Shift+P (Cmd+Shift+P no Mac)
3. Procure: "Copilot: Comments"
4. Digite sua pergunta:

"Faça um code review especializado em:
- Segurança (API keys, credenciais)
- Qualidade de código (nomes, docstrings)
- Integração com LangChain
- Performance e tratamento de erros

Siga este framework: [copiar framework da seção 2 do documento]"
```

### 5.2 Exemplo de Prompt para Copilot

```markdown
@copilot Review este arquivo seguindo a Skill de Code Review especializada.

Dimensions:
1. 🔐 Security & Privacy
2. 📝 Code Quality
3. ⚡ Performance
4. 🧪 Test Coverage
5. 🔗 LangChain Integration
6. 📚 Documentation

Prioritize: CRITICAL > HIGH > MEDIUM > LOW

Format response as:
## [Priority] [Category]
**Issue:** ...
**Impact:** ...
**Suggestion:** ...
```

---

## 6. Analisar Métricas da Review

### 6.1 Report JSON (Automaticamente Gerado)

```bash
# Após rodar code review, arquivo é criado:
cat code_review_report.json
```

**Estrutura:**

```json
{
  "timestamp": "2026-02-19T15:30:00",
  "total_issues": 8,
  "summary": {
    "critical": 0,
    "high": 2,
    "medium": 3,
    "low": 3,
    "suggestion": 0
  },
  "issues": [
    {
      "priority": "🟠 HIGH",
      "category": "Error Handling",
      "file": "src/evaluate.py",
      "line": 120,
      "title": "hub.pull sem try-except",
      "description": "...",
      "suggestion": "..."
    },
    ...
  ]
}
```

### 6.2 Acompanhar Progresso

```bash
# Ver histórico de reviews
ls -la *.json

# Contar reduction de issues over time
# (depois de múltiplas reviews)
for f in code_review_report_*.json; do
  echo "$f: $(cat $f | jq '.total_issues')"
done
```

---

## 7. Checklist Prático Diário

### ✅ Antes de Começar Desenvolvimento

```bash
# 1. Atualizar main
git checkout main && git pull

# 2. Criar branch
git checkout -b feat/my-feature

# 3. Ativar venv
source venv/bin/activate  # ou semelhante
```

### ✅ Durante Desenvolvimento

```bash
# 1. Fazer alterações
# Editar src/evaluate.py, prompts/bug_to_user_story_v2.yml, etc.

# 2. Testes locais
pytest tests/ -v

# 3. Code review
python src/code_review.py src/
python src/code_review.py prompts/

# 4. Corrigir issues encontrados
# Editar arquivos conforme feedback
```

### ✅ Antes de Fazer Commit

```bash
# 1. Revisar mudanças
git diff

# 2. Última checagem de segurança
grep -r "sk-proj-\|AIzaSy\|lsv2_pt_" src/ prompts/ tests/ || echo "✅ No secrets found"

# 3. Testes finais
pytest tests/ -v --cov=src

# 4. Code review final
python src/code_review.py .

# 5. Se tudo ok:
git add .
git commit -m "Type: Description of changes"
git push origin feat/my-feature
```

### ✅ Antes de Fazer Merge

```bash
# Verificar feedback do GitHub Actions
# (Que roda code review automaticamente)

# Se tudo verde:
# Aprove o PR e faça merge
```

---

## 8. Exemplos de Correções Baseadas em Review

### Cenário 1: Hub.pull sem Try-Except

**Antes (Problema):**
```python
def load_prompt(prompt_name: str):
    prompt = hub.pull(prompt_name)  # ❌ Pode falhar silenciosamente
    return prompt
```

**Depois (Review Corrigido):**
```python
def load_prompt(prompt_name: str) -> RunnableSequence:
    """
    Carrega prompt do LangSmith Hub com tratamento de erro.
    
    Args:
        prompt_name: Nome do prompt (ex: "username/prompt_v2")
    
    Returns:
        Prompt runnable do LangChain
    
    Raises:
        ValueError: Se prompt não existir
    """
    try:
        prompt = hub.pull(prompt_name)
        logger.info(f"✅ Prompt '{prompt_name}' carregado com sucesso")
        return prompt
    except Exception as e:
        error_msg = f"❌ Falha ao carregar '{prompt_name}': {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e
```

---

### Cenário 2: YAML sem Few-Shot Examples

**Antes:**
```yaml
version: v2
system_prompt: "You are a Product Manager"
# ❌ Sem exemplos!
```

**Depois:**
```yaml
version: v2
system_prompt: "You are a Product Manager"

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
      
  - name: "Database issue"
    input: "Query returns duplicates"
    output: |
      ## User Story
      ...
```

---

## 9. Métricas de Sucesso

### Antes da Skill
- ❌ Issues encontrados em produção: 15/mês
- ❌ Bugs de segurança: 2-3/ano
- ❌ PR review time: 3-5 dias

### Depois da Skill (Esperado)
- ✅ Issues em produção: < 3/mês
- ✅ Bugs de segurança: 0 (detectados antes)
- ✅ PR review time: < 24h
- ✅ Code coverage: > 85%
- ✅ CRITICAL issues: 0

---

## 10. Troubleshooting

### Problema: Script não encontra arquivo

```bash
# Erro: "Arquivo não encontrado"

# Solução: Use caminho absoluto ou relativo correto
python src/code_review.py ./src/evaluate.py

# Ou verifique se est
á no dir
etório certo
pwd
ls src/
```

### Problema: Muitos false positives

```bash
# Solução: Code review é uma ferramenta, não verdade absoluta
# Use como guia, not como lei
# Discuta issues no time se discordar

# Você pode editar src/code_review.py para:
# - Mudar prioridades
# - Adicionar exceções (ex: ignore test_* functions)
# - Customizar regras por projeto
```

### Problema: Performance lenta em diretórios grandes

```bash
# Solução: Analisar arquivos específicos
python src/code_review.py src/evaluate.py  # Em vez de src/

# Ou adicionar filtering ao script
```

---

## 11. Próximos Passos

1. **Executar agora:**
   ```bash
   python src/code_review.py src/
   ```

2. **Implementar pré-commit hook:**
   - Adicionar `.github/workflows/code-review-ci.yml`
   - Ou git hook local

3. **Integrar no fluxo diário:**
   - Adicionar ao checklist pessoal
   - Usar antes de cada PR

4. **Customizar conforme necessário:**
   - Editar `src/code_review.py`
   - Adicionar novas regras específicas do projeto
   - Ajustar prioridades

5. **Treinar o time:**
   - Compartilhar documentation
   - Executar juntos em uma sessão
   - Usar feedback como learning material

---

## Conclusão

A **Code Review Skill** é uma ferramenta poderosa que:
- 🔍 Automatiza detecção de problemas
- 📋 Fornece feedback estruturado e actionable
- 🛡️ Melhora segurança e qualidade
- ⚡ Acelera tempo de review
- 📈 Documenta best practices

**Use-a todo dia para código melhor! 🚀**

