#!/usr/bin/env python3
"""Source-linked buyer research and manual deal preflight. NEVER sends outreach."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "registry" / "buyer_channels.json"
OUT = HERE / "output" / "buyer_research"

def read():
    return json.loads(DATA.read_text(encoding="utf-8"))

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def discovery_plan(limit):
    data=read()
    records=[]
    for group in data["discovery_surfaces"]:
        if group["method"] != "decodo_search":
            continue
        for query in group["queries"]:
            records.append({"source_id":group["id"],"query":query,"purpose":group["name"],"origin":group["url"],"status":"unexecuted_search"})
            if len(records)>=limit: return records
    return records

def validated_routes():
    data=read()
    return [{"buyer_id":r["id"],"name":r["label"],"method":r["method"],"official_page":r["programme_url"],
             "contact_route":r["contact_url"],"general_business_email":r["general_business_email"],
             "partner_status":r["status"],"independent_research_eligibility":r["referral_eligibility"]}
            for r in data["routes"]]

def brief(buyer):
    candidates={r["id"]:r for r in read()["routes"]}
    if buyer not in candidates:
        raise ValueError(f"Unknown buyer {buyer}. Try 'channels'.")
    r=candidates[buyer]
    return {
        "buyer_id":buyer,
        "business":r["label"],
        "official_programme_page":r["programme_url"],
        "approved_contact_channel":r["method"],
        "contact_url":r["contact_url"],
        "general_business_email":r["general_business_email"],
        "published_terms":r["expected_terms"],
        "opportunity_status":"published_not_approved",
        "next_human_action":r["suggested_first_action"],
        "must_confirm":["Do you accept externally discovered prospects, not only existing clients?",
                        "Is a consent-based introduction required? What records evidence consent?",
                        "How are new-client referrals registered and protected?",
                        "Excluded existing pipeline / duplicate customers?",
                        "Eligible service categories and minimum project value?",
                        "Commission basis, qualifying trigger, protection window and payment deadline?",
                        "Are public procurement tenders excluded?",
                        "Who can give written commercial approval?"],
        "draft_only_subject":r.get("suggested_email_subject","Partnership enquiry: permission-based project introductions"),
        "draft_only_body":(
            "Hello,\n\n"
            "I'm researching organisations with evidenced requests for digital services, "
            "using their original published RFPs rather than speculative contact lists.\n\n"
            f"I noticed your published programme ({r['programme_url']}) and wanted to "
            "ask whether you accept independently identified prospects once they "
            "have agreed to an introduction. If so, what service types/project budgets "
            "are suitable, how is attribution recorded, and when does payment become due?\n\n"
            "I'd be happy to discuss a small, clearly documented trial once we agree the terms.\n\n"
            "[Your name]\n"
        ),
        "human_review_required":True,
        "no_outreach_sent":True,
        "generated_at_utc":now()
    }

def live_scan(limit, max_results, geo):
    """Run official Decodo CLI search for buyer discovery queries, without scraping sites."""
    import sys
    sys.path.insert(0, str(HERE))
    from run import decodo, search_entries, safe_public_url, canonical

    results = {}
    errors = []
    plan = discovery_plan(limit)
    for index, job in enumerate(plan, 1):
        try:
            raw = decodo(["search", job["query"], "--geo", geo])
            data = json.loads(raw)
            for entry in search_entries(data)[:max_results]:
                original_url = entry.get("link") or entry.get("url") or entry.get("display_url")
                if not isinstance(original_url, str) or not safe_public_url(original_url):
                    continue
                url = canonical(original_url)
                if url not in results:
                    title = str(entry.get("title") or "")[:300]
                    excerpt = str(entry.get("snippet") or entry.get("description") or "")[:1000]
                    text = (title + " " + excerpt).lower()
                    signals = [token for token in ("referral", "affiliate", "introducer",
                              "commission", "partner", "qualified lead", "paid pilot")
                               if token in text]
                    results[url] = {"source_id":job["source_id"],
                        "url":url,"title":title,"search_excerpt":excerpt,
                        "signals_from_search":signals,
                        "discovery_query":job["query"],
                        "seen_at_utc":now(),
                        "verification_status":"unverified_search_candidate",
                        "official_company_contact_channel":None,
                        "evidence_of_willingness_to_pay":None,
                        "independent_lead_eligibility":"unconfirmed",
                        "agreement_status":"none",
                        "next_human_action":"Verify business-owned programme/contact page and its current terms"}
        except (RuntimeError, ValueError, TimeoutError) as error:
            errors.append({"source_id":job["source_id"],"error_type":type(error).__name__,
                           "detail":str(error)[:140]})
        print(f"buyer query {index}/{len(plan)}, unique={len(results)}",file=sys.stderr)
    OUT.mkdir(parents=True,exist_ok=True)
    destination=OUT/"discovered-agencies.jsonl"
    with destination.open("w",encoding="utf-8") as f:
        for row in results.values():
            f.write(json.dumps(row,ensure_ascii=False)+"\n")
    summary={"generated_at_utc":now(),"queries_requested":len(plan),
             "queries_succeeded":len(plan)-len(errors),"unique_candidates":len(results),
             "confirmed_partners":0,"verified_contact_routes_from_search":0,
             "errors":errors,"file":str(destination),
             "message":"Search-only candidates. No emails/introductions or deals executed."}
    (OUT/"scan-summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="action",required=True)
    sub.add_parser("channels")
    pl=sub.add_parser("plan");pl.add_argument("--limit",type=int,default=12)
    sc=sub.add_parser("scan");sc.add_argument("--limit",type=int,default=10)
    sc.add_argument("--geo",choices=("gb","us","de","fr","ca","au"),default="gb")
    sc.add_argument("--max-results",type=int,default=10)
    b=sub.add_parser("brief");b.add_argument("--buyer",required=True)
    sub.add_parser("checklist")
    args=p.parse_args()
    if args.action=="channels": result=validated_routes()
    elif args.action=="plan":
        if not 1<=args.limit<=100:p.error("--limit 1..100")
        result=discovery_plan(args.limit)
    elif args.action=="scan":
        if not 1<=args.limit<=100:p.error("--limit 1..100")
        if not 1<=args.max_results<=100:p.error("--max-results 1..100")
        result=live_scan(args.limit,args.max_results,args.geo)
    elif args.action=="brief":
        result=brief(args.buyer)
        OUT.mkdir(parents=True,exist_ok=True)
        path=OUT/(args.buyer+"-draft.json")
        path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    else: result={"commercial_gates":[
        "G1 company and programme independently verified","G2 contact route official and legal to use",
        "G3 introduction sourcing method expressly accepted","G4 minimum project, region and exclusions agreed",
        "G5 attribution and duplicate exclusions documented",
        "G6 payout basis, event, timing and clawbacks agreed",
        "G7 prospect consent evidenced before any introduction",
        "G8 partner acceptance and introduction human-approved",
        "G9 invoice and payment verified"
    ],"status":"checklist_only","outreach_enabled":False}
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
