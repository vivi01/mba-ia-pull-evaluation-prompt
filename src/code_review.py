#!/usr/bin/env python3
"""
Code Review Specialist Script - Implementação Prática da Skill

Este script automatiza análise de code review baseada na skill especializada,
aplicando dimensões de avaliação em arquivos Python e YAML do projeto.

Uso:
    python src/code_review.py [arquivo_ou_diretorio]
    python src/code_review.py src/                  # Revisar todos os .py
    python src/code_review.py prompts/              # Revisar todos os .yml
"""

import os
import sys

# Força UTF-8 encoding no Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None


class ReviewPriority(Enum):
    """Prioridades de feedback"""
    CRITICAL = "🔴 CRITICAL"
    HIGH = "🟠 HIGH"
    MEDIUM = "🟡 MEDIUM"
    LOW = "🟢 LOW"
    SUGGESTION = "💡 SUGGESTION"


@dataclass
class ReviewIssue:
    """Representa um issue encontrado no code review"""
    priority: ReviewPriority
    category: str
    file: str
    line: Optional[int] = None
    title: str = ""
    description: str = ""
    suggestion: str = ""
    code_snippet: str = ""

    def to_dict(self) -> Dict:
        return {
            "priority": self.priority.value,
            "category": self.category,
            "file": self.file,
            "line": self.line,
            "title": self.title,
            "description": self.description,
            "suggestion": self.suggestion,
            "code_snippet": self.code_snippet,
        }


class CodeReviewAnalyzer:
    """Analisador especializado em code review"""

    def __init__(self):
        self.issues: List[ReviewIssue] = []
        self.base_path = Path.cwd()

    def analyze_file(self, filepath: str) -> List[ReviewIssue]:
        """Analisa um arquivo específico"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

        if path.suffix == ".py":
            return self._analyze_python_file(path)
        elif path.suffix in [".yml", ".yaml"]:
            return self._analyze_yaml_file(path)
        else:
            print(f"⚠️  Tipo de arquivo não suportado: {path.suffix}")
            return []

    def analyze_directory(self, dirpath: str) -> List[ReviewIssue]:
        """Analisa todos os arquivos em um diretório"""
        path = Path(dirpath)
        all_issues = []

        for py_file in path.glob("**/*.py"):
            if "__pycache__" not in str(py_file):
                all_issues.extend(self._analyze_python_file(py_file))

        for yaml_file in path.glob("**/*.yml"):
            all_issues.extend(self._analyze_yaml_file(yaml_file))

        for yaml_file in path.glob("**/*.yaml"):
            all_issues.extend(self._analyze_yaml_file(yaml_file))

        return all_issues

    def _analyze_python_file(self, filepath: Path) -> List[ReviewIssue]:
        """Análise especializada de arquivos Python"""
        issues = []
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
        except Exception as e:
            return [ReviewIssue(
                priority=ReviewPriority.HIGH,
                category="IO Error",
                file=str(filepath),
                title="Erro ao ler arquivo",
                description=str(e)
            )]

        # 1. Segurança: Detectar API keys
        issues.extend(self._check_security(filepath, content))

        # 2. Imports
        issues.extend(self._check_imports(filepath, content, lines))

        # 3. Docstrings
        issues.extend(self._check_docstrings(filepath, content, lines))

        # 4. Naming & Style
        issues.extend(self._check_naming_style(filepath, content, lines))

        # 5. LangChain/LangSmith patterns
        if "langchain" in content or "langsmith" in content:
            issues.extend(self._check_langchain_patterns(filepath, content, lines))

        # 6. Type hints
        issues.extend(self._check_type_hints(filepath, content, lines))

        # 7. Error handling
        issues.extend(self._check_error_handling(filepath, content, lines))

        return issues

    def _analyze_yaml_file(self, filepath: Path) -> List[ReviewIssue]:
        """Análise especializada de arquivos YAML (prompts)"""
        issues = []

        if yaml is None:
            return [ReviewIssue(
                priority=ReviewPriority.LOW,
                category="YAML Analysis",
                file=str(filepath),
                title="PyYAML não instalado",
                description="Install PyYAML, para análise mais detalhada de YAML",
                suggestion="pip install pyyaml"
            )]

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            return [ReviewIssue(
                priority=ReviewPriority.CRITICAL,
                category="YAML Syntax",
                file=str(filepath),
                title="YAML syntax error",
                description=str(e)
            )]
        except Exception as e:
            return [ReviewIssue(
                priority=ReviewPriority.HIGH,
                category="IO Error",
                file=str(filepath),
                title="Erro ao ler arquivo",
                description=str(e)
            )]

        # 1. Estrutura obrigatória
        issues.extend(self._check_prompt_structure(filepath, data))

        # 2. Few-shot examples
        issues.extend(self._check_few_shot_examples(filepath, data))

        # 3. Versioning
        issues.extend(self._check_prompt_versioning(filepath, data))

        # 4. Técnicas aplicadas
        issues.extend(self._check_techniques(filepath, data))

        return issues

    # ==================== VERIFICAÇÕES PYTHON ====================

    def _check_security(self, filepath: Path, content: str) -> List[ReviewIssue]:
        """Verifica problemas de segurança"""
        issues = []
        lines = content.split("\n")

        # Detectar API keys hardcoded
        api_key_patterns = [
            (r'sk-proj-[a-zA-Z0-9_-]{40,}', "OpenAI API key"),
            (r'AIzaSy[a-zA-Z0-9_-]{32,}', "Google API key"),
            (r'lsv2_pt_[a-zA-Z0-9_-]{32,}', "LangSmith API key"),
            (r'[\'\"]API_KEY[\'\"]?\s*[=:]\s*[\'\"](?![\w.]*[\'\"]$)', "Hardcoded API_KEY"),
        ]

        for line_no, line in enumerate(lines, 1):
            for pattern, key_type in api_key_patterns:
                if re.search(pattern, line) and not any(x in line for x in ["example", "placeholder", "..."]):
                    issues.append(ReviewIssue(
                        priority=ReviewPriority.CRITICAL,
                        category="Security",
                        file=str(filepath),
                        line=line_no,
                        title=f"Hardcoded {key_type} detected",
                        description="API keys devem estar APENAS em .env (adicionado ao .gitignore)",
                        suggestion="Mover para variáveis de ambiente usando os.getenv()",
                        code_snippet=line.strip()
                    ))

        # Verificar uso de .env
        if ".env" not in str(filepath) and "os.getenv" in content:
            return issues  # Ok, está usando variáveis de ambiente

        return issues

    def _check_imports(self, filepath: Path, content: str, lines: List[str]) -> List[ReviewIssue]:
        """Verifica organização de imports"""
        issues = []

        import_lines = [l for l in lines if l.strip().startswith("import ") or l.strip().startswith("from ")]
        
        # Detectar imports não utilizados (básico)
        for import_line in import_lines:
            # Extract module name
            if "import " in import_line:
                if " as " in import_line:
                    module = import_line.split(" as ")[-1].strip()
                else:
                    module = import_line.split("import ")[1].strip().split(",")[0].strip()
                
                # Procurar se é usado no arquivo
                if module and f"{module}." not in content and module not in ["*", "datetime", "json"]:
                    # Skip built-ins
                    if not any(x in module for x in ["typing", "abc", "collections"]):
                        # Pode ser positivo falso, então LOW priority
                        pass

        # Verificar ordem de imports (bons hábitos)
        std_imports = []
        third_party = []
        local_imports = []

        for line in import_lines:
            if "from . import" in line or "from .." in line:
                local_imports.append(line)
            elif any(pkg in line for pkg in ["langchain", "langsmith", "openai", "google"]):
                third_party.append(line)
            else:
                std_imports.append(line)

        # Sugerir organização se estiver desorganizado
        if not (std_imports + third_party + local_imports == import_lines):
            issues.append(ReviewIssue(
                priority=ReviewPriority.LOW,
                category="Code Style",
                file=str(filepath),
                title="Imports não organizados",
                description="Imports devem estar na ordem: stdlib → third-party → local",
                suggestion="Reorganizar imports seguindo padrão PEP 8"
            ))

        return issues

    def _check_docstrings(self, filepath: Path, content: str, lines: List[str]) -> List[ReviewIssue]:
        """Verifica presença e qualidade de docstrings"""
        issues = []

        # Funções e classes sem docstring
        in_def = False
        has_docstring = False
        def_line = 0

        for i, line in enumerate(lines, 1):
            if re.match(r'^\s*(def|class) ', line):
                if in_def and not has_docstring and "test_" not in line:
                    issues.append(ReviewIssue(
                        priority=ReviewPriority.MEDIUM,
                        category="Documentation",
                        file=str(filepath),
                        line=def_line,
                        title="Docstring ausente",
                        description=f"Função/classe sem documentação",
                        suggestion='Adicionar docstring no formato Google/NumPy'
                    ))
                in_def = True
                def_line = i
                has_docstring = False
            elif in_def and ('"""' in line or "'''" in line):
                has_docstring = True

        return issues

    def _check_naming_style(self, filepath: Path, content: str, lines: List[str]) -> List[ReviewIssue]:
        """Verifica convenções de naming"""
        issues = []

        # Variáveis com nomes muito genéricos
        generic_names = ["x", "y", "z", "temp", "tmp", "data1", "data2"]
        
        for i, line in enumerate(lines, 1):
            for name in generic_names:
                if re.search(rf'\b{name}\s*=', line) and "__" not in line:
                    issues.append(ReviewIssue(
                        priority=ReviewPriority.LOW,
                        category="Naming",
                        file=str(filepath),
                        line=i,
                        title=f"Variável genérica: '{name}'",
                        description="Nome não é descritivo",
                        suggestion="Use nomes mais específicos (e.g., 'prompt_data' em vez de 'data')"
                    ))

        return issues

    def _check_langchain_patterns(self, filepath: Path, content: str, lines: List[str]) -> List[ReviewIssue]:
        """Análise específica de padrões LangChain/LangSmith"""
        issues = []

        # Verificar hub.pull sem try-except
        for i, line in enumerate(lines, 1):
            if "hub.pull" in line and "try" not in lines[max(0, i-3):i]:
                issues.append(ReviewIssue(
                    priority=ReviewPriority.HIGH,
                    category="LangChain Integration",
                    file=str(filepath),
                    line=i,
                    title="hub.pull sem tratamento de erro",
                    description="hub.pull() pode falhar se prompt não existir",
                    suggestion="Envolver em try-except com mensagem de erro clara"
                ))

            # Verificar Client() sem validação de credenciais
            if "Client()" in line:
                issues.append(ReviewIssue(
                    priority=ReviewPriority.MEDIUM,
                    category="LangChain Integration",
                    file=str(filepath),
                    line=i,
                    title="Cliente LangSmith sem validação",
                    description="Deve validar LANGSMITH_API_KEY antes",
                    suggestion="Adicionar check_env_vars() antes de Client()"
                ))

        return issues

    def _check_type_hints(self, filepath: Path, content: str, lines: List[str]) -> List[ReviewIssue]:
        """Verifica presença de type hints"""
        issues = []

        for i, line in enumerate(lines, 1):
            if re.match(r'\s*def ', line) and "->" not in line and "test_" not in line:
                # Função sem return type hint
                if "self" not in line or ":" not in line:
                    issues.append(ReviewIssue(
                        priority=ReviewPriority.LOW,
                        category="Type Hints",
                        file=str(filepath),
                        line=i,
                        title="Type hints ausentes",
                        description="Função deveria ter anotações de tipo",
                        suggestion="Adicionar type hints: def func(param: str) -> dict:"
                    ))

        return issues

    def _check_error_handling(self, filepath: Path, content: str, lines: List[str]) -> List[ReviewIssue]:
        """Verifica tratamento de erros"""
        issues = []

        for i, line in enumerate(lines, 1):
            # Detectar bare except
            if "except:" in line or "except Exception:" in line:
                issues.append(ReviewIssue(
                    priority=ReviewPriority.MEDIUM,
                    category="Error Handling",
                    file=str(filepath),
                    line=i,
                    title="Exceção muito genérica",
                    description="Usar 'except Exception' ou 'except:' captura tudo",
                    suggestion="Especificar exceção esperada: 'except FileNotFoundError:'"
                ))

        return issues

    # ==================== VERIFICAÇÕES YAML/PROMPTS ====================

    def _check_prompt_structure(self, filepath: Path, data: Dict) -> List[ReviewIssue]:
        """Verifica estrutura obrigatória do prompt"""
        issues = []
        required_fields = ["system_prompt", "version", "techniques_applied", "description"]

        for field in required_fields:
            if field not in data:
                issues.append(ReviewIssue(
                    priority=ReviewPriority.CRITICAL,
                    category="Prompt Structure",
                    file=str(filepath),
                    title=f"Campo obrigatório ausente: '{field}'",
                    description=f"Prompt YAML deve conter: {', '.join(required_fields)}",
                    suggestion=f"Adicionar campo '{field}' ao prompt YAML"
                ))
            elif not data[field] or (isinstance(data[field], str) and len(data[field].strip()) == 0):
                issues.append(ReviewIssue(
                    priority=ReviewPriority.HIGH,
                    category="Prompt Structure",
                    file=str(filepath),
                    title=f"Campo vazio: '{field}'",
                    description=f"'{field}' não pode estar vazio",
                    suggestion=f"Preencher '{field}' com conteúdo significativo"
                ))

        return issues

    def _check_few_shot_examples(self, filepath: Path, data: Dict) -> List[ReviewIssue]:
        """Verifica qualidade dos exemplos few-shot"""
        issues = []

        if "examples" not in data:
            issues.append(ReviewIssue(
                priority=ReviewPriority.HIGH,
                category="Few-Shot Learning",
                file=str(filepath),
                title="Sem exemplos few-shot",
                description="Prompts de qualidade devem incluir exemplos input/output",
                suggestion="Adicionar seção 'examples' com pelo menos 2-3 casos de uso"
            ))
        else:
            examples = data["examples"]
            if not isinstance(examples, list) or len(examples) < 2:
                issues.append(ReviewIssue(
                    priority=ReviewPriority.MEDIUM,
                    category="Few-Shot Learning",
                    file=str(filepath),
                    title="Few-shot examples insuficientes",
                    description="Recomenda-se 2-3 exemplos para melhor performance",
                    suggestion="Expandir exemplos para cobrir casos comuns e edge cases"
                ))

            # Verificar qualidade dos exemplos
            for i, ex in enumerate(examples):
                if not isinstance(ex, dict):
                    issues.append(ReviewIssue(
                        priority=ReviewPriority.MEDIUM,
                        category="Few-Shot Learning",
                        file=str(filepath),
                        title=f"Exemplo #{i+1} mal formatado",
                        description="Cada exemplo deve ser um dicionário",
                        suggestion="Estruturar como: {input: '...', output: '...'}"
                    ))
                elif "input" not in ex or "output" not in ex:
                    issues.append(ReviewIssue(
                        priority=ReviewPriority.MEDIUM,
                        category="Few-Shot Learning",
                        file=str(filepath),
                        title=f"Exemplo #{i+1} incompleto",
                        description="Exemplo deve ter 'input' e 'output'",
                        suggestion="Adicionar ambos os campos para completar exemplo"
                    ))

        return issues

    def _check_prompt_versioning(self, filepath: Path, data: Dict) -> List[ReviewIssue]:
        """Verifica versioning consistente"""
        issues = []

        version = data.get("version", "")
        filename = filepath.name

        if not version:
            issues.append(ReviewIssue(
                priority=ReviewPriority.HIGH,
                category="Versioning",
                file=str(filepath),
                title="Versão não definida",
                description="Campo 'version' é obrigatório",
                suggestion="Define versão: 'v1', 'v2', '1.0.0', etc."
            ))
        elif "v" not in str(version).lower():
            issues.append(ReviewIssue(
                priority=ReviewPriority.MEDIUM,
                category="Versioning",
                file=str(filepath),
                title="Formato de versão não padrão",
                description="Use padrão semântico: v1, v2, 1.0.0",
                suggestion=f"Reformatar versão para algo como 'v{version}'"
            ))

        # Verificar consistência entre filename e versão
        if "v1" in filename and "v2" in str(version):
            issues.append(ReviewIssue(
                priority=ReviewPriority.MEDIUM,
                category="Versioning",
                file=str(filepath),
                title="Inconsistência de versão",
                description="Versão no arquivo não combina com versão no YAML",
                suggestion="Manter consistência: bug_to_user_story_v2.yml deve ter version: v2"
            ))

        return issues

    def _check_techniques(self, filepath: Path, data: Dict) -> List[ReviewIssue]:
        """Verifica técnicas de prompt engineering aplicadas"""
        issues = []

        techniques = data.get("techniques_applied", [])

        if not techniques:
            issues.append(ReviewIssue(
                priority=ReviewPriority.HIGH,
                category="Prompt Engineering",
                file=str(filepath),
                title="Técnicas não documentadas",
                description="'techniques_applied' deve listar técnicas usadas",
                suggestion="Adicionar lista de técnicas: ['Few-shot Learning', 'Chain of Thought']"
            ))
        elif isinstance(techniques, list):
            if len(techniques) < 2:
                issues.append(ReviewIssue(
                    priority=ReviewPriority.MEDIUM,
                    category="Prompt Engineering",
                    file=str(filepath),
                    title="Poucas técnicas aplicadas",
                    description="Requisito mínimo: 2 técnicas de prompt engineering",
                    suggestion="Aplicar e documentar pelo menos 2 técnicas diferentes"
                ))

            # Verificar técnicas conhecidas
            valid_techniques = [
                "Few-shot Learning",
                "Chain of Thought",
                "Tree of Thought",
                "Skeleton of Thought",
                "ReAct",
                "Role Prompting"
            ]

            for tech in techniques:
                if not any(vt.lower() in str(tech).lower() for vt in valid_techniques):
                    issues.append(ReviewIssue(
                        priority=ReviewPriority.LOW,
                        category="Prompt Engineering",
                        file=str(filepath),
                        title=f"Técnica desconhecida: '{tech}'",
                        description=f"Técnica pode ser pouco clara ou não reconhecida",
                        suggestion=f"Usar nomes padrão do curso ou descrever melhor"
                    ))

        return issues

    # ==================== RELATÓRIO ====================

    def generate_report(self, issues: List[ReviewIssue]) -> str:
        """Gera relatório formatado dos issues"""
        
        if not issues:
            return "✅ Nenhum issue encontrado! Código está limpo.\n"

        report = []
        report.append("\n" + "=" * 80)
        report.append("🔍 CODE REVIEW REPORT")
        report.append("=" * 80 + "\n")

        # Agrupar por prioridade
        by_priority = {}
        for issue in issues:
            if issue.priority not in by_priority:
                by_priority[issue.priority] = []
            by_priority[issue.priority].append(issue)

        # Exibir por prioridade (CRITICAL primeiro)
        priority_order = [ReviewPriority.CRITICAL, ReviewPriority.HIGH, 
                         ReviewPriority.MEDIUM, ReviewPriority.LOW, ReviewPriority.SUGGESTION]

        total_count = {
            "critical": len(by_priority.get(ReviewPriority.CRITICAL, [])),
            "high": len(by_priority.get(ReviewPriority.HIGH, [])),
            "medium": len(by_priority.get(ReviewPriority.MEDIUM, [])),
            "low": len(by_priority.get(ReviewPriority.LOW, [])),
            "suggestion": len(by_priority.get(ReviewPriority.SUGGESTION, [])),
        }

        # Summary
        report.append(f"📊 RESUMO")
        report.append(f"  - Critical:  {total_count['critical']} issue(ns)")
        report.append(f"  - High:      {total_count['high']} issue(ns)")
        report.append(f"  - Medium:    {total_count['medium']} issue(ns)")
        report.append(f"  - Low:       {total_count['low']} issue(ns)")
        report.append(f"  - Suggestion: {total_count['suggestion']} issue(ns)")
        report.append(f"  - TOTAL:     {len(issues)} issue(ns)\n")

        # Detalhes por prioridade
        for priority in priority_order:
            if priority in by_priority:
                report.append(f"\n{priority.value} ({len(by_priority[priority])} issues)")
                report.append("-" * 80)
                
                for issue in by_priority[priority]:
                    report.append(f"\n📄 {issue.file}" + (f":{issue.line}" if issue.line else ""))
                    report.append(f"   Categoria: {issue.category}")
                    report.append(f"   Título: {issue.title}")
                    report.append(f"   Descrição: {issue.description}")
                    
                    if issue.code_snippet:
                        report.append(f"   Código: {issue.code_snippet}")
                    
                    if issue.suggestion:
                        report.append(f"   ✨ Sugestão: {issue.suggestion}")

        report.append("\n" + "=" * 80)
        report.append(f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80 + "\n")

        return "\n".join(report)

    def save_report_json(self, issues: List[ReviewIssue], output_path: str = "code_review_report.json"):
        """Salva relatório em formato JSON"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_issues": len(issues),
            "summary": {
                "critical": len([i for i in issues if i.priority == ReviewPriority.CRITICAL]),
                "high": len([i for i in issues if i.priority == ReviewPriority.HIGH]),
                "medium": len([i for i in issues if i.priority == ReviewPriority.MEDIUM]),
                "low": len([i for i in issues if i.priority == ReviewPriority.LOW]),
                "suggestion": len([i for i in issues if i.priority == ReviewPriority.SUGGESTION]),
            },
            "issues": [issue.to_dict() for issue in issues]
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"✅ Relatório salvo em: {output_path}")


def main():
    """Função principal"""
    
    if len(sys.argv) < 2:
        print("📋 Uso: python src/code_review.py [arquivo_ou_diretorio]")
        print("\nExemplos:")
        print("  python src/code_review.py src/evaluate.py")
        print("  python src/code_review.py src/")
        print("  python src/code_review.py prompts/bug_to_user_story_v2.yml")
        sys.exit(1)

    target = sys.argv[1]
    
    analyzer = CodeReviewAnalyzer()
    
    print(f"\n🔍 Analisando: {target}\n")

    try:
        if Path(target).is_dir():
            issues = analyzer.analyze_directory(target)
        else:
            issues = analyzer.analyze_file(target)

        # Exibir relatório
        report = analyzer.generate_report(issues)
        print(report)

        # Salvar relatório JSON
        analyzer.save_report_json(issues)

        # Exit code baseado em issues críticos
        critical_count = len([i for i in issues if i.priority == ReviewPriority.CRITICAL])
        sys.exit(critical_count)

    except Exception as e:
        print(f"❌ Erro ao analisar: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
