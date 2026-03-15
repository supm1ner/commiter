#!/usr/bin/env python3
"""
committer.py — спамит пустые коммиты в GitHub для заполнения графа активности.
"""

import subprocess
import time
import random
import argparse
from datetime import datetime


def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[error] {result.stderr.strip()}")
    return result.returncode == 0


def make_commit(message=None):
    if not message:
        message = f"chore: update {random.randint(1000, 9999)}"
    
    # Пишем что-нибудь в файл чтобы коммит не был совсем пустым
    with open(".committer_log", "a") as f:
        f.write(f"{datetime.now().isoformat()} — {message}\n")
    
    run("git add .committer_log")
    ok = run(f'git commit -m "{message}"')
    return ok


def push(batch_size, count):
    """Пушим каждые batch_size коммитов"""
    if count % batch_size == 0:
        print(f"  → pushing...")
        run("git push")


def main():
    parser = argparse.ArgumentParser(description="Spam commits to GitHub")
    parser.add_argument("-n", "--count", type=int, default=0,
                        help="Количество коммитов (0 = бесконечно)")
    parser.add_argument("-d", "--delay", type=float, default=0.1,
                        help="Задержка между коммитами в секундах (default: 0.1)")
    parser.add_argument("-b", "--batch", type=int, default=10,
                        help="Пушить каждые N коммитов (default: 10)")
    args = parser.parse_args()

    print(f"🚀 Committer запущен | delay={args.delay}s | batch={args.batch} | count={'∞' if args.count == 0 else args.count}")
    print("Ctrl+C для остановки\n")

    i = 0
    try:
        while True:
            i += 1
            ok = make_commit()
            if ok:
                print(f"[{i}] ✓ commit")
                push(args.batch, i)
            else:
                print(f"[{i}] ✗ failed")

            if args.count > 0 and i >= args.count:
                break

            time.sleep(args.delay)

    except KeyboardInterrupt:
        print(f"\n⏹ Остановлено. Всего коммитов: {i}")

    # Финальный пуш
    print("→ final push...")
    run("git push")
    print("Done.")


if __name__ == "__main__":
    main()
