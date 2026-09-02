"""Copy blog files into pages repo and push to origin main."""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SRC = Path(r"C:\Users\Auriseg\jit-global")
DST = Path(r"C:\Users\Auriseg\jit-global-pages")
LOG_DST = DST / "_deploy_status.txt"
LOG_SRC = SRC / "_deploy_status.txt"
COMMIT_MSG = "Add Blog page and Company nav Blog link"
LIVE = "https://shivavmprakash390-tech.github.io/jit-global/blog.html"

FILES = [
    "blog.html",
    "index.html",
    "about.html",
    "logo.png",
    "svc-migration-featured.jpg",
    "blog-featured.jpg",
]


def write_status(prefix: str, body_lines: list[str]) -> None:
    text = prefix + "\n" + "\n".join(body_lines) + "\n"
    LOG_DST.write_text(text, encoding="utf-8")
    LOG_SRC.write_text(text, encoding="utf-8")


def main() -> int:
    lines: list[str] = []
    push_ok = False
    add_ok = False
    commit_ok = False

    def log(msg: str) -> None:
        print(msg, flush=True)
        lines.append(msg)

    log("=== AGENT DEPLOY " + datetime.now(timezone.utc).isoformat() + " ===")
    log("python=" + sys.executable)

    for name in FILES:
        s, d = SRC / name, DST / name
        if not s.exists():
            log(f"SKIP missing {name}")
            continue
        shutil.copy2(s, d)
        log(f"COPIED {name} ({s.stat().st_size} bytes)")

    featured_dst = DST / "blog-featured.jpg"
    if not featured_dst.exists() or featured_dst.stat().st_size < 1000:
        for p in [
            SRC / "blog-featured.jpg",
            Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CUsers%5CAuriseg%5Cjit-global-pages\01a061c3-5a54-72b1-8d95-11454e99fcc0\images\1.jpg"),
            Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CUsers%5CAuriseg%5Cjit-global\01a0616c-df9e-7da1-9072-59294cb8834e\images\1.jpg"),
        ]:
            if p.exists():
                shutil.copy2(p, featured_dst)
                log(f"COPIED blog-featured.jpg from {p} ({featured_dst.stat().st_size} bytes)")
                break

    for cmd in [
        ["git", "add", "-A"],
        ["git", "commit", "-m", COMMIT_MSG],
        ["git", "push", "origin", "main"],
        ["git", "rev-parse", "HEAD"],
        ["git", "status", "-sb"],
    ]:
        log("> " + " ".join(cmd))
        p = subprocess.run(cmd, cwd=str(DST), capture_output=True, text=True)
        out = (p.stdout or "").rstrip()
        err = (p.stderr or "").rstrip()
        if out:
            log(out)
        if err:
            log(err)
        log("exit " + str(p.returncode))
        joined = out + "\n" + err
        if cmd[1] == "add":
            add_ok = p.returncode == 0
        elif cmd[1] == "commit":
            commit_ok = p.returncode == 0 or "nothing to commit" in joined.lower()
        elif cmd[1] == "push":
            push_ok = p.returncode == 0 or "everything up-to-date" in joined.lower()

    log("LIVE_URL=" + LIVE)
    ok = add_ok and commit_ok and push_ok
    log("DONE" if ok else "FAILED")
    write_status("SUCCESS" if ok else "FAIL", lines)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
