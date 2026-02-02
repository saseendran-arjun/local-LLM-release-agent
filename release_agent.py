import json
import re
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def ollama_generate(prompt: str) -> str:
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["response"]

def extract_failures(log_text: str):
    #grab lines that look like failures
    fails = []
    for line in log_text.splitlines():
        if re.search(r"\bFAIL\b|\bERROR\b|AssertionError|Exception", line):
            fails.append(line.strip())
    return fails[:30]  # cap for readability

def main():
    with open("release_request.txt", "r", encoding="utf-8") as f:
        req_text = f.read()

    with open("test_log.txt", "r", encoding="utf-8") as f:
        log_text = f.read()

    failures = extract_failures(log_text)

    # 1) Planning prompt
    prompt_plan = f"""
You are a software release preparation assistant.

RELEASE REQUEST:
{req_text}

TASK:
1) Produce a step-by-step checklist to prepare the software load (build, versioning, packaging).
2) Produce a qualification plan (tests to run + what evidence to collect).
3) If you see risks, list them with mitigations.

Return in Markdown with clear headings.
"""
    plan = ollama_generate(prompt_plan)

    # 2) Reporting prompt (uses extracted facts)
    prompt_report = f"""
You are a QA qualification assistant.

Given these extracted failures:
{failures}

And this raw log context:
{log_text[:2500]}

Write a short qualification report with:
- Status: PASS/FAIL
- Top failure themes
- Suggested next actions (ordered)
Keep it concise and practical.
"""
    report = ollama_generate(prompt_report)

    print("\n=== RELEASE PREP PLAN ===\n")
    print(plan)
    print("\n=== QUALIFICATION REPORT ===\n")
    print(report)

if __name__ == "__main__":
    main()
