"""Lab 3.1 — Code-Repair Agent.
Receives a broken task, diagnoses it with pytest + flake8, asks the model
for TWO alternative fixes, tests each in isolation, and logs everything.

Usage:
    python repair_agent.py broken_tasks/task1
    python repair_agent.py broken_tasks/task1 broken_tasks/task2 ...
"""
import json, os, shutil, subprocess, sys, tempfile, time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=os.environ["OPENROUTER_API_KEY"])
DEFAULT_MODEL = os.environ.get("REPAIR_MODEL", "openai/gpt-4o-mini")
RESULTS = "results.jsonl"


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=120)
    return p.returncode, (p.stdout + p.stderr)[-3000:]


def diagnose(task_dir):
    """Tools of this agent: the test runner and the linter."""
    rc_t, out_t = run([sys.executable, "-m", "pytest", "-q"], task_dir)
    rc_l, out_l = run([sys.executable, "-m", "flake8", "task.py"], task_dir)
    return {"tests_pass": rc_t == 0, "pytest": out_t, "flake8": out_l}


def propose_fixes(code, diag, model):
    t0 = time.time()
    r = client.chat.completions.create(model=model, messages=[
        {"role": "system", "content":
         "You are a senior Python engineer. Given broken code and its "
         "diagnostics, identify the issues and produce exactly TWO "
         "alternative complete fixed versions of task.py. Keep the "
         "public function names and docstrings. Return STRICT JSON: "
         '{"issues": ["..."], "fixes": [{"explanation": "...", '
         '"code": "..."}, {"explanation": "...", "code": "..."}]}'},
        {"role": "user", "content":
         f"BROKEN task.py:\n```python\n{code}\n```\n\n"
         f"pytest output:\n{diag['pytest']}\n\n"
         f"flake8 output:\n{diag['flake8']}"}])
    latency = round(time.time() - t0, 2)
    txt = r.choices[0].message.content.strip()
    txt = txt.removeprefix("```json").removeprefix("```").removesuffix("```")
    data = json.loads(txt)
    return data, latency, r.usage.prompt_tokens, r.usage.completion_tokens


def test_fix(task_dir, fix_code):
    """Apply a candidate fix in an isolated copy and re-run the tests."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(task_dir, tmp, dirs_exist_ok=True)
        with open(os.path.join(tmp, "task.py"), "w", encoding="utf-8") as f:
            f.write(fix_code)
        rc, out = run([sys.executable, "-m", "pytest", "-q"], tmp)
        return rc == 0, out


def repair(task_dir, model=DEFAULT_MODEL):
    code = open(os.path.join(task_dir, "task.py"), encoding="utf-8").read()
    diag = diagnose(task_dir)
    print(f"[{task_dir}] [{model}] tests pass before fix: {diag['tests_pass']}")
    data, latency, p_tok, c_tok = propose_fixes(code, diag, model)
    record = {"task": task_dir, "model": model, "latency_s": latency,
              "prompt_tokens": p_tok, "completion_tokens": c_tok,
              "issues": data.get("issues", []), "fixes": []}
    for i, fix in enumerate(data.get("fixes", [])[:2], 1):
        passed, _ = test_fix(task_dir, fix["code"])
        print(f"  fix {i}: {'PASS' if passed else 'FAIL'} — "
              f"{fix['explanation'][:70]}")
        record["fixes"].append({"n": i, "explanation": fix["explanation"],
                                "passed": passed})
        if passed:
            fixed_path = os.path.join(task_dir, "task_fixed.py")
            if not os.path.exists(fixed_path):
                with open(fixed_path, "w", encoding="utf-8") as f:
                    f.write(fix["code"])
    with open(RESULTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record


if __name__ == "__main__":
    tasks = sys.argv[1:] or ["broken_tasks/task1"]
    for t in tasks:
        repair(t)
