# Worked examples

Shortened processes from different kinds of work. Each shows where the
blocker turned out to be, which is rarely where people first look. Examples
1 to 4 come from real use in a marketing agency; 5 to 7 are typical patterns
from other functions, written to show the method, not measured results.

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

**No monitoring tool yet?** Start by hand, and keep it honest: write down
15 to 20 questions your buyers really ask, run each in ChatGPT, Perplexity
and Google (AI Overviews or AI Mode) three times (in a temporary chat, so memory doesn't favour your
own brand), and count a mention only if it shows up in at least two of three
runs. Log question, engine, mentioned yes/no, competitors named and cited
URLs in a sheet. Several markets: write the questions in each market's
language instead of translating them, and run them with that country's
location. Sister brands: decide up front whether one of your own brands
winning counts as a win or a loss. The first slice in a chat is smaller:
5 questions, one engine, one market, three runs, about 15 minutes. Scale
up next week. AI writes the weekly summary; a person sends it. When this
takes more than an hour a week, a monitoring tool with an API replaces the
manual runs.

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

## 5. Incoming invoices (finance)

**Outcome.** Every supplier invoice is checked, booked and ready for
payment approval within a day, without anyone retyping it.

**Where it stopped.** Access: invoices arrive as PDFs in three inboxes, and
the accounting tool's connector only takes uploads, not email.

**What fixed it.**
- **Access.** One shared inbox that forwards to the accounting tool's
  ingest address; the tool's API for reading the extracted fields.
- **Context.** A list of regular suppliers with expected amounts and cost
  centres, so outliers stand out.
- **Guardrails.** Deterministic checks (totals, VAT, duplicate invoice
  numbers); AI only for assigning the cost centre when it's ambiguous; a
  human approves every payment. Money is the expensive mistake.

## 6. Interview scheduling and candidate summaries (HR)

**Outcome.** A candidate who passes screening gets interview slots the same
day, and interviewers get a one-page summary beforehand.

**Where it stopped.** Context and trust: the recruiting tool had an API,
but nobody wanted AI-written summaries going to hiring managers unchecked,
and the criteria for each role lived in the hiring manager's head.

**What fixed it.**
- **Context.** A short scorecard per role, written once with the hiring
  manager.
- **Guardrails.** Scheduling runs unattended (reversible, low stakes). The
  summary goes through an advisory board (the hiring manager, the
  candidate, the employment lawyer) and only states what's in the CV and
  screening notes.

## 7. Sales call follow-ups (sales)

**Outcome.** A follow-up email and an updated CRM record within an hour of
every call.

**Where it stopped.** Access: call recordings were in a meeting tool whose
transcripts nobody had connected to anything.

**What fixed it.**
- **Access.** The meeting tool's connector for transcripts, the CRM's
  connector for writing the record.
- **Context.** The offer, pricing rules and what was promised to this
  account before, read from the CRM on every run.
- **Guardrails.** The CRM update runs on its own. The email is a draft the
  rep sends, after a board check for promises delivery can't keep.
