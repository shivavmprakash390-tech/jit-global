import shutil
import subprocess
import sys
from pathlib import Path

LOG = Path(r"C:\Users\Auriseg\jit-global\_deploy_result.txt")
STATUS = Path(r"C:\Users\Auriseg\jit-global\_deploy_status.txt")


def log(msg):
    line = str(msg)
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


LOG.write_text("START\n", encoding="utf-8")
log("python=" + sys.executable)

src = Path(r"C:\Users\Auriseg\jit-global")
dst = Path(r"C:\Users\Auriseg\jit-global-pages")

# wire
r = subprocess.run([sys.executable, str(src / "_wire_company_nav.py")], capture_output=True, text=True)
log("=== wire ===")
log((r.stdout or "").rstrip())
if r.stderr:
    log((r.stderr or "").rstrip())
log("wire exit " + str(r.returncode))
wire_ok = r.returncode == 0

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
copy_ok = True
for n in files:
    s, d = src / n, dst / n
    if not s.exists():
        log("MISSING " + n)
        copy_ok = False
        continue
    shutil.copy2(s, d)
    log(f"copied {n} ({d.stat().st_size} bytes)")

# session featured fallbacks
for p in [
    src / "blog-featured.jpg",
    Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CUsers%5CAuriseg%5Cjit-global\01a0616c-df9e-7da1-9072-59294cb8834e\images\1.jpg"),
    Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CUsers%5CAuriseg%5Cjit-global\01a0616f-d711-7d80-a9f6-b511430829f3\images\1.jpg"),
    Path(r"C:\Users\Auriseg\.grok\sessions\C%3A%5CWINDOWS%5Csystem32\01a0616f-2174-7911-a3be-269fd86dfa14\images\1.jpg"),
]:
    if p.exists():
        shutil.copy2(p, dst / "blog-featured.jpg")
        log(f"featured from {p} ({(dst / 'blog-featured.jpg').stat().st_size} bytes)")
        break

blog_size = (src / "blog.html").stat().st_size if (src / "blog.html").exists() else -1
log(f"blog.html size {blog_size}")

log("=== git ===")
commit_ok = push_ok = False
for cmd in (
    ["git", "add", "-A"],
    ["git", "commit", "-m", "Add JIT Global Blog page and Company dropdown (About Us / Blog)"],
    ["git", "push", "origin", "main"],
):
    log("> " + " ".join(cmd))
    p = subprocess.run(cmd, cwd=str(dst), capture_output=True, text=True)
    if p.stdout:
        log(p.stdout.rstrip())
    if p.stderr:
        log(p.stderr.rstrip())
    log("exit " + str(p.returncode))
    joined = (p.stdout or "") + (p.stderr or "")
    if "commit" in cmd:
        commit_ok = p.returncode == 0 or "nothing to commit" in joined
    if "push" in cmd:
        push_ok = p.returncode == 0

overall = wire_ok and copy_ok and push_ok
log(f"OVERALL={'SUCCESS' if overall else 'FAIL'} wire={wire_ok} copy={copy_ok} commit={commit_ok} push={push_ok}")
log("DONE" if overall else "FAILED")

STATUS.write_text(LOG.read_text(encoding="utf-8"), encoding="utf-8")
raise SystemExit(0 if overall else 1)
