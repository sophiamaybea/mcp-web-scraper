# Verification notes and references (23 October 2026)

This source directory is based on live checks of *official* pages and GitHub repositories. It is not a completed lead harvest.

Decodo:
- https://github.com/Decodo/mcp-server — currently documents hosted Bearer authentication, MCP web/search tools and optional Map/Crawl.
- https://github.com/Decodo/agent-skills — how to route requests for CLI, MCP, REST.
- https://github.com/Decodo/cli — documented Node.js 22+; `decodo search`, `decodo scrape`, `decodo map`, `decodo crawl`.
- https://decodo.com/web-data-api — four Web Data API functions; free-tier wording/pricing may change.

Tenders:
- https://www.contractsfinder.service.gov.uk/apidocumentation
- https://www.find-tender.service.gov.uk/Developer/Documentation
- https://docs.ted.europa.eu/api/latest/search.html
- https://open.gsa.gov/api/get-opportunities-public-api/
- https://www.nyc.gov/site/mocs/resources/public-procurement-sites.page
- https://data.cityofnewyork.us/City-Government/City-Record-Online/dg92-zbpx

Published buyers:
- https://www.semibold.co.uk/referral-scheme/
- https://synmek.com/referrals
- https://www.dispensedigital.co.uk/seo-web-design-affiliate-programme/
- https://circulardesign.io/referral-scheme/

Proof policy:
- `known_public_page` means a real published scheme page, not the publisher's approval of this project.
- `official_api` means a documented API/data feed, not an implemented adapter.
- `decodo_search` is executable discovery. It yields **candidates**, never committed business.
- `manual_review` requires site-specific approval before automation.
- If a source changes or disappears, mark `enabled:false` and record the review date.
