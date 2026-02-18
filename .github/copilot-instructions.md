# Copilot instructions for this repository

Purpose: help AI coding agents become immediately productive in this prompt-optimization project.

- **Big picture**: This repo pulls low-quality prompts from the LangSmith Prompt Hub, applies prompt-engineering techniques locally, pushes optimized prompts back to LangSmith, then evaluates them with an automated evaluation pipeline using LLM-as-judge metrics. Key scripts:
  - `src/pull_prompts.py` — pull prompt(s) from LangSmith (local: `prompts/bug_to_user_story_v1.yml`).
  - `src/push_prompts.py` — push optimized prompt YAML (`prompts/bug_to_user_story_v2.yml`) to the Hub (publishes public prompt, metadata includes `techniques_applied`).
  - `src/evaluate.py` — creates/updates LangSmith dataset from `datasets/bug_to_user_story.jsonl`, pulls prompt from the Hub, runs examples and computes metrics in `src/metrics.py`.
  - `src/metrics.py` — implements LLM-as-judge evaluators (F1, Clarity, Precision, Tone, etc.). These expect evaluator LLM responses to be valid JSON (the code will try to extract JSON if extra text is present).
  - `src/utils.py` — helper functions used across scripts (YAML load/save, env checks, `get_llm`, `validate_prompt_structure`).

- **Where to change prompts and tests**:
  - Edit `prompts/bug_to_user_story_v2.yml` for optimized prompt versions.
  - Implement/complete tests in `tests/test_prompts.py` (placeholders exist) — use `utils.validate_prompt_structure` and `yaml.safe_load` to assert required fields.

- **Environment & runtime**:
  - Required env vars (minimum): `LANGSMITH_API_KEY`, `LLM_PROVIDER`.
  - Provider-specific keys: `OPENAI_API_KEY` (when `LLM_PROVIDER=openai`) or `GOOGLE_API_KEY` (when `LLM_PROVIDER=google`).
  - Optional vars: `LLM_MODEL`, `EVAL_MODEL`, `LANGCHAIN_PROJECT`.
  - Install and run:

    ```bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    pip install -r requirements.txt
    ```

    Common commands:
    ```bash
    python src/pull_prompts.py   # pull initial prompts
    python src/push_prompts.py   # push optimized prompts
    python src/evaluate.py       # run evaluation pipeline
    pytest tests/test_prompts.py # run validation tests
    ```

- **Project-specific conventions & patterns**:
  - Prompt YAML must include these fields: `description`, `system_prompt`, `version`, and `techniques_applied` (see `utils.validate_prompt_structure`). Agents should not alter the evaluation dataset in `datasets/`.
  - Push naming convention: push prompts under a versioned name such as `{your_username}/bug_to_user_story_v2`. `evaluate.py` expects to pull `bug_to_user_story_v2` (ensure names match the Hub entry).
  - Evaluation LLMs are separated from generation LLMs: use `get_llm()` for generation and `get_eval_llm()` / `EVAL_MODEL` for the LLM-as-judge.
  - Evaluator prompts in `src/metrics.py` instruct LLM to return JSON only — keep evaluator prompts strict and return valid JSON (the repo attempts to extract JSON if extra text exists, but prefer clean JSON).
  - Deterministic evaluation: both `get_llm` and evaluation code use `temperature=0` by default for reproducible scoring.

- **Integration points and external dependencies**:
  - LangSmith: `langsmith.Client()` is used to create datasets and list/create examples. The code uses `langchain.hub.pull()` to fetch prompts and `langchain`/`langsmith` libraries to push and evaluate.
  - LLM Providers: configured via `LLM_PROVIDER`; supported values: `openai` or `google` (Gemini). Ensure provider API keys are present in `.env`.

- **What agents should do first (recommended minimal checklist)**:
  1. Open `README.md` and confirm environment steps and dataset presence.
  2. Implement or finish `src/pull_prompts.py` and `src/push_prompts.py` helpers if missing (they are skeletons here).
  3. Edit `prompts/bug_to_user_story_v2.yml` with at least 2 prompt-engineering techniques applied and include few-shot examples.
  4. Implement the tests in `tests/test_prompts.py` and run `pytest` locally.
  5. Run `python src/push_prompts.py` and `python src/evaluate.py` to validate behavior against LangSmith.

- **Important notes & gotchas**:
  - Do not modify `datasets/bug_to_user_story.jsonl` — evaluation expects the original dataset.
  - The code expects prompt objects in the Hub to be pullable by `hub.pull(name)`; if `push_prompts.py` publishes under a namespaced username, `evaluate.py` may need the exact short name; ensure names align.
  - Evaluator LLM responses must be JSON-parseable; when testing locally, use small example inputs to validate parsing logic in `src/metrics.py` and `src/utils.py`.

If anything in these instructions is unclear or you want the file to include example YAML snippets or test implementations, tell me which section to expand and I'll iterate.
