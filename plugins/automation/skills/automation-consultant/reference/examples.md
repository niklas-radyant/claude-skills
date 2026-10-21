# Worked examples

Real processes, shortened. Each shows where the blocker turned out to be,
which is rarely where people first look.

## 1. A new website, from domain idea to indexed page

**Outcome.** A new microsite goes from "we need a site for this" to live
and indexable without anyone clicking through a registrar, a DNS panel and
a hosting dashboard.

**Steps.** Find good domain names for the company and check availability →
register the domain → set DNS → set up hosting and deploy → set up TLS →
submit the sitemap for indexing.

**Where it stopped.** Not at the AI. The domain registrar had no usable API
for registration and DNS, so every run ended with "now log in and click
this". The credentials for the other tools were in different people's
password managers.

**What fixed it.**
- **Access, by switching tools.** Moved domains to a registrar with a full
  API (registration, DNS, transfers), so the whole chain runs from one
  session. The switching cost was a few hours; the manual step had cost that
  on every site.
- **Access, credentials.** A password manager service account the AI can
  read, with vaults holding scoped API tokens for the registrar, the host
  and the search console. One token to revoke.
- **Guardrails.** Decisions settled up front in a planning session (which
  domain, budget cap, which template), then one autonomous run with review
  agents checking the result in a real browser before anything counts as
  done (`afk`).

## 2. AEO monitoring: from dashboard to action

**Outcome.** Every week, the team knows which prompts the brand lost or won
in AI answers, why, and which page to change, without someone exporting
dashboards.

**Steps.** Pull visibility and citation data from the AI-search monitoring
tool → compare with last week → find the prompts that moved → check which
sources the engines cited instead → map to own pages → propose changes →
create tasks.

**Where it stopped.** The monitoring tool had the data, but the analysis
needed context it didn't have: which pages belong to which product, what
was already changed last month, what the client cares about this quarter.

**What fixed it.**
- **Access.** The monitoring tool's MCP server, plus read access to the
  project management tool for creating tasks.
- **Context.** A per-client knowledge base (goals, products, past changes,
  decisions) that every run reads first and that grows with every meeting
  and every correction.
- **Guardrails.** Recommendations go out as drafts. An advisory board
  (the client's head of marketing, the fact-checker, the editor) reviews
  them first; a human approves before tasks are created.

## 3. Content briefs

**Outcome.** A brief for each new page within a day of the topic being
picked, good enough that a writer starts without questions.

**Where it stopped.** The briefs were generic. Each writer re-asked the same
questions about tone, audience and what the client had rejected before.

**What fixed it.**
- **Context.** The writer's questions became the brief template. Past
  rejected drafts and the reasons became a charter for the advisory board.
- **Guardrails.** Board with "the writer who executes this" and "the
  searcher" roles. When a writer still has questions, the question gets
  added to the template, so the next brief answers it.

## 4. Citation checks

**Outcome.** Know when a page that AI answers used to cite stops being
cited, or when a competitor's page takes its place.

**Where it stopped.** Purely access: checks were done by hand in a browser.

**What fixed it.** A scheduled, deterministic job against the monitoring
tool's API: no AI judgement needed for detection, so none is used. AI comes
in only for the follow-up: comparing the two pages and drafting what to
change. Detection is deterministic; diagnosis is AI with a check.
