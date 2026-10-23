# Bird-Dog Intelligence | Decodo source registry

A source-led, two-sided commercial opportunity research kit: **where to look for organisations asking for services**, **where to find agencies with published referral programmes**, and **how to collect evidence without turning weak signals into fictional leads**.

**Status:** researched source directory + executable Decodo CLI scanner; NOT an autonomous sales, outreach or payment bot. Nothing here is a booked commission, an accepted referral, or a verified live sales lead until humans confirm it.

This project lives within [sophiamaybea/mcp-web-scraper](https://github.com/sophiamaybea/mcp-web-scraper) so it can be used beside the Decodo MCP server already in that repo. The `bird-dog-intelligence/` folder is self-contained and can be moved into a standalone repository later.

## Source of truth

| File | Purpose |
|---|---|
| [registry/sources.json](registry/sources.json) | **Machine-readable source inventory**: real source sites, official API documentation, discovery queries, priority, side of marketplace, collection method, permissions and cadence. |
| [registry/buyers.json](registry/buyers.json) | Four example published referral schemes with links, terms, caveats and human-approval status. |
| [registry/toolkit.json](registry/toolkit.json) | Verified GitHub repositories to assemble Decodo + scoring + workflows. |
| [AGENTS.md](AGENTS.md) | Agent instructions: discover → verify → match → human review; provenance and compliance rules. |
| [docs/SOURCING_PLAYBOOK.md](docs/SOURCING_PLAYBOOK.md) | Specific places and filters to find tenders, RFPs, private buyers and referral programmes. |
| [docs/DECODO_SETUP.md](docs/DECODO_SETUP.md) | Hosted MCP and CLI instructions, including connecting agents on an iPad/cloud environment. |
| [docs/ECONOMICS.md](docs/ECONOMICS.md) | Wolfram-backed example model, referral EV and why research contracts should come first. |
| [docs/COMPLIANCE.md](docs/COMPLIANCE.md) | Platform, procurement and privacy safeguards. |
| [run.py](run.py) | Standard-library Python tool: build a search plan, run Decodo search jobs and review-approved URL scrapes. |

## Where demand is found

1. **Official procurement feeds FIRST.** UK Contracts Finder OCDS data, Find a Tender OCDS, EU TED Search API, US SAM.gov, NYC procurement datasets. Official APIs normally outperform site scraping for structured tenders and dates. Their adapter entries are in the registry and marked `official_api`, not falsely represented as Decodo search calls.
2. **Private-sector direct buying requests.** Use Decodo `search` with quotes, sectors and source domains to discover `RFP`, `RFQ`, `seeking agency`, `website redesign`, `AI automation consultant`. Use Decodo `scrape` only on a reviewed, publicly accessible original source.
3. **Agency partners and referrers.** Use Decodo searches to discover referral and partnership programmes. Confirm the programme's terms and get agreement before making introductions.
4. **Directories / job marketplaces.** Manual research only until specific access terms are reviewed. A job advert or an old-looking website is not proof that a business wants to purchase an external project.

### Quick commands (Python 3.10+; Node 22+ for Decodo CLI)

```bash
cd bird-dog-intelligence
python3 run.py validate
python3 run.py plan --max-queries 20
npm install -g @decodo/cli
export DECODO_AUTH_TOKEN='YOUR_KEY'  # Or run: decodo setup
python3 run.py scan --max-queries 12 --max-results 10 --geo gb
python3 run.py scan --side buyer --max-queries 6 --geo gb
# Only after reviewing the source site's access terms and URL:
python3 run.py scrape --url 'https://www.semibold.co.uk/referral-scheme/' --confirmed-rights
```

The real scanner invokes **`decodo search`**, collects search result URL/title/snippet with source, and writes to a local ignored `output/` folder. It uses no AI model to invent details. It does not automatically scrape every search result; that requires separate site-specific permission checking. If the CLI is unavailable, `plan` still creates a usable Decodo task list.

**Important:** The scanner is an *initial candidate discovery pipeline*, not a verified tender importer, buyer-qualified CRM, or guaranteed parse of all third-party output formats. The official APIs still need live integrations. This separation avoids presenting search snippets as confirmed opportunities.

## Connecting an AI agent straight to the registry

Raw manifest URL:
```text
https://raw.githubusercontent.com/sophiamaybea/mcp-web-scraper/main/bird-dog-intelligence/registry/sources.json
```

Tell the agent: "Read AGENTS.md and sources.json from the bird-dog-intelligence directory. Prioritise official APIs, then use Decodo search for permitted queries. Do not treat scraped pages or search snippets as verified. Produce source-linked candidate records; do not contact anyone without my approval."

## What counts as commercially useful

The priority is **paid, authorised research deliverables first**, then **mutually agreed referrals**. A listed 10% referral rate does not guarantee that a cold researched company is eligible, wants contact, or will buy. Public tenders are research intelligence, not automatically commissionable referrals.

**Do not put Decodo API keys, personal leads, private customer dossiers or negotiated agreements in this public repository.** Keep them server-side/private.

## Evidence and design

The registry was assembled from official procurement, Decodo and agency referral pages, checked on **23 October 2026**. It deliberately distinguishes official API endpoints, search surfaces, known referral pages and manual-review directories. Operational access rights, API parameters, commissions, legal requirements, deadlines and scheme eligibility may change; reverify before acting.

The source collection rules follow the uploaded GitHub-repository research skill: inspect through APIs, attribute sources, respect limits, and do not confuse hypotheses with established facts.
