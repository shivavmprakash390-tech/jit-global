import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

out = Path(r"C:\Users\Auriseg\jit-global\_deploy_out.txt")
lines = []

def log(msg):
    lines.append(str(msg))
    print(msg, flush=True)

log("=== FORCE DEPLOY " + datetime.now(timezone.utc).isoformat() + " ===")
src = Path(r"C:\Users\Auriseg\jit-global")
dst = Path(r"C:\Users\Auriseg\jit-global-pages")

wire = src / "_wire_company_nav.py"
if wire.exists():
    r = subprocess.run([sys.executable, str(wire)], capture_output=True, text=True)
    log("=== wire script ===")
    log(r.stdout)
    if r.stderr:
        log(r.stderr)
    log("wire exit " + str(r.returncode))
else:
    log("wire script MISSING")

files = [
    "blog.html",
    "blog-featured.jpg",
    "logo.png",
    "index.html",
    "about.html",
    "success-stories.html",
    "healthcare-life-sciences.html",
    "cloud-migration-modernization.html",
]
log("=== copy ===")
for name in files:
    s, d = src / name, dst / name
    if not s.exists():
        log("MISSING " + name)
        continue
    shutil.copy2(s, d)
    log(f"copied {name} ({s.stat().st_size} bytes)")

# also try session image if blog-featured missing/zero
for session_img in [
    Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CWINDOWS%5Csystem32\01a06170-4220-7631-b151-0a3d9d0ba338\images\1.jpg"),
    Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CWINDOWS%5Csystem32\01a06170-c5c4-7811-bf5e-a1d7fc3cbe21\images\1.jpg"),
    Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CUsers%5CAuriseg%5Cjit-global\01a0616f-d711-7d80-a9f6-b511430829f3\images\1.jpg"),
    Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CUsers%5CAuriseg%5Cjit-global\01a06170-f2f4-7c50-ac35-74e5bfbd16ac\images\1.jpg"),
]:
    if session_img.exists():
        shutil.copy2(session_img, dst / "blog-featured.jpg")
        log(f"copied session blog-featured.jpg ({session_img.stat().st_size} bytes) from {session_img}")
        break
else:
    log("session blog-featured.jpg MISSING")

log("=== git ===")
for cmd in [
    ["git", "add", "-A"],
    ["git", "commit", "-m", "Add JIT Global Blog page and Company dropdown (About Us / Blog)"],
    ["git", "push", "origin", "main"],
]:
    log("> " + " ".join(cmd))
    p = subprocess.run(cmd, cwd=str(dst), capture_output=True, text=True)
    log(p.stdout)
    if p.stderr:
        log(p.stderr)
    log("exit " + str(p.returncode))

blog = src / "blog.html"
log("blog size " + str(blog.stat().st_size if blog.exists() else 0))
log("DONE")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
