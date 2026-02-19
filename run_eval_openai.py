"""
Wrapper script to run evaluation with explicit OpenAI configuration.
This ensures environment variables are set before loading modules.
"""
import os
import sys
import subprocess

# Set environment variables BEFORE importing anything else
os.environ["LLM_PROVIDER"] = "openai"
os.environ["LLM_MODEL"] = "gpt-4o-mini"
os.environ["EVAL_MODEL"] = "gpt-4o-mini"

# Now run evaluate.py in a subprocess with these env vars
result = subprocess.run([sys.executable, "src/evaluate.py"], env=os.environ)
sys.exit(result.returncode)
