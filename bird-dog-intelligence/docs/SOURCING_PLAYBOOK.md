# Sourcing playbook: where Decodo should look

## A. Real buying requests, strongest first

**UK Contracts Finder:** https://www.contractsfinder.service.gov.uk/contractfinder . Look for *Opportunity*, *Future Opportunity*, not only *Awarded*. Filter with procurement stage, publication date, software/website/marketing service keywords and deadline. **In production use the OCDS API**: https://www.contractsfinder.service.gov.uk/apidocumentation . Keep the notice ID / OCID to prevent double counting.

**UK Find a Tender:** https://www.find-tender.service.gov.uk/ . Use the official OCDS release and record JSON described at https://www.find-tender.service.gov.uk/Developer/Documentation . Distinguish opportunity from award, check closing date and public procurement rules.

**EU TED:** https://ted.europa.eu/ . Prefer the public `POST /v3/notices/search` documented at https://docs.ted.europa.eu/api/latest/search.html ; filter CPV (services/software), place, tender deadlines, publication. The official portal explicitly recommends the API instead of heavy scraping of its CMS.

**US SAM.gov:** https://sam.gov/content/opportunities . Official search API https://open.gsa.gov/api/get-opportunities-public-api/ requires its own API key; filter active notices and the relevant contract category. Check whether suppliers from the UK are eligible before recommending.

**New York City:** start at https://www.nyc.gov/site/mocs/resources/public-procurement-sites.page and open City Record, Procurement Navigator, and PASSPort Public. For machine-readable notices use NYC Open Data https://data.cityofnewyork.us/City-Government/City-Record-Online/dg92-zbpx . Some solicitation attachments need registration; never bypass it.

**Devolved UK:** https://www.publiccontractsscotland.gov.uk/ , https://www.sell2wales.gov.wales/ , and https://etendersni.gov.uk/ . Registry marks these as `manual_review` until an approved feed/connector is established.

**Public private-sector requests:** Decodo searches rather than blind crawling:
- `"website redesign" "request for proposals" deadline`
- `"website development" "request for proposal" budget`
- `site:.org "website redesign" "RFP"`
- `"AI automation" "request for proposal"`
- `"workflow automation" "seeking consultant"`
- `"software development" "request for proposal" deadline`
- `"seeking software development partner"`
- `"SEO agency" "request for proposal"`

Always click through to the **original buyer's** published page. Discard expired, duplicated, speculative or reseller-only notices, and distinguish publicly posted RFP from a generic marketing blog.

## B. Organisations with published referral rewards

Four **examples actually checked on official pages**, not pre-agreed buyers:
- Semibold: https://www.semibold.co.uk/referral-scheme/ , 10% on qualifying first website project.
- Synmek: https://synmek.com/referrals , tiered published website/software/marketing partner percentages.
- Dispense Digital: https://www.dispensedigital.co.uk/seo-web-design-affiliate-programme/ , published 15% recurring on qualifying referred account revenue; programme describes freelancer/agency referrals.
- Circular Design: https://circulardesign.io/referral-scheme/ , £200 for suitable purpose-led web design projects.

Decodo buyer searches:
- `"web design" "referral scheme" "commission"`
- `"website development" "referral programme"`
- `"AI automation agency" "referral partners"`
- `"software development" "partner programme" commission`
- `"digital marketing" "affiliate programme" agency`

The system should **verify whether newly discovered, independently researched companies can be referred under the rules**, preferably before research costs are incurred.

## C. People paying for specialised research

Use current platform-approved job search for paid lead-research assignments; example directory: https://www.upwork.com/freelance-jobs/lead-generation/ . Make a research contract with clear acceptance criteria and payment terms first, then work. **Do not crawl Upwork or contact clients off-platform unless their actual terms permit it.**

## D. What NOT to mark as a verified deal

Old websites, company fundraising announcements, hiring adverts, site speed errors, blog complaints, domain registration, comment threads and generic social posts are *signals*, not proof of a funded buying request. The same customer may post through multiple tender portals, so use unique notice IDs and organisation/project similarity.

## E. Classification of discovery methods

`official_api` = use the original structured data service and its permitted pagination/rate limits.

`decodo_search` = Decodo search is permitted as a discovery stage; fetch individual issuer pages only after access terms/robots review.

`known_public_page` = documented referral page; revisit and confirm eligibility/terms.

`manual_review` = human-only until platform access and rights are explicitly approved.

Country- or sector-specific sources can be appended to `registry/sources.json` with clear provenance and safety flags. Do not treat a source URL itself as an invitation to bulk scrape that host.
