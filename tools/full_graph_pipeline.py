import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True)

def main():
    print("Compiling graph...")
    run("python tools/graph_memory_compiler.py")

    print("Analyzing graph...")
    run("python tools/graph_analyzer.py")

    print("Committing changes...")
    run("git add .")
    run('git commit -m "auto: graph memory update"')
    run("git push")

if __name__ == "__main__":
    main()