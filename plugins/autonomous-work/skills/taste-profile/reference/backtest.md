# Blind backtest of the design critic

## 1. Collect cases

From the transcripts (step 1 of the skill), find the moments where the agent
showed a built screen and the owner reacted. You need:
- every clear rejection or correction round
- the accepted state after the fix, as a control
- any explicit praise

Aim for 8–15 cases, at least 5 of them rejections.

For each case, get the screenshot of the state that was judged. These are
usually already in the transcripts:
- the agent's own screenshot tool results (base64 images in `tool_result`
  blocks)
- screenshots the owner pasted

Decode them to PNG files. If the image is missing, re-render the route at
the commit that was judged.

Write each case to `<backtest-dir>/<id>/case.md`:
- date and session
- surface, and the seat it was judged from
- the owner's verdict, verbatim
- the concrete complaints
- what the accepted fix did
- the commits
- a customer-data flag

In `INDEX.md`, list every case with the findings a good critic must raise.
Keep the whole directory out of git (`.gitignore` containing `*`) whenever
screenshots show customer data.

## 2. Split

Use some cases as examples in the profile or the project's design-taste doc.
**Hold the rest out.** The held-out cases measure whether the critic can
judge screens it has never seen described. If every case appears in the
profile, you are testing recall.

## 3. Make it blind

```bash
B=$(mktemp -d)/blind
mkdir -p "$B/A"
cp <backtest-dir>/<case>/before-*.png "$B/A/"   # repeat per case, letters A, B, C…
```

Mix the controls (accepted states) in among the rejections. Keep a key file
that maps letters to cases, outside the blind directory. The critic must not
be able to read `case.md` or `INDEX.md`, so tell it explicitly not to look
under the backtest directory.

## 4. Run

One critic per case, in parallel. The prompt contains:
- `BACKTEST MODE`
- "do NOT take your own screenshots; judge only the screenshots given"
- "do NOT read anything under <backtest-dir> or .afk"
- the screenshot folder
- a neutral description of the surface ("a customer meeting page")
- the seat

Never give it the verdict or any hint of it.

## 5. Score

| | Count |
|---|---|
| Rejections caught (verdict FIX or BLOCKER, the main complaints named) | strong / partial / missed |
| Controls passed (PASS, or FIX with only the points the owner would also raise) | |
| False alarms (MAJOR findings on something the owner accepts) | |

Two typical failure patterns, each with its fix:
- **Everything gets flagged, including accepted screens.** Severity is
  miscalibrated. The critic's first-reaction step caps the verdict; add the
  owner's re-judged controls as calibration.
- **Visual bloat gets caught, structure doesn't** (wrong grouping, things
  that belong on another page, one row per item instead of one per source).
  Add the missed structural rule to the profile or the taste doc, with its
  case.

Change one thing, re-run all the cases, and compare. Record every round, and
every re-judging by the owner, in `INDEX.md`.
