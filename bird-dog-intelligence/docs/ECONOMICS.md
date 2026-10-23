# Commercial economics: conservative decision model

The paid unit is **verified, contractually acceptable intelligence**, not scraped rows. At the start, commission eligibility, close probabilities, payouts and research labour are all unmeasured.

## Core equations

```text
Expected contribution (referral) =
 P(valid) × P(eligible | valid) × P(close | eligible) × P(paid | close)
 × eligible commission amount
 - search cost - qualification cost - transaction cost

Expected contribution (research deliverable) =
 P(deliverable accepted) × signed research fee
 - research cost - transaction cost

Value per hour = expected contribution / total research hours
```

Never use public contract value as if it were an affiliate commission. Public-sector tender data is usually valuable as research or sourcing intelligence, **not** automatic referral fees.

## Hypothetical worked comparison (computed with Wolfram Language)

| Path per investigated lead | Assumed gross payout | Other assumptions | Cost | Example expected contribution |
|---|---:|---|---:|---:|
| Pre-contracted research report | £120 | P(accepted)=0.55 | £22 | **£44.00** |
| Website successful referral | £500 | P(eligible)=0.45, P(close)=0.12, P(paid)=1 | £22 | **£5.00** |
| AI integration successful referral | £1,200 | P(eligible)=0.32, P(close)=0.08, P(paid)=1 | £31 | **−£0.28** |

The probabilities, £500/£1,200 fees and costs above are **fabricated modelling inputs**, NOT measured Decodo conversion rates or actual contracted partner terms.

For the referral paths to outperform the **£44** illustrative research path, holding all other numbers fixed, the required closing probabilities would be about **29.3%** (web) and **19.5%** (AI). These are sensitivity thresholds, not plausible market benchmarks.

A Bayesian small-sample example with a Beta(1,1) prior and 2 closes out of 20 eligible leads has Beta(3,19) posterior mean **13.64%**, with illustrative 90% central range about **4.0–27.1%**. Actual modelling should include lead age, customer segment, lead source, right-to-refer, commission payment delay and capacity. Do not infer precise conversion rates from tiny samples.

## Matching rather than greedy routing

An agency may have capacity for only one introduction, and a business should not be introduced to multiple providers without consent. Solve a constrained assignment problem:

```text
maximise Σ(i,j) expected_contribution[i,j] * x[i,j]
subject to Σ(j) x[i,j] ≤ 1 for each opportunity
           Σ(i) x[i,j] ≤ capacity[j] for each agency
           x[i,j] = 0 if compliance, consent or eligibility fails
           x[i,j] ∈ {0,1}
```

In one hypothetical 3×3 matrix, independent greedy choice totals 191 units whereas the best one-to-one assignment totals 287; this was computed with Wolfram Language and illustrates why global matching can matter. Use [google/or-tools](https://github.com/google/or-tools) for larger operational assignments. Optimisation comes **after**, never before, the legal/consent/eligibility gates.

## What to measure in the first month

Track search queries, candidates found, genuine dated RFPs, duplicate rate, research hours, acceptance rate, agency partnership agreements signed, authorised introductions, conversion and paid amounts. Compare return per hour and *time to cash*. Start with small tests across website, AI automation and software; double down only on evidence of payment.
