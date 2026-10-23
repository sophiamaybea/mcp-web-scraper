#!/usr/bin/env python3
"""Plan and run cautious B2B discovery searches through the official Decodo CLI.

No external Python dependencies. Outputs are candidates, not verified leads.
Only a review-approved explicit scrape command calls decodo scrape.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "registry" / "sources.json"
BUYERS = ROOT / "registry" / "buyers.json"
VALID_METHODS = {"official_api", "decodo_search", "manual_review", "known_public_page"}
DROP_QUERY_PARAMS = {"fbclid", "gclid", "igshid", "mc_cid", "mc_eid"}
STRONG_TERMS = ("request for proposal", "request for proposals", "request for quotation",
                "invitation to tender", "invitation to quote", "rfp", "rfq",
                "seeking an agency", "seeking agency", "seeking consultant")
NEGATIVE_TERMS = ("awarded contract", "award notice", "cancellation notice",
                  "tender closed", "deadline passed", "job vacancy", "apply for this job")


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(sources=None):
    sources = sources or read_json(SRC)["sources"]
    ids = set()
    for row in sources:
        assert isinstance(row.get("id"), str) and row["id"], "Source id missing"
        assert row["id"] not in ids, f"Duplicate source id: {row['id']}"
        ids.add(row["id"])
        assert row["method"] in VALID_METHODS, f"Unknown method: {row['id']}"
        assert row["side"] in {"demand", "buyer"}, f"Invalid side: {row['id']}"
        assert isinstance(row.get("priority"), int) and 1 <= row["priority"] <= 5
        assert row.get("url", "").startswith("https://"), f"HTTPS required: {row['id']}"
        assert isinstance(row.get("queries"), list)
        if row["method"] == "decodo_search":
            assert all(isinstance(q, str) and q.strip() for q in row["queries"])
            assert row["queries"], f"Search queries missing: {row['id']}"
    buyer_ids = [b["id"] for b in read_json(BUYERS)["buyers"]]
    assert len(set(buyer_ids)) == len(buyer_ids), "Duplicate buyer id"
    return len(sources)


def tasks(sources, side="all", limit=20, selected_id=None):
    items = [s for s in sources if s["enabled"] and s["method"] == "decodo_search"
             and (side == "all" or s["side"] == side)
             and (selected_id is None or s["id"] == selected_id)]
    items.sort(key=lambda s: (s["priority"], s["id"]))
    todo = []
    for source in items:
        for query in source["queries"]:
            if len(todo) >= limit:
                return todo
            todo.append({"source_id": source["id"], "side": source["side"],
                         "verticals": source["verticals"], "priority": source["priority"],
                         "query": query, "origin": source["url"]})
    return todo


def canonical(url):
    """Stable public URL key: tracking removed; no fragment."""
    try:
        parts = urlsplit(url)
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            return None
        domain = parts.hostname.lower()
        params = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                  if not k.lower().startswith("utm_") and k.lower() not in DROP_QUERY_PARAMS]
        return urlunsplit((parts.scheme, domain + (f":{parts.port}" if parts.port else ""),
                           parts.path.rstrip("/") or "/", urlencode(sorted(params)), ""))
    except ValueError:
        return None


def safe_public_url(url):
    key = canonical(url)
    if key is None:
        return False
    host = urlsplit(key).hostname or ""
    if host in {"localhost", "0.0.0.0"} or host.endswith((".local", ".internal", ".test")):
        return False
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_global
    except ValueError:
        return "." in host


def search_entries(payload):
    """Decodo CLI search emits organic results; accept several documented wrappers."""
    if isinstance(payload, list):
        if all(isinstance(x, dict) for x in payload):
            return payload
        return []
    if not isinstance(payload, dict):
        return []
    for field in ("organic", "results", "items"):
        if isinstance(payload.get(field), list):
            return [x for x in payload[field] if isinstance(x, dict)]
    for field in ("data", "result", "response"):
        if field in payload:
            candidates = search_entries(payload[field])
            if candidates:
                return candidates
    return []


def signal_info(title, snippet, side, verticals):
    blob = (title + " " + snippet).lower()
    if side == "buyer":
        strength = "programme_candidate" if any(
            x in blob for x in ("referral", "affiliate", "partner programme", "partner program")
        ) else "weak_signal"
        return strength, 45 if strength == "programme_candidate" else 15
    if any(x in blob for x in NEGATIVE_TERMS):
        return "likely_ineligible_or_expired", 0
    if any(x in blob for x in STRONG_TERMS):
        score = 65
        if any(x in blob for x in ("deadline", "closing date", "proposals due")):
            score += 10
        if re.search(r"(?:£|€|\$)\s?\d[\d,.]*", blob):
            score += 10
        return "direct_request_candidate", min(85, score)
    return "weak_signal", 15


def normalize(entry, task):
    title = str(entry.get("title") or entry.get("name") or "")[:300]
    snippet = str(entry.get("snippet") or entry.get("description") or "")[:1200]
    url = entry.get("url") or entry.get("link") or entry.get("display_url")
    if not isinstance(url, str) or not safe_public_url(url):
        return None
    key = canonical(url)
    strength, score = signal_info(title, snippet, task["side"], task["verticals"])
    return {
        "id": hashlib.sha256(key.encode("utf-8")).hexdigest()[:20],
        "side": task["side"],
        "source_id": task["source_id"],
        "original_source_url": task["origin"],
        "url": key,
        "title": title,
        "excerpt": snippet,
        "search_query": task["query"],
        "verticals": task["verticals"],
        "signal": strength,
        "discovery_score": score,
        "seen_at_utc": utc_now(),
        "budget": None,
        "deadline": None,
        "organisation": None,
        "verification_status": "unverified_search_result",
        "consent_to_introduction": False,
        "payment_rights": "not_verified",
    }


def matching_published_programmes(item, buyers):
    """Candidate list only. Published programme does not equal approved relationship."""
    if item["side"] != "demand" or item["signal"] == "likely_ineligible_or_expired":
        return []
    result = []
    for buyer in buyers:
        if set(item["verticals"]) & set(buyer["verticals"]):
            result.append({"buyer_id": buyer["id"], "published_terms_url": buyer["url"],
                           "status": "published_only_not_contractually_approved"})
    return result


def decodo(cli_args, timeout=90):
    if not shutil.which("decodo"):
        raise RuntimeError("Decodo CLI missing. Install Node 22+ and npm i -g @decodo/cli.")
    p = subprocess.run(["decodo", *cli_args], capture_output=True, text=True,
                       timeout=timeout, check=False)
    if p.returncode:
        # Do not echo third-party stderr; it might include headers or token.
        raise RuntimeError(f"Decodo command failed with exit code {p.returncode}")
    return p.stdout


def write_jsonl(file, rows):
    with file.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def do_scan(args, sources):
    plan = tasks(sources, side=args.side, limit=args.max_queries, selected_id=args.source)
    out = ROOT / "output" if not args.output_dir else Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    found, failures = {}, []
    buyers = read_json(BUYERS)["buyers"]
    for i, task in enumerate(plan, 1):
        try:
            stdout = decodo(["search", task["query"], "--geo", args.geo])
            try:
                payload = json.loads(stdout)
            except json.JSONDecodeError:
                failures.append({"source_id": task["source_id"],
                                 "reason": "CLI output not JSON; verify installed Decodo CLI version"})
                continue
            for entry in search_entries(payload)[:args.max_results]:
                item = normalize(entry, task)
                if not item:
                    continue
                if item["id"] in found:
                    found[item["id"]]["seen_in"].append(task["source_id"])
                    continue
                item["seen_in"] = [task["source_id"]]
                item["candidate_partner_programmes"] = matching_published_programmes(item, buyers)
                found[item["id"]] = item
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            failures.append({"source_id": task["source_id"],
                             "error_type": type(exc).__name__, "reason": str(exc)[:150]})
        print(f"{i}/{len(plan)} queries completed; {len(found)} unique candidates",
              file=sys.stderr)
    rows = sorted(found.values(), key=lambda r: r["discovery_score"], reverse=True)
    write_jsonl(out / "candidates.jsonl", rows)
    write_jsonl(out / "errors.jsonl", failures)
    columns = ["id", "side", "source_id", "title", "url", "signal", "discovery_score",
               "verification_status", "seen_at_utc"]
    with (out / "candidates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows([{k: r.get(k) for k in columns} for r in rows])
    summary = {"generated_utc": utc_now(), "queries_requested": len(plan),
               "queries_succeeded": len(plan) - len(failures), "failures": len(failures),
               "unique_candidates": len(rows), "verified_leads": 0,
               "commission_agreements_confirmed": 0,
               "note": "Search candidates only; human evidence review required."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if not failures else 2


def reviewed_fetch(args):
    if not args.confirmed_rights:
        raise RuntimeError("Require --confirmed-rights after checking original site access terms.")
    if not safe_public_url(args.url):
        raise RuntimeError("Use a publicly accessible http/https domain, never private/local URLs.")
    op = args.action
    command = ["scrape", args.url] if op == "scrape" else ["map", args.url, "--limit", str(args.map_limit)]
    content = decodo(command, timeout=150)
    out = ROOT / "output" / "reviewed"
    out.mkdir(parents=True, exist_ok=True)
    slug = hashlib.sha256(args.url.encode("utf-8")).hexdigest()[:20]
    dest = out / (f"{op}-{slug}." + ("md" if op == "scrape" else "txt"))
    dest.write_text(content[:1000000], encoding="utf-8")
    print(json.dumps({"output_file": str(dest), "action": op,
                      "url": args.url, "reviewed_access_by_operator": True}))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("validate")
    plan_parser = sub.add_parser("plan")
    scan_parser = sub.add_parser("scan")
    for p in (plan_parser, scan_parser):
        p.add_argument("--side", choices=("all", "buyer", "demand"), default="all")
        p.add_argument("--max-queries", type=int, default=20)
        p.add_argument("--source", help="Optional source ID filter")
    scan_parser.add_argument("--max-results", type=int, default=10)
    scan_parser.add_argument("--geo", choices=("gb", "us", "de", "fr", "ca", "au"), default="gb")
    scan_parser.add_argument("--output-dir", default=None)
    for action in ("scrape", "map"):
        p = sub.add_parser(action)
        p.add_argument("--url", required=True)
        p.add_argument("--confirmed-rights", action="store_true")
        if action == "map":
            p.add_argument("--map-limit", type=int, default=20)
    args = parser.parse_args()
    sources = read_json(SRC)["sources"]
    validate(sources)
    if args.action == "validate":
        print(f"Valid manifest: {len(sources)} sources; {len(read_json(BUYERS)['buyers'])} published buyer programmes.")
        return 0
    if args.action in ("plan", "scan"):
        if args.max_queries < 1 or args.max_queries > 200:
            parser.error("--max-queries must be between 1 and 200")
        if args.action == "plan":
            print(json.dumps(tasks(sources, args.side, args.max_queries, args.source), indent=2))
            return 0
        if args.max_results < 1 or args.max_results > 100:
            parser.error("--max-results must be between 1 and 100")
        return do_scan(args, sources)
    if args.action == "map" and not (1 <= args.map_limit <= 100):
        parser.error("--map-limit must be between 1 and 100")
    return reviewed_fetch(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, AssertionError) as error:
        print("Error: " + str(error), file=sys.stderr)
        sys.exit(1)
