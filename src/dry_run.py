"""Local dry-run evaluator (mocked) to demonstrate pipeline without external APIs.

This script reads the optimized prompt YAML and the evaluation dataset, then
produces deterministic mock metrics and a JSON results file under `results/`.
"""
from pathlib import Path
import json
import yaml


def load_yaml(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_jsonl(p: Path):
    items = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def mock_metrics(prompt_meta: dict, n_examples: int):
    """Return deterministic mock metrics based on prompt version and dataset size."""
    version = str(prompt_meta.get("version", "v0"))
    base = 0.9 if version.endswith("2") else 0.6
    # Slight variation with number of examples
    delta = min(0.08, n_examples * 0.002)
    metrics = {
        "F1-Score": round(base + 0.02 + delta, 3),
        "Clarity": round(base + 0.03 + delta, 3),
        "Precision": round(base + 0.015 + delta, 3),
        "Tone Score": round(base + 0.025 + delta, 3),
        "Acceptance Criteria Score": round(base + 0.02 + delta, 3),
        "User Story Format Score": round(base + 0.02 + delta, 3),
        "Completeness Score": round(base + 0.01 + delta, 3),
    }
    return metrics


def main():
    repo_root = Path(__file__).parent.parent
    prompts_path = repo_root / "prompts" / "bug_to_user_story_v2.yml"
    dataset_path = repo_root / "datasets" / "bug_to_user_story.jsonl"
    out_dir = repo_root / "results"
    out_dir.mkdir(exist_ok=True)

    prompt = load_yaml(prompts_path)
    examples = load_jsonl(dataset_path)

    metrics = mock_metrics(prompt, len(examples))
    avg = round(sum(metrics.values()) / len(metrics), 3)
    verdict = "APROVADO" if all(v >= 0.9 for v in metrics.values()) else "FALHOU"

    result = {
        "prompt": prompts_path.name,
        "n_examples": len(examples),
        "metrics": metrics,
        "average": avg,
        "verdict": verdict,
    }

    out_file = out_dir / "dry_run_results.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Dry-run evaluation complete:")
    for k, v in metrics.items():
        print(f"- {k}: {v}")
    print(f"Average: {avg} — Verdict: {verdict}")
    print(f"Results written to: {out_file}")


if __name__ == "__main__":
    main()
