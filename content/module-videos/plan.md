# Systems Thinking for Airtable: Module Videos Plan

**Overall Progress:** `60%`

*(35 of 58 subtasks 🟩. In-progress 🟨 subtasks count as 0. Updated Wed Oct 7, 2026, 1:35 PM PT.)*

## TLDR
Make one short video for each of the 8 modules of `github.com/RachaelQuisel/systems-thinking-for-airtable`, to post on Instagram and LinkedIn. They build Rachael's platform (airbnbai.rent, and her profile as a product / AI builder), in first person with no hype or absolutes, and every fact comes from the course text. Rachael records each module herself in Loom: her Airtable screen, her face in the corner bubble, and her own voice, reading from a scrolling teleprompter. Our part is the scripts, the teleprompter, an optional per-module recording checklist, and the captions.

## Critical Decisions
- **Voice and recording (changed Oct 7, 1:26 PM PT):** Rachael records Loom-style, with her face bubble and her own voice, reading from the teleprompter. Source: Rachael, "i want to make my voice the overlay" and "i want my head in the corner, like a Loom video, speaking". The British AI voice is dropped. The `bf_emma` 1.3x render (`module-01.mp4`) and the `voice-samples/` files (not in this repo) stay only as a reference for pacing and scene order. No more AI voiceovers are generated.
- **Teleprompter:** `../teleprompter/teleprompter.html`, one offline file she opens on her Mac by double-clicking. It holds all 8 scripts, one paragraph per scene, plus a box to paste any other script. It has a compact mode for a narrow window next to her webcam.
- **Scripts:** `read-aloud-scripts.md` is the source of truth. It was written with her voice-align skill, with one paragraph per scene in scene-list order. After any script edit, run `python3 content/teleprompter/build.py` to refresh the teleprompter.
- **What she shows on screen:** the "Screen-recording shots" in each module below and the starting states in `recording-runbook.md`. Sandbox bases with dummy data only, never client bases (Client A data is HIPAA-scoped). Hide the sidebar and any base list that shows client names before recording.
- **Existing raw footage:** `recordings/m1-scenes4-5-raw.mp4` (Oct 7, about 5 min; kept outside this repo because it shows Airtable screens with base IDs) is optional B-roll only. Its Line Total column was off screen.
- **Format after recording:** open. She can post the Loom as recorded (16:9 with the face bubble), or send us the export to cut a 1080×1920 vertical version with captions inside the IG safe zones. Ask her (Step 3).
- **Visual style:** the video shows her live Airtable screen. The teleprompter uses the brand colors: cream #FBF8F3, deep aqua #1D4E5B, sand #F3D9A4. Whether the watercolor brand look applies to these videos is open in Rachael's brand plan (D8), which is kept outside this repo.
- **Examples:** the course's real Client A and Client B cases, kept anonymous; no student or client first names. No host analogies (removed, since voice-align bans analogies).
- **Sequence:** she records a module after its pending checks in Step 4 are answered. Modules 2 and 6 wait on those checks.
- **Posting targets:** Instagram (Reels) and LinkedIn.

## Tasks:

- [x] 🟩 **Step 1: Inventory the course repo**
  - [x] 🟩 Clone the public repo to `src/repo/` (8 modules, syllabus, 3 appendices, ~43,000 words)
  - [x] 🟩 Inventory each module's title, learning goals, key concepts, examples and exercises (table in `scripts.md`)
  - [x] 🟩 Note the example sources: Client A (medical-coding education), Client B (magazine advertising); no host examples

- [ ] 🟨 **Step 2: Module 1: Schema Design in Airtable (prototype)**
  - [x] 🟩 Script: voice-align read-aloud version in `read-aloud-scripts.md` (170 words; total read zero, QuickBooks customer ID ×3, about 14,000 duplicate rows)
  - [x] 🟩 Scene list: 8 scenes, with screen recordings marked on scenes 4, 5 and 7
  - [x] 🟩 Screen-recording shots: Demo · Magazine Ads → *Contract Line Items* add formula `Line Total = {Quantity} * {Per Unit Cost}` → *Contracts* rollup `SUM(values)`; *Contacts* showing the same QB Customer ID on 3 rows → field created on *Advertisers*; base copy → *Insertion Orders*: lookup-only fields, move fields to the line item, delete backlinks, delete the table
  - [x] 🟩 Prototype render: slide-only `module-01.mp4` with `bf_emma` at 1.3x (47.9 s). Now a reference only; `module-01-v2-afheart.mp4` kept too (outside this repo; it was this folder's `module-01.mp4` in commit e669e7c)
  - [ ] 🟥 Rachael records Module 1 in Loom (face bubble, own voice, teleprompter)
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 3: Prototype review with Rachael**
  - [x] 🟩 Share `module-01.mp4` and `module-01-poster.png`
  - [x] 🟩 Rachael reviewed look, pacing, caption style and the 🎥 placement
  - [x] 🟩 Decide the voice: Rachael's own voice, recorded Loom-style with her face bubble; the British AI voice is dropped
  - [ ] 🟥 Ask Rachael: post each Loom as recorded, or send the export for a vertical cut with captions

- [ ] 🟨 **Step 4: Scripts and teleprompter**
  - [x] 🟩 Rewrite all 8 scripts with voice-align into `read-aloud-scripts.md` (149–170 words each) and sync the Voiceover sections in `scripts.md`
  - [x] 🟩 Remove the host analogy lines from `scripts.md`
  - [ ] 🟥 Rachael checks before she records: Module 2 AAPC example number "<EXAMPLE_AAPC_NUMBER, read digit by digit>" (the number in the course text, swapped for a placeholder here) may be a real student's; confirm or replace
  - [ ] 🟥 Rachael checks: Module 6 added definition "HIPAA, the United States health privacy law"; confirm
  - [ ] 🟥 Rachael checks: review the phrases changed to remove analogies and metaphors
  - [x] 🟩 Build the teleprompter with all 8 scripts, a paste box, and a compact mode (`../teleprompter/teleprompter.html`, tested in headless Chrome)
  - [ ] 🟥 Rachael opens the teleprompter on her Mac and does a test read; adjust from her feedback

- [ ] 🟨 **Step 5: Recording setup (Rachael records her own screen)**
  - [x] 🟩 Set up two sandbox bases with dummy data in the Demos workspace: "Demo · Magazine Ads" `<DEMO_BASE_ID_1>` (Advertisers, Contacts, Contracts, Contract Line Items, Insertion Orders, Projects, Tasks, Template Tasks) and "Demo · Course Enrollment" `<DEMO_BASE_ID_2>` (Students, Orders, Attendance; fields State, AAPC Number, Caseworker Email). Starting states and on-camera steps in `recording-runbook.md`
  - [ ] 🟥 Check Demo · Magazine Ads against the runbook starting state before she records Module 1. The Oct 7 recording created the LIVE fields Line Total, Contract Total and QuickBooks Customer ID; delete them if they are still there
  - [ ] 🟥 Optional: one-page `recording-checklist.md` with one short block per module: which Demo base and table to have open, the starting state, and prep (Module 1 scene 7 needs a duplicated base; Modules 3 and 5 need Fillout forms; Module 6 needs a second Airtable user for Preview)

- [ ] 🟨 **Step 6: Module 2: Data Normalization**
  - [x] 🟩 Script: voice-align version (170 words); AAPC number losing its leading zeros in a number field; formula pads to eight digits, copied into a text field; one feed → Students + Orders (example number pending Step 4 check)
  - [x] 🟩 Scene list: 7 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → *Students*: `AAPC Number` as Number (zeros gone) → padding formula by `LEN()` → duplicate → convert to Single line text → exact match succeeds; optional *Students* + *Orders* link
  - [ ] 🟥 Rachael records Module 2 in Loom (after the AAPC number check)
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 7: Module 3: Workflow Building**
  - [x] 🟩 Script: voice-align version (149 words); move the decision to an earlier step; state-specific enrollment forms (Florida, Indiana, South Carolina, Texas, headquarters default) through one SWITCH formula; manual process first
  - [x] 🟩 Scene list: 7 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → *Students* formula `Enrollment Form URL = SWITCH({State}, …)`; Fillout dashboard with 5 duplicated forms; automation send-email step inserting `{Enrollment Form URL}`
  - [ ] 🟥 Rachael records Module 3 in Loom
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 8: Module 4: Automation Architecture**
  - [x] 🟩 Script: voice-align version (170 words); write the link from the one-side; find or create on a unique key; the four questions
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → Automations: *Find records* in *Students* by key → found / not-found branches → *Create record* in *Orders* with the `Student` link set
  - [ ] 🟥 Rachael records Module 4 in Loom
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 9: Module 5: PDF & Document Generation**
  - [x] 🟩 Script: voice-align version (155 words); QuickBooks customer ID printed 3× → `ARRAYUNIQUE` rollup and fix the level; a generated PDF does not change after it is created, so plan for the second submission
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Magazine Ads → *Contracts*: lookup "123, 123, 123" next to the `ARRAYUNIQUE(values)` rollup; Fillout PDF field mapped to the rollup; change data → PDF unchanged → resubmit → new PDF
  - [ ] 🟥 Rachael records Module 5 in Loom
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 10: Module 6: Interface & Access Design**
  - [x] 🟩 Script: voice-align version (167 words); 148 caseworkers vs the 50-page limit; one page filtered on the logged-in user; HIPAA (definition pending Step 4 check); handoff as a constraint
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → Interface designer: page filter `Caseworker Email` is the current user's email; Preview as 2 users; Share menu showing public page vs read-only collaborator
  - [ ] 🟥 Rachael records Module 6 in Loom (after the HIPAA definition check)
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 11: Module 7: Project Management for Solo Consultants**
  - [x] 🟩 Script: voice-align version (169 words); a task is a record from a Template Tasks table; one record per status change; build only what the client will ask about
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Magazine Ads → *Tasks* grid (Project link, Status, date, owner); automation "When record created" in *Projects* → *Find records* in *Template Tasks* → repeating group *Create record* in *Tasks*; create Project D → tasks appear
  - [ ] 🟥 Rachael records Module 7 in Loom
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 12: Module 8: Client Communication**
  - [x] 🟩 Script: voice-align version (169 words); "the client is always right" vs "the client's reason is a good one"; Insertion Order table as a naming preference; sort constraint vs preference on the first call
  - [x] 🟩 Scene list: 7 scenes
  - [x] 🟩 Screen-recording shots: Demo · Magazine Ads → Interface designer: rename the page to "Insertion Orders" over *Contract Line Items*; hide the insertion-order fields in the layout
  - [ ] 🟥 Rachael records Module 8 in Loom
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do
