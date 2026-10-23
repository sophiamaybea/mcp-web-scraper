# Buyer acquisition and deal-closing playbook

**Objective:** secure the *buyer agreement first*, not scrape 500 company inboxes and hope one pays. Two distinct products are (A) an agreed-fee, specified research deliverable and (B) a permission-based, attributable introduction earning a qualifying commission.

## 1. Find buyers through evidence of demand for leads

**Tier 1: explicit published referral programmes.** Check `registry/buyer_channels.json` for four example agency-owned schemes and their official contact routes. These show a way to **apply** or **ask**, not a guarantee of acceptance.

**Tier 2: public company sites discovered by Decodo searches.** Search:
- `"web development agency" "referral programme" "commission"`
- `"software agency" "introducer fee"`
- `"AI automation agency" "referral partner"`
- `"we pay for qualified leads" agency`
- `"partner with us" "agency" "referrals"`
- `"marketing agency" "pay per qualified lead"`

**Tier 3: curated agencies in DesignRush, The Manifest or GoodFirms.** Only use these directories as discovery aids and inspect **the agency's own official partner/contact page**. Being listed as an agency proves neither that it needs leads nor that it has a commission programme. A directory's automation permissions must be checked before crawling it.

**Tier 4: firms commissioning paid research.** Manually review platform-approved lead-generation or opportunity research contracts (e.g. Upwork); agree on exact data fields, acceptance criteria, allowable sources, deadline, deliverable and payment terms **before** collecting datasets. Observe platform rules.

**Tier 5: PartnerStack.** Use permitted PartnerStack marketplace programme discovery and join programmes following their application workflow. Affiliate-link programmes selling SaaS subscriptions are **not interchangeable** with custom agency-project introduction agreements.

For every new buyer, record `agency_name`, `official_domain`, `service_vertical`, `public_programme_url`, `published_contact_route`, `payment_model`, `agreement_status`, `geography`, `minimum_budget`, `next_action` and `source_verified_at`. Do **not** bulk collect employee names, private contact details, guessed addresses or personal mobile numbers.

## 2. Find the right route to approach them

Order of preference:
1. Their explicit **referral/affiliate/partner registration form**.
2. Their official **partnerships/introducer** or sales enquiry page.
3. A **generic corporate business contact** email published on their own website (only where lawful and appropriate).
4. A relevant in-platform **partner marketplace** application.

Use Decodo `search` with e.g. `site:agency.example (referrals OR partnership OR contact)` to find the right page. On reviewed, permitted sites, use `map` for `/partner`, `/referral`, `/contact`, `/business-development` paths and `scrape_as_markdown` for the chosen **official page**. Extract only corporate/general business contact routes, programme forms, factual terms and evidence URLs.

**Do not submit forms, send emails, book calendars, or accept terms automatically.** The system prepares a concise proposal for user review. Do not assert a referral right until the business has confirmed it.

## 3. The buyer-first conversation (what actually closes it)

### First message: ask for the rules, not a payment upfront

Subject: Partnership enquiry: research-backed introductions for [service]

Hello,

I'm developing a small, evidence-led sourcing service that identifies organisations actively seeking [website development / software integrations / AI automation], supported by original public requests rather than speculative lead lists.

I came across your [referral/partner] programme and wanted to check whether you accept **independently researched prospects**, provided the organisation wants an introduction and there is a documented attribution process.

If this is relevant, could you confirm your ideal project size and geography, how a referral is registered, what counts as a new qualifying client and when any commission becomes payable? I would be happy to start with a small, clearly specified pilot once we agree the terms.

Kind regards

[Your name]

**Do not imply** that you represent the prospective customer, have their permission, or already have a lead when you do not.

### Questions on the first call or reply

1. Are independent, research-identified introductions acceptable, or do referrals need to be from existing clients/network contacts?
2. What is your minimum contract value, geography, service stack and monthly intake capacity?
3. Which service lines qualify and which are excluded?
4. How is a lead **registered and attributed** before it reaches you (partner code, deal registration, dated reply, CRM record)?
5. What happens if this business is already in your sales pipeline?
6. What is your qualifying event: booked meeting, sales-qualified lead, signed contract, deposit, project kickoff, project completion or paid invoice?
7. What amount is paid, on what base (before/after VAT, pass-through costs, retainers) and when?
8. Is there an attribution protection window (e.g. 90 days) and is there a clawback/refund policy?
9. How will you confirm a lead's status and eventual payout without exposing unnecessary customer data?
10. Are there sectors, tender rules or referral restrictions that make commission inappropriate?

After obtaining their answers, send a **one-page commercial schedule** for written agreement.

## 4. Negotiable commercial schedule (NOT legal advice)

```text
Buyer organisation:
Referring research provider:
Effective date / jurisdiction:
Eligible service categories and geographical territories:
Qualification definition (what exactly the referrer must deliver):
Exclusions (existing pipeline, previous clients, public tender restrictions, duplicates):
Registration and acknowledgement process:
Attribution protection period:
Consent and appropriate contact-channel requirements:
Reward model (fixed fee, report price, % of specified revenues):
Payment trigger and days to pay:
Evidence of qualified/paid milestone (without unnecessary personal data):
Refunds, cancellation and clawbacks:
Disputes, confidentiality, permitted data reuse, termination:
Non-exclusivity/exclusivity, if any:
Approval and signatures:
```

Without this, a scheme advertisement or friendly reply is *not* a proven right to a commission. For public tenders, check tender and ethics rules; consider selling a permitted research brief instead of brokering contract access.

## 5. First paid pilot options

**Fixed-fee brief:** Sell 5–10 original, sourced and live RFP opportunities with verified service requirement, deadline, issuer URL and acceptance criteria; charge a mutually agreed price for research work under a written contract. Deliverable should not include private contact lists.

**Qualified-introduction fee:** Agree a specific lead-acceptance definition and payment amount *before* sourcing, then obtain the prospect's permission before making an introduction.

**Commission:** Use the agency's eligible first-contract basis and payment trigger. Keep a record of introduction permission, partner acknowledgement, the signed project milestone and invoices.

No claim of actual income until money arrives.

## 6. Pipeline / decision gates

```text
candidate
  → programme_verified
  → contact_route_verified
  → outreach_reviewed
  → partner_contacted [only after human action]
  → partner_replied
  → pilot_terms_agreed [documented in writing]
  → eligible_opportunity_found
  → prospect_opted_into_introduction
  → agency_accepts_registration
  → introduction_completed
  → project_status_confirmed
  → payment_due
  → paid
```

The first four steps may be automated as research; **all communications, contract acceptance and introductions need separate human authorisation**. Never promote a candidate directly to `paid` or `partner_approved` just because a site has a commission banner.

## 7. GDPR, PECR and source-access gates

- For the UK, ICO guidance says electronic B2B marketing rules differ between corporate subscribers and sole traders/individual subscribers. Corporate B2B emails may not require PECR consent, but identity/opt-out rules and UK GDPR (when personal data are used) still apply. A sole trader generally needs consent or another narrow permitted exception. See https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/
- Only research publicly offered **corporate contact channels** and preserve proof of where they were published. If legal status is unclear, avoid assuming the corporate exception.
- Record suppression/opt-outs in private storage. Do not auto send, bulk enrich or scrape protected social platform inboxes.
- Decodo helps technically retrieve pages, but that does not override a website's terms, data permissions, or privacy law.

## 8. Recommended daily operator loop

1. Create a Decodo plan of ten **buyer-first** queries from `registry/buyer_channels.json`.
2. Validate two or three official first-party partnership pages.
3. Send no more than a few individually reviewed relevant enquiries after confirming the contact route and applicable rules.
4. Prioritise written pilot agreements and a documented way to register opportunities.
5. Only then pay for larger Decodo searches on the agreed service niches.
6. Calculate acceptance rate, commission eligibility, hours per verified opportunity, cash collected and *days to payout*, rather than raw scraped rows.

**Source evidence checked 23 October 2026:** official buyer-owned pages in buyer_channels.json; DesignRush/GoodFirms/The Manifest directories; PartnerStack documentation; ICO B2B marketing guidance. These are examples, not a curated list of committed purchasing partners.
