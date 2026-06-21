import subprocess
import os
from datetime import datetime

REPO_ROOT = "."
STATE_FILE = "MASTER_CONTEXT.md"

def run(cmd):
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)

def git_sync(message):
    run("git add .")
    run(f'git commit -m "{message}"')
    run("git push")

def read_context():
    with open(STATE_FILE, "r") as f:
        return f.read()

def scan_missing_structure():
    required = [
        "research/",
        "sources/notes/",
        "research/architecture/",
        "research/analysis/",
        "research/firmware/",
        "research/exploit_history/"
    ]

    missing = []
    for path in required:
        if not os.path.exists(path):
            missing.append(path)

    return missing

def generate_open_code_task(missing):
    if not missing:
        return None

    return f"""
Review repository.

Detected missing structure:

{missing}

Tasks:
1. Create missing directories/files
2. Ensure markdown scaffolding exists
3. Do NOT add technical content
4. Update MASTER_CONTEXT.md with current structure state
"""

def main():
    context = read_context()
    missing = scan_missing_structure()

    task = generate_open_code_task(missing)

    if task:
        print("Trigger OpenCode task:\n")
        print(task)
    else:
        git_sync("auto-sync: system check complete")

    print("Orchestrator run complete at", datetime.now())

if __name__ == "__main__":
    main()