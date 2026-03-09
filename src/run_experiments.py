"""
Cria experimentos no LangSmith usando datasets existentes e avaliadores customizados.

Uso:
  python src/run_experiments.py

Config via .env (opcional):
  EXPERIMENT_DATASET_IDS=19af14cd-0293-4565-bdbd-1799a1cb6670,ee449d82-1cd8-41de-a0a2-5433232cf942
  EXPERIMENT_MAX_EXAMPLES=15
  EXPERIMENT_PREFIX=bug-to-user-story
  EVAL_PROMPT_NAME=viviane-pereira/viviane-pereira
"""

import os
from datetime import datetime
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from langsmith.evaluation import evaluate

from metrics import (
    evaluate_acceptance_criteria_score,
    evaluate_clarity,
    evaluate_completeness_score,
    evaluate_f1_score,
    evaluate_precision,
    evaluate_tone_score,
    evaluate_user_story_format_score,
)
from utils import check_env_vars, get_llm

load_dotenv()


def _question_from_inputs(inputs: Dict[str, Any]) -> str:
    return str(
        inputs.get("bug_report")
        or inputs.get("question")
        or inputs.get("pr_title")
        or ""
    )


def _reference_from_outputs(reference_outputs: Dict[str, Any] | None) -> str:
    if not reference_outputs:
        return ""
    return str(reference_outputs.get("reference") or "")


def _answer_from_outputs(outputs: Dict[str, Any] | None) -> str:
    if not outputs:
        return ""
    return str(outputs.get("answer") or "")


def make_target(prompt_name: str):
    llm = get_llm(temperature=0)
    prompt = hub.pull(prompt_name)
    chain = prompt | llm

    def target(inputs: Dict[str, Any]) -> Dict[str, Any]:
        response = chain.invoke(inputs)
        content = getattr(response, "content", str(response))
        return {"answer": content}

    return target


def evaluator_f1(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]):
    result = evaluate_f1_score(_question_from_inputs(inputs), _answer_from_outputs(outputs), _reference_from_outputs(reference_outputs))
    return {"key": "f1_score", "score": float(result.get("score", 0.0)), "comment": result.get("reasoning", "")}


def evaluator_clarity(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]):
    result = evaluate_clarity(_question_from_inputs(inputs), _answer_from_outputs(outputs), _reference_from_outputs(reference_outputs))
    return {"key": "clarity", "score": float(result.get("score", 0.0)), "comment": result.get("reasoning", "")}


def evaluator_precision(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]):
    result = evaluate_precision(_question_from_inputs(inputs), _answer_from_outputs(outputs), _reference_from_outputs(reference_outputs))
    return {"key": "precision", "score": float(result.get("score", 0.0)), "comment": result.get("reasoning", "")}


def evaluator_tone(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]):
    result = evaluate_tone_score(_question_from_inputs(inputs), _answer_from_outputs(outputs), _reference_from_outputs(reference_outputs))
    return {"key": "tone_score", "score": float(result.get("score", 0.0)), "comment": result.get("reasoning", "")}


def evaluator_acceptance(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]):
    result = evaluate_acceptance_criteria_score(_question_from_inputs(inputs), _answer_from_outputs(outputs), _reference_from_outputs(reference_outputs))
    return {"key": "acceptance_criteria_score", "score": float(result.get("score", 0.0)), "comment": result.get("reasoning", "")}


def evaluator_user_story_format(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]):
    result = evaluate_user_story_format_score(_question_from_inputs(inputs), _answer_from_outputs(outputs), _reference_from_outputs(reference_outputs))
    return {"key": "user_story_format_score", "score": float(result.get("score", 0.0)), "comment": result.get("reasoning", "")}


def evaluator_completeness(inputs: Dict[str, Any], outputs: Dict[str, Any], reference_outputs: Dict[str, Any]):
    result = evaluate_completeness_score(_question_from_inputs(inputs), _answer_from_outputs(outputs), _reference_from_outputs(reference_outputs))
    return {"key": "completeness_score", "score": float(result.get("score", 0.0)), "comment": result.get("reasoning", "")}


def _dataset_ids() -> List[str]:
    configured = os.getenv(
        "EXPERIMENT_DATASET_IDS",
        "19af14cd-0293-4565-bdbd-1799a1cb6670,ee449d82-1cd8-41de-a0a2-5433232cf942",
    )
    return [item.strip() for item in configured.split(",") if item.strip()]


def main() -> int:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    required_vars = ["LANGSMITH_API_KEY", "LLM_PROVIDER"]
    if provider == "openai":
        required_vars.append("OPENAI_API_KEY")
    else:
        required_vars.append("GOOGLE_API_KEY")

    if not check_env_vars(required_vars):
        return 1

    client = Client()
    prompt_name = os.getenv("EVAL_PROMPT_NAME") or os.getenv("PUSH_PROMPT_NAME") or "viviane-pereira/viviane-pereira"
    max_examples = int(os.getenv("EXPERIMENT_MAX_EXAMPLES", "15"))
    prefix = os.getenv("EXPERIMENT_PREFIX", "bug-to-user-story")

    target = make_target(prompt_name)
    evaluators = [
        evaluator_f1,
        evaluator_clarity,
        evaluator_precision,
        evaluator_tone,
        evaluator_acceptance,
        evaluator_user_story_format,
        evaluator_completeness,
    ]

    print(f"Prompt avaliado: {prompt_name}")
    print(f"Max exemplos por dataset: {max_examples}")

    for dataset_id in _dataset_ids():
        dataset = client.read_dataset(dataset_id=dataset_id)
        examples = list(client.list_examples(dataset_id=dataset_id))
        selected = examples[:max_examples]

        experiment_prefix = f"{prefix}-{dataset.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        print("=" * 70)
        print(f"Dataset: {dataset.name} ({dataset_id})")
        print(f"Exemplos: {len(selected)}/{len(examples)}")
        print(f"Experiment prefix: {experiment_prefix}")

        results = evaluate(
            target,
            data=selected,
            evaluators=evaluators,
            experiment_prefix=experiment_prefix,
            max_concurrency=1,
        )

        experiment_name = getattr(results, "experiment_name", None)
        if experiment_name:
            print(f"✅ Experimento criado: {experiment_name}")
        else:
            print("✅ Experimento executado com sucesso")

    print("\nConcluído: experimentos e avaliadores executados no LangSmith.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
