#!/usr/bin/env python3
"""Ledger for levent-method runs (stdlib only).

Ledger lines (append-only, run/ledger.md):
  N | STATUS | claim | locator | tags
STATUS in PROVED, REFUTED, OPEN, FRAGMENT, AUDIT, RETRACT
tags: comma list, e.g. GOAL, toy, control-pass, ref=N, auditor=name

Commands:
  init RUN                      create run dir skeleton
  add RUN STATUS "claim" LOC [TAGS]
  answers RUN ROUND             report each rounds/r{R}_q*.md answered (has END line) / partial / missing
  check RUN ROUND CAP MAXR      print exactly one verdict: WAVE n FLOOR f | CONCLUDE reason | RETRY reason | STOP reason
  status RUN                    print current goal and counts
"""
import os, re, sys, glob

VALID = {"PROVED", "REFUTED", "OPEN", "FRAGMENT", "AUDIT", "RETRACT"}


def lpath(run):
    return os.path.join(run, "ledger.md")


def read(run):
    rows = []
    p = lpath(run)
    if not os.path.exists(p):
        return rows
    for line in open(p, encoding="utf-8"):
        parts = [x.strip() for x in line.rstrip("\n").split("|")]
        if len(parts) >= 4 and parts[0].isdigit():
            tags = parts[4] if len(parts) > 4 else ""
            rows.append(dict(n=int(parts[0]), st=parts[1], claim=parts[2], loc=parts[3],
                             tags={t.strip() for t in tags.split(",") if t.strip()}))
    retracted = set()
    for r in rows:
        if r["st"] == "RETRACT":
            for t in r["tags"]:
                if t.startswith("ref="):
                    retracted.add(int(t[4:]))
    return [r for r in rows if r["n"] not in retracted]


def goal(rows):
    g = [r for r in rows if "GOAL" in r["tags"]]
    return g[-1] if g else None


def cmd_init(run):
    for d in [run, os.path.join(run, "rounds"), os.path.join(run, "lean")]:
        os.makedirs(d, exist_ok=True)
    for f in ["problem.md", "controls.md", "analogy.md", "SPEC.md", "summary.md", "state.md", "ledger.md"]:
        p = os.path.join(run, f)
        if not os.path.exists(p):
            open(p, "w").close()
    print("OK", run)


def cmd_add(run, st, claim, loc, tags=""):
    st = st.upper()
    if st not in VALID:
        sys.exit("ERROR: status must be one of " + ",".join(sorted(VALID)))
    if "|" in claim or "|" in loc:
        sys.exit("ERROR: '|' not allowed in fields")
    rows = read(run)
    allrows = 0
    if os.path.exists(lpath(run)):
        allrows = sum(1 for l in open(lpath(run)) if re.match(r"^\d+ \|", l))
    n = allrows + 1
    with open(lpath(run), "a", encoding="utf-8") as f:
        f.write(f"{n} | {st} | {claim} | {loc} | {tags}\n")
    print(n)


def answers(run, rnd):
    out = {}
    for q in sorted(glob.glob(os.path.join(run, "rounds", f"r{rnd}_q*.md"))):
        if q.endswith(".answer.md"):
            continue
        a = q[:-3] + ".answer.md"
        if not os.path.exists(a) or os.path.getsize(a) == 0:
            out[q] = "missing"
        else:
            txt = open(a, encoding="utf-8").read().rstrip()
            out[q] = "answered" if txt.splitlines()[-1].strip() == "END" else "partial"
    return out


def cmd_answers(run, rnd):
    for q, s in answers(run, rnd).items():
        print(os.path.basename(q), s)


def cmd_check(run, rnd, cap, maxr):
    rnd, cap, maxr = int(rnd), int(cap), int(maxr)
    rows = read(run)
    g = goal(rows)
    if g and g["st"] in ("PROVED", "REFUTED"):
        audits = [r for r in rows if r["st"] == "AUDIT" and f"ref={g['n']}" in r["tags"]]
        auditors = {t for r in audits for t in r["tags"] if t.startswith("auditor=")}
        if len(auditors) >= 2:
            print(f"CONCLUDE goal {g['n']} {g['st']} with {len(auditors)} independent audits")
            return
        print(f"RETRY goal {g['n']} is {g['st']} but has {len(auditors)} independent AUDIT lines; schedule auditors")
        return
    if rnd > maxr:
        print("STOP budget: max rounds reached")
        return
    if rnd > 1:
        prev = answers(run, rnd - 1)
        n = len(prev)
        done = sum(1 for s in prev.values() if s in ("answered", "partial"))
        if n and done < max(1, (3 * n) // 10):
            print(f"STOP systemic failure: only {done}/{n} answers in round {rnd-1}")
            return
        if rnd > 2:
            recent = [r for r in rows if r["st"] in ("PROVED", "FRAGMENT") and
                      any(t in r["tags"] for t in (f"round={rnd-1}", f"round={rnd-2}"))]
            if not recent:
                print("STOP no new PROVED/FRAGMENT in two rounds; change representation or end run")
                return
    qs = [q for q in glob.glob(os.path.join(run, "rounds", f"r{rnd}_q*.md")) if not q.endswith(".answer.md")]
    if not qs:
        print(f"RETRY no query files rounds/r{rnd}_q*.md written")
        return
    if len(qs) > cap:
        print(f"RETRY {len(qs)} queries exceed cap {cap}")
        return
    attempts = sum(1 for q in qs if open(q, encoding="utf-8").readline().strip().lower() == "kind: attempt")
    if attempts * 2 < len(qs):
        print(f"RETRY only {attempts}/{len(qs)} queries are 'kind: attempt'; need at least half")
        return
    print(f"WAVE {len(qs)} FLOOR {max(1, (3 * len(qs)) // 10)}")


def cmd_status(run):
    rows = read(run)
    g = goal(rows)
    print("GOAL:", f"{g['n']} {g['st']} {g['claim']}" if g else "none")
    for s in sorted(VALID - {"RETRACT"}):
        print(s, sum(1 for r in rows if r["st"] == s))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(0)
    fn = {"init": cmd_init, "add": cmd_add, "answers": cmd_answers, "check": cmd_check, "status": cmd_status}.get(a[0])
    if not fn:
        sys.exit("usage: see --help")
    fn(*a[1:])
