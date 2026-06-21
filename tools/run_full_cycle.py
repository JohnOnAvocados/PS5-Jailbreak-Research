import os
import subprocess
import sys

SCRIPTS = [
    "tools/graph_memory_compiler.py",
    "tools/contradiction_detector.py",
    "tools/vulnerability_scorer.py",
    "tools/dependency_resolver.py",
    "tools/insight_extractor.py",
    "tools/knowledge_cluster.py",
]

def run(cmd):
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    failures = []
    for script in SCRIPTS:
        if not os.path.isfile(script):
            print(f"FAIL: {script} not found")
            failures.append(script)
            continue
        print(f"Running: {script}")
        if run(f"python {script}"):
            print(f"  OK: {script}")
        else:
            print(f"  FAIL: {script}")
            failures.append(script)
    if failures:
        print(f"\nPipeline finished with {len(failures)} failure(s): {', '.join(failures)}")
        sys.exit(1)
    else:
        print("\nAll pipeline steps completed successfully")

if __name__ == "__main__":
    main()
