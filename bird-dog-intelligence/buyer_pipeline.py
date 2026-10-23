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

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="action",required=True)
    sub.add_parser("channels")
    pl=sub.add_parser("plan");pl.add_argument("--limit",type=int,default=12)
    b=sub.add_parser("brief");b.add_argument("--buyer",required=True)
    sub.add_parser("checklist")
    args=p.parse_args()
    if args.action=="channels": result=validated_routes()
    elif args.action=="plan":
        if not 1<=args.limit<=100:p.error("--limit 1..100")
        result=discovery_plan(args.limit)
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
