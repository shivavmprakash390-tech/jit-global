const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const SRC = "C:\\Users\\Auriseg\\jit-global";
const DST = "C:\\Users\\Auriseg\\jit-global-pages";
const COMMIT_MSG = "Add Blog page and Company nav Blog link";
const LIVE = "https://shivavmprakash390-tech.github.io/jit-global/blog.html";
const FILES = [
  "blog.html",
  "index.html",
  "about.html",
  "logo.png",
  "svc-migration-featured.jpg",
  "blog-featured.jpg",
];
const FEATURED_FALLBACKS = [
  path.join(SRC, "blog-featured.jpg"),
  "C:\\Users\\Auriseg\\.grok\\sessions\\C%3A%5CUsers%5CAuriseg%5Cjit-global-pages\\01a061c3-5a54-72b1-8d95-11454e99fcc0\\images\\1.jpg",
];

const lines = [];
function log(msg) {
  console.log(msg);
  lines.push(String(msg));
}

function writeStatus(prefix) {
  const text = prefix + "\n" + lines.join("\n") + "\n";
  fs.writeFileSync(path.join(DST, "_deploy_status.txt"), text, "utf8");
  fs.writeFileSync(path.join(SRC, "_deploy_status.txt"), text, "utf8");
}

log("=== AGENT DEPLOY JS " + new Date().toISOString() + " ===");
log("node=" + process.execPath);

for (const name of FILES) {
  const s = path.join(SRC, name);
  const d = path.join(DST, name);
  if (!fs.existsSync(s)) {
    log("SKIP missing " + name);
    continue;
  }
  fs.copyFileSync(s, d);
  log("COPIED " + name + " (" + fs.statSync(d).size + " bytes)");
}

const featuredDst = path.join(DST, "blog-featured.jpg");
if (!fs.existsSync(featuredDst) || fs.statSync(featuredDst).size < 1000) {
  for (const p of FEATURED_FALLBACKS) {
    if (fs.existsSync(p)) {
      fs.copyFileSync(p, featuredDst);
      log("COPIED blog-featured.jpg from " + p + " (" + fs.statSync(featuredDst).size + " bytes)");
      break;
    }
  }
}

let addOk = false;
let commitOk = false;
let pushOk = false;

for (const cmd of [
  ["git", ["add", "-A"]],
  ["git", ["commit", "-m", COMMIT_MSG]],
  ["git", ["push", "origin", "main"]],
  ["git", ["rev-parse", "HEAD"]],
  ["git", ["status", "-sb"]],
]) {
  log("> " + cmd[0] + " " + cmd[1].join(" "));
  const r = spawnSync(cmd[0], cmd[1], { cwd: DST, encoding: "utf8" });
  const out = (r.stdout || "").trim();
  const err = (r.stderr || "").trim();
  if (out) log(out);
  if (err) log(err);
  log("exit " + r.status);
  const joined = (out + "\n" + err).toLowerCase();
  if (cmd[1][0] === "add") addOk = r.status === 0;
  if (cmd[1][0] === "commit") commitOk = r.status === 0 || joined.includes("nothing to commit");
  if (cmd[1][0] === "push") pushOk = r.status === 0 || joined.includes("everything up-to-date");
}

log("LIVE_URL=" + LIVE);
const ok = addOk && commitOk && pushOk;
log(ok ? "DONE" : "FAILED");
writeStatus(ok ? "SUCCESS" : "FAIL");
process.exit(ok ? 0 : 1);
