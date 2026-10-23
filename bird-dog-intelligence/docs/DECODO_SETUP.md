# Connecting Decodo to this repository

## Hosted MCP, easiest for an iPad/cloud AI agent

Current official hosted Decodo MCP URL:
```json
{
  "mcpServers": {
    "Decodo": {
      "url": "https://mcp.decodo.com/mcp?toolsets=web,search",
      "headers": {
        "Authorization": "Bearer <WEB_DATA_API_KEY>"
      }
    }
  }
}
```
Keep the key in the client/server secret store. **Do not commit a real key**. Legacy subscriptions might use a `Basic` token instead of a `Bearer` API key. The official tool names for the relevant toolsets include `search`, `scrape_as_markdown`, `map`, `crawl_start`, `crawl_status`, and `crawl_results`. Agent instructions live in [../AGENTS.md](../AGENTS.md).

### What to tell the agent

> Read the raw GitHub file `bird-dog-intelligence/registry/sources.json`, then `AGENTS.md`. Plan 10 high-priority discovery searches for privately published website, AI and software RFPs and agency referral schemes. Call Decodo's search tool. Only scrape original publicly readable issuer pages after verifying access rights. Return citations and mark all unverified fields as unknown. Never email anyone automatically.

**Source URL:** https://raw.githubusercontent.com/sophiamaybea/mcp-web-scraper/main/bird-dog-intelligence/registry/sources.json

## Decodo CLI

Current official repository: https://github.com/Decodo/cli . Requires Node.js 22+ according to its README.

```bash
npm install -g @decodo/cli
export DECODO_AUTH_TOKEN='YOUR_API_KEY'
decodo search '"website redesign" "request for proposal"'
decodo scrape 'https://www.semibold.co.uk/referral-scheme/'
decodo map 'https://example.org/' --limit 20
```

You may use `decodo setup` to save a local key rather than the environment variable. The runner executes the official CLI without a shell and never prints a secret itself.

```bash
python3 run.py validate
python3 run.py plan --max-queries 12
python3 run.py scan --max-queries 12 --max-results 10 --geo gb
python3 run.py scan --side buyer --max-queries 8
python3 run.py scrape --url 'https://www.semibold.co.uk/referral-scheme/' --confirmed-rights
```

**Note:** `plan` and `validate` are key-free. `scan` and `scrape` consume API requests and require a configured Decodo CLI. Browser scraping tools can access sites technically without a right to republish their content or personal data.

## Deployment path

Use this public GitHub directory for **configuration and provenance only**. Store private leads, consent status, researched reports and financial records in a private Supabase schema (RLS). For recurring jobs use Trigger.dev/Render/Coolify or controlled GitHub Actions with secrets. First test a small budget, track failures and avoid unnecessary refreshes. Avoid placing collected contact records in a publicly accessible GitHub file or workflow artefact.

## Buyer discovery and closing prep

The companion `registry/buyer_channels.json` documents official first-party programme routes and discovery-only directories. `docs/DEAL_PLAYBOOK.md` describes written terms, introduction consent and the commission/invoice process.

```bash
cd bird-dog-intelligence
python3 buyer_pipeline.py channels
python3 buyer_pipeline.py plan --limit 12
python3 buyer_pipeline.py scan --limit 8 --geo gb
python3 buyer_pipeline.py brief --buyer dispense_digital
```

A scan runs **Decodo web search only**. It does not automatically inspect agency contact pages, submit a programme registration, send outreach, secure partner agreements or generate paid commissions. Each candidate needs a confirmed first-party page and manual commercial approval.
