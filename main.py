"""
main.py — runs generate.py then publish.py in one shot.

For separate control use:
    python generate.py   # Step 1: LLM pipeline → docs/<course>/
    python publish.py    # Step 2: patch mkdocs.yml, update index, push
"""

import subprocess
import sys


def main() -> None:
    # Forward all args to generate.py, then publish
    generate_args = [sys.executable, "generate.py"] + sys.argv[1:]
    result = subprocess.run(generate_args)
    if result.returncode != 0:
        sys.exit(result.returncode)

    publish_args = [sys.executable, "publish.py"]
    # Pass --course if it was provided
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--course" and i + 1 < len(sys.argv) - 1:
            publish_args += ["--course", sys.argv[i + 2]]
            break

    subprocess.run(publish_args)


if __name__ == "__main__":
    main()
