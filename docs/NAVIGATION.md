# 📚 Mapa de Navegação: Code Review Skill

## 🎯 Comece por Aqui

Escolha seu perfil e siga o caminho recomendado:

```
┌─────────────────────────────────────────────────────────────┐
│         VOCÊ É NOVO NA SKILL? COMECE AQUI!                 │
└─────────────────────────────────────────────────────────────┘

1️⃣  LER: docs/CODE_REVIEW_PRESENTATION.md (5 min)
    └─ Overview executivo da skill

2️⃣  EXECUTAR: python src/code_review.py src/ (1 min)  
    └─ Ver funcionando na prática

3️⃣  LER: docs/CODE_REVIEW_GUIDE.md - Seção 1-2 (10 min)
    └─ Como usar todo dia

4️⃣  EXPLORAR: docs/CODE_REVIEW_EXAMPLES.md (10 min)
    └─ Exemplos práticos de correções

✅ PRONTO! Você domina a skill. Continue explorando conforme necessário.
```

---

## 👥 Paths por Perfil

### 👔 Product Manager / Tech Lead

**Objetivo:** Entender estratégia e implementar no time

**Path Recomendado:**
```
1. Ler: docs/CODE_REVIEW_PRESENTATION.md (5 min)
   └─ TL;DR, ROI, benchmarks

2. Visualizar: docs/CODE_REVIEW_EXAMPLES.md → Cenário 5 (3 min)
   └─ Como funciona GitHub Actions (automático)

3. Implementar: Copiar .github/workflows/code-review-ci.yml (10 min)
   └─ Setup automático no time

4. Comunicar: Compartilhar CODE_REVIEW_PRESENTATION.md com time (5 min)
   └─ Explicar benefícios esperados

Total: ~25 minutos
Status: ✅ Implementado no time
```

**Próximas Ações:**
- [ ] Implementar GitHub Actions
- [ ] Comunicar ao time em standup
- [ ] Acompanhar métricas de melhoria
- [ ] Fazer review de segurança (API keys)

---

### 💻 Developer (Iniciante)

**Objetivo:** Aprender a usar no seu workflow diário

**Path Recomendado:**
```
1. Ler: docs/CODE_REVIEW_PRESENTATION.md (5 min)
   └─ Entender o quê e por quê

2. Ler: docs/CODE_REVIEW_GUIDE.md - Seção 1-3 (15 min)
   └─ Como usar: rápido, daily, integração

3. Executar: python src/code_review.py src/utils.py (1 min)
   └─ Testar no seu código

4. Ler: docs/CODE_REVIEW_EXAMPLES.md → Cenários 1-2 (10 min)
   └─ Exemplos de problemas reais

5. Praticar: python src/code_review.py prompts/ (1 min)
   └─ Rodar em YAML também

6. Ler: docs/CODE_REVIEW_GUIDE.md - Seção 7-8 (10 min)
   └─ Como corrigir issues encontrados

Total: ~40 minutos
Status: ✅ Usando todo dia
```

**Próximas Ações:**
- [ ] Adicionar `python src/code_review.py .` ao seu pré-commit
- [ ] Usar antes de cada push
- [ ] Revisar issues encontrados
- [ ] Aprender melhorias sugeridas

---

### 🔐 DevOps / Infrastructure

**Objetivo:** Implementar automação em CI/CD

**Path Recomendado:**
```
1. Ler: .github/code-review-skill.md → Seção 6 (GitHub Actions) (10 min)
   └─ Template YAML pronto

2. Criar: .github/workflows/code-review-ci.yml (5 min)
   └─ Copiar template e customizar

3. Testar: Fazer PR de teste (2 min)
   └─ Ver automation rodando

4. Validar: Confirmar exit codes funcionando (2 min)
   └─ Bloqueia PR em caso de CRITICAL? ✅

5. Documentar: Comunicar ao time (5 min)
   └─ Como ler feedback automático

Total: ~20 minutos
Status: ✅ Automação ativa
```

**Próximas Ações:**
- [ ] Implementar GitHub Actions
- [ ] Testar com PR dummy
- [ ] Ajustar exit codes conforme política
- [ ] Monitorar primeira semana

---

### 🎓 Code Reviewer / QA

**Objetivo:** Usar skill para fazer reviews mais efetivos

**Path Recomendado:**
```
1. Ler: .github/code-review-skill.md - Completo (30 min)
   └─ Framework de 6 dimensões, checklist, exemplos

2. Ler: docs/CODE_REVIEW_GUIDE.md - Completo (20 min)
   └─ Todos os detalhes de uso

3. Ler: docs/CODE_REVIEW_EXAMPLES.md - Completo (15 min)
   └─ Todos os 8 cenários

4. Praticar: Rodar em código real (5 min)
   └─ python src/code_review.py .

5. Usar com PR: Aplicar framework em PRs (ongoing)
   └─ Usar checklist + dimensões

Total: ~70 minutos
Status: ✅ Expert em skill
```

**Próximas Ações:**
- [ ] Conhecer todos os 6 frameworks
- [ ] Fazer reviews estruturados
- [ ] Usar templates de feedback
- [ ] Treinar outros reviewers

---

## 📂 Estrutura de Arquivos

```
code-review-skill/
│
├── 📄 ESTA PÁGINA (YOU ARE HERE)
│   └─ Mapa de navegação para todos os arquivos
│
├── 🔍 .github/code-review-skill.md (Framework)
│   ├─ 1.  Princípios (8 items)
│   ├─ 2.  Framework (6 dimensões)
│   ├─ 3.  Guia por arquivo
│   ├─ 4.  Checklist completo
│   ├─ 5.  Exemplos (5 cenários)
│   ├─ 6.  Integração GitHub Actions
│   ├─ 7.  Template PR
│   ├─ 8.  Métricas
│   ├─ 9.  Ferramentas recomendadas
│   └─ 10. Treinamento contínuo
│
├── 💻 src/code_review.py (Automação)
│   ├─ Análise Python
│   ├─ Análise YAML
│   ├─ Relatório estruturado
│   └─ JSON export
│
├── 📖 docs/CODE_REVIEW_GUIDE.md (Prático)
│   ├─ 1.  Quick start
│   ├─ 2.  Fluxo integrado
│   ├─ 3.  Exemplos (3+)
│   ├─ 4.  GitHub Actions
│   ├─ 5.  Copilot integration
│   ├─ 6.  Métricas
│   ├─ 7.  Checklist
│   ├─ 8.  Correções
│   ├─ 9.  Benchmarks
│   ├─ 10. Troubleshooting
│   └─ 11. Próximos passos
│
├── 🎬 docs/CODE_REVIEW_EXAMPLES.md (Exemplos)
│   ├─ 1.  Revisar Python (LangChain)
│   ├─ 2.  Revisar YAML (Prompts)
│   ├─ 3.  Revisar Testes
│   ├─ 4.  Scan completo
│   ├─ 5.  GitHub Actions
│   ├─ 6.  Segurança (API keys)
│   ├─ 7.  Documentação
│   └─ 8.  Daily workflow
│
├── 📋 docs/CODE_REVIEW_SKILL_SUMMARY.md (Sumário)
│   ├─ Arquivos criados
│   ├─ Como usar agora
│   ├─ Dimensões implementadas
│   ├─ Fluxo integrado
│   ├─ Benefícios esperados
│   └─ Próximos passos
│
├── 🎯 docs/CODE_REVIEW_PRESENTATION.md (Executivo)
│   ├─ TL;DR
│   ├─ O que você recebeu
│   ├─ Use cases
│   ├─ Dimensões
│   ├─ Quick start
│   ├─ Benchmarks
│   ├─ FAQ
│   └─ Próximas ações
│
└── 📚 docs/NAVIGATION.md (Este arquivo!)
    └─ Mapa de navegação
```

---

## 🔍 Buscar Informação Específica

### "Como usar a skill?"
→ `docs/CODE_REVIEW_GUIDE.md` - Seção 1-2

### "Quais dimensões são avaliadas?"
→ `.github/code-review-skill.md` - Seção 2

### "Exemplos reais de problemas"
→ `docs/CODE_REVIEW_EXAMPLES.md` - Todos os 8

### "Como integrar com GitHub?"
→ `.github/code-review-skill.md` - Seção 6  
→ `docs/CODE_REVIEW_GUIDE.md` - Seção 4

### "Template para PR"
→ `.github/code-review-skill.md` - Seção 6.3

### "Qual é o ROI?"
→ `docs/CODE_REVIEW_PRESENTATION.md` - Seção "Benchmarks"

### "Como corrigir tal problema?"
→ `docs/CODE_REVIEW_EXAMPLES.md` - Seção específica

### "Checklist antes de commitar"
→ `docs/CODE_REVIEW_GUIDE.md` - Seção 6

### "Como usar com Copilot?"
→ `docs/CODE_REVIEW_GUIDE.md` - Seção 5

### "Troubleshooting"
→ `docs/CODE_REVIEW_GUIDE.md` - Seção 10

---

## ⏱️ Tempo de Leitura

```
Por Arquivo:
├─ .github/code-review-skill.md        ~30 min (framework completo)
├─ src/code_review.py                   ~5 min (entender código)
├─ docs/CODE_REVIEW_GUIDE.md           ~20 min (guia prático)
├─ docs/CODE_REVIEW_EXAMPLES.md        ~15 min (exemplos)
├─ docs/CODE_REVIEW_SKILL_SUMMARY.md   ~10 min (resumo)
├─ docs/CODE_REVIEW_PRESENTATION.md    ~10 min (executivo)
└─ docs/NAVIGATION.md                   ~5 min (este arquivo)
  ─────────────────────────────────────────────
  Total: ~95 minutos (leitura completa)

RECOMENDADO:
- Tech Lead: 30 minutos (Presentation + Examples)
- Developer: 40 minutos (Guide + Examples + Practice)
- DevOps: 20 minutos (Skill + GitHub Actions)
```

---

## 🎯 Quick Reference (Comandos Principais)

```bash
# Revisar arquivo Python específico
python src/code_review.py src/evaluate.py

# Revisar todos os Python
python src/code_review.py src/

# Revisar prompts YAML
python src/code_review.py prompts/

# Revisar tudo
python src/code_review.py .

# Ver relatório JSON
cat code_review_report.json

# Usar em GitHub Actions
Copiar .github/workflows/code-review-ci.yml (template em Seção 6)

# Usar com Copilot
Abrir arquivo + Ctrl+Shift+P + "Copilot: Comments"
```

---

## 🔗 Relacionamentos Entre Arquivos

```
.github/code-review-skill.md (FRAMEWORK)
    │
    ├─→ docs/CODE_REVIEW_GUIDE.md (PRÁTICO)
    │   └─→ docs/CODE_REVIEW_EXAMPLES.md (EXEMPLOS)
    │
    ├─→ src/code_review.py (AUTOMAÇÃO)
    │   └─→ Gera: code_review_report.json
    │
    └─→ GitHub Actions CI/CD
        └─→ Automático a cada PR

docs/CODE_REVIEW_PRESENTATION.md (EXECUTIVO)
    └─→ TL;DR de tudo acima

docs/NAVIGATION.md (ESTE ARQUIVO)
    └─→ Guia para navegar tudo
```

---

## ❓ FAQ Rápido

| Pergunta | Resposta | Arquivo |
|----------|----------|---------|
| Como começo? | Ler Presentation + rodar script | CODE_REVIEW_PRESENTATION.md |
| Como uso todo dia? | Uma linha antes de commit | CODE_REVIEW_GUIDE.md §1 |
| Quais issues detecta? | 6 dimensões de qualidade | code-review-skill.md §2 |
| Exemplos de problemas? | 8 cenários reais com fix | CODE_REVIEW_EXAMPLES.md |
| Como integrar GitHub? | Template CI/CD pronto | code-review-skill.md §6 |
| Quanto tempo economiza? | ~20h/mês em debug | CODE_REVIEW_PRESENTATION.md |
| Funciona no Windows? | Sim, UTF-8 garantido | src/code_review.py |
| E no GitHub Actions? | Sim, template incluído | code-review-skill.md |
| Como customizar regras? | Editar src/code_review.py | CODE_REVIEW_GUIDE.md |
| Precisa de dependências? | Só stdlib, opcional YAML | CODE_REVIEW_GUIDE.md §7 |

---

## 🚀 Decisão Árvore: O Que Ler/Fazer

```
┌─ VOCÊ QUER...
│
├─ "Quickstart" (5-10 min)
│  └─ Ler: CODE_REVIEW_PRESENTATION.md
│     Fazer: python src/code_review.py src/
│
├─ "Usar todo dia" (20-30 min)
│  └─ Ler: CODE_REVIEW_GUIDE.md §1-7
│     Praticar: docs/CODE_REVIEW_EXAMPLES.md
│
├─ "Implementar no time" (30-40 min)
│  └─ Ler: code-review-skill.md (COMPLETO)
│     Fazer: .github/workflows/code-review-ci.yml
│
├─ "Entender a fundo" (90 min)
│  └─ Ler: TUDO na ordem numérica
│     Praticar: Todos os exemplos
│
└─ "Troubleshoot algo" (5 min)
   └─ Buscar em: CODE_REVIEW_GUIDE.md §10 (Troubleshooting)
```

---

## 📞 Suporte Rápido

**Problema:** "Script não roda"
→ Ver: `CODE_REVIEW_GUIDE.md` Seção 10

**Problema:** "Como corrigir issue X?"
→ Ver: `CODE_REVIEW_EXAMPLES.md` - Procure por "Cenário X"

**Problema:** "E na empresa Y?"
→ Customizar: `src/code_review.py` (trechos marcados como customizáveis)

**Problema:** "Preciso saber tudo"
→ Ler: `.github/code-review-skill.md` (framework completo)

---

## ✅ Checklist de Leitura

Marque conforme você lê:

- [ ] CODE_REVIEW_PRESENTATION.md (Overview)
- [ ] docs/CODE_REVIEW_GUIDE.md (Prático)
- [ ] docs/CODE_REVIEW_EXAMPLES.md (Exemplos)
- [ ] .github/code-review-skill.md (Profundo)
- [ ] src/code_review.py (Código)
- [ ] docs/CODE_REVIEW_SKILL_SUMMARY.md (Resumo)
- [ ] docs/NAVIGATION.md (Este - Mapa)

**Status:** Você leu:  `[ ] / 7 arquivos`

---

## 🎉 Conclusão

Você tem a **Skill de Code Review completa** com:
- ✅ Framework teórico (6 dimensões)
- ✅ Script automático (analisador)
- ✅ Documentação prática (guias)
- ✅ Exemplos reais (8 cenários)
- ✅ Integração GitHub (CI/CD)
- ✅ Mapa de navegação (este arquivo!)

**Próximo passo:** Escolha seu perfil acima e siga o path recomendado! 🚀

---

**Last Updated:** February 19, 2026  
**Version:** 1.0  
**Status:** ✅ Complete & Ready

