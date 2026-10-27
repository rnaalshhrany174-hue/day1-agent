"""Lab 3.2 — Comparative model evaluation on the fixed task set.
Runs the repair agent across every task with each model, then writes
evaluation_report.md with the scorecard.

Edit MODELS to the exact ids you are using on OpenRouter.
"""
import glob, json
from repair_agent import repair

MODELS = [
    "openai/gpt-4o-mini"
]

tasks = sorted(glob.glob("broken_tasks/task*"))
records = []
for model in MODELS:
    for t in tasks:
        try:
            records.append(repair(t, model=model))
        except Exception as e:                   # a failed run is data too
            print(f"  ERROR [{model}] {t}: {e}")
            records.append({"task": t, "model": model, "error": str(e),
                            "fixes": [], "latency_s": 0,
                            "prompt_tokens": 0, "completion_tokens": 0})

lines = ["# Model Evaluation Report — Code Repair\n",
         f"Tasks: {len(tasks)} | Models: {', '.join(MODELS)}\n",
         "| Model | Task solved (any fix) | First-fix success | "
         "Hallucinated fixes* | Avg latency (s) | Avg tokens |",
         "|---|---|---|---|---|---|"]
for model in MODELS:
    rs = [r for r in records if r["model"] == model]
    solved = sum(1 for r in rs if any(f["passed"] for f in r["fixes"]))
    first = sum(1 for r in rs if r["fixes"] and r["fixes"][0]["passed"])
    halluc = sum(1 for r in rs for f in r["fixes"] if not f["passed"])
    lat = sum(r["latency_s"] for r in rs) / max(len(rs), 1)
    tok = sum(r["prompt_tokens"] + r["completion_tokens"] for r in rs) \
        / max(len(rs), 1)
    lines.append(f"| {model} | {solved}/{len(tasks)} | {first}/{len(tasks)} "
                 f"| {halluc} | {lat:.1f} | {tok:.0f} |")
lines += ["", "*A hallucinated fix = the model presented it as a valid "
          "repair, but the tests fail.", "", "## Per-task matrix", "",
          "| Task | " + " | ".join(MODELS) + " |",
          "|---|" + "---|" * len(MODELS)]
for t in tasks:
    row = []
    for model in MODELS:
        r = next((x for x in records
                  if x["task"] == t and x["model"] == model), None)
        row.append("✓" if r and any(f["passed"] for f in r["fixes"])
                   else "✗")
    lines.append(f"| {t.split('/')[-1]} | " + " | ".join(row) + " |")

with open("evaluation_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\nWrote evaluation_report.md")
