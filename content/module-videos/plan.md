# Systems Thinking for Airtable: Module Videos Plan

**Overall Progress:** `58%`

*(34 of 59 subtasks 🟩. In-progress 🟨 subtasks count as 0. Updated Wed Oct 7, 2026, 10:22 AM PT.)*

## TLDR
Make one short vertical video for each of the 8 modules of `github.com/RachaelQuisel/systems-thinking-for-airtable`, to post on Instagram and LinkedIn. They build Rachael's platform (airbnbai.rent, and her profile as a product / AI builder), in first person with no hype or absolutes, and every fact comes from the course text. Each module needs a read-aloud script, a scene list, Rachael's recorded voiceover, Airtable screen recordings, a rendered MP4 and captions. Rachael has reviewed the Module 1 prototype and chose to record her own voice.

## Critical Decisions
- **Format:** 1080×1920 vertical MP4, about 55–75 s, with burned-in captions inside the IG safe zones. Fits Reels and LinkedIn vertical video.
- **Visual style:** matches the loop carousel (its build script is kept outside this repo): cream #FBF8F3 / deep aqua #1D4E5B, accent #286575, sand #F3D9A4, Manrope headings, Source Sans 3 body. Keeps her posts visually consistent.
- **Voiceover:** Rachael records her own voiceover for all 8 modules. Kokoro (`af_heart`) is no longer the voice. It stays only as a timing placeholder until her recordings arrive.
- **Scripts:** `read-aloud-scripts.md` is the source of truth for every voiceover. It was written with her voice-align skill, with one paragraph per scene in scene-list order. The Voiceover sections in `scripts.md` match it.
- **Captions on video:** re-timed to Rachael's recorded audio, one caption at a time.
- **Real Airtable footage:** screen recordings replace the slides marked `🎥 SCREEN REC` in `scripts.md`. They're recorded in sandbox bases with dummy data, never in client bases (Client A data is HIPAA-scoped).
- **Examples:** the course's real Client A and Client B cases, kept anonymous; no student or client first names. No host analogies (removed, since voice-align bans analogies).
- **Sequence:** the remaining modules are rendered only after the template is locked and Rachael's recordings are in.
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
  - [x] 🟩 Prototype render: slide-only `module-01.mp4` (65.5 s, Kokoro placeholder) and `module-01-poster.png`, with the QA fixes in (IG safe zones, caption overlap, scene fades, dead air, hook, fact check)
  - [ ] 🟥 Final render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 3: Prototype review with Rachael**
  - [x] 🟩 Share `module-01.mp4` and `module-01-poster.png`
  - [x] 🟩 Rachael reviewed look, pacing, caption style and the 🎥 placement
  - [x] 🟩 Decide the voice: Rachael's own recording
  - [ ] 🟥 Lock the template in `src/build_module01.py`, generalized to a per-module scene config

- [ ] 🟨 **Step 4: Voiceover (Rachael records)**
  - [x] 🟩 Rewrite all 8 voiceovers with voice-align into `read-aloud-scripts.md` (149–170 words each) and sync the Voiceover sections in `scripts.md`
  - [x] 🟩 Remove the host analogy lines from `scripts.md`
  - [ ] 🟥 Rachael checks: Module 2 AAPC example number "<EXAMPLE_AAPC_NUMBER, read digit by digit>" (the number in the course text, swapped for a placeholder here) may be a real student's; confirm or replace
  - [ ] 🟥 Rachael checks: Module 6 added definition "HIPAA, the United States health privacy law"; confirm
  - [ ] 🟥 Rachael checks: review the phrases changed to remove analogies and metaphors
  - [ ] 🟥 Rachael records 8 voiceovers, one audio file per module, one paragraph per scene
  - [ ] 🟥 Sync each recording to its scenes and re-time captions to her audio

- [ ] 🟨 **Step 5: Airtable recording sessions**
  - [x] 🟩 Set up two sandbox bases with dummy data in the Demos workspace: "Demo · Magazine Ads" `<DEMO_BASE_ID_1>` (Advertisers, Contacts, Contracts, Contract Line Items, Insertion Orders, Projects, Tasks, Template Tasks) and "Demo · Course Enrollment" `<DEMO_BASE_ID_2>` (Students, Orders, Attendance; fields State, AAPC Number, Caseworker Email). Starting states and on-camera steps in `recording-runbook.md`
  - [ ] 🟥 Session 1, Magazine Ads shots: Modules 1, 5, 7, 8
  - [ ] 🟥 Session 2, Course Enrollment shots: Modules 2, 3, 4, 6
  - [ ] 🟥 Export clips cropped to 1080×1920 and named `mNN-sceneNN.mp4`

- [ ] 🟨 **Step 6: Module 2: Data Normalization**
  - [x] 🟩 Script: voice-align version (170 words); AAPC number losing its leading zeros in a number field; formula pads to eight digits, copied into a text field; one feed → Students + Orders (example number pending Step 4 check)
  - [x] 🟩 Scene list: 7 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → *Students*: `AAPC Number` as Number (zeros gone) → padding formula by `LEN()` → duplicate → convert to Single line text → exact match succeeds; optional *Students* + *Orders* link
  - [ ] 🟥 Render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 7: Module 3: Workflow Building**
  - [x] 🟩 Script: voice-align version (149 words); move the decision to an earlier step; state-specific enrollment forms (Florida, Indiana, South Carolina, Texas, headquarters default) through one SWITCH formula; manual process first
  - [x] 🟩 Scene list: 7 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → *Students* formula `Enrollment Form URL = SWITCH({State}, …)`; Fillout dashboard with 5 duplicated forms; automation send-email step inserting `{Enrollment Form URL}`
  - [ ] 🟥 Render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 8: Module 4: Automation Architecture**
  - [x] 🟩 Script: voice-align version (170 words); write the link from the one-side; find or create on a unique key; the four questions
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → Automations: *Find records* in *Students* by key → found / not-found branches → *Create record* in *Orders* with the `Student` link set
  - [ ] 🟥 Render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 9: Module 5: PDF & Document Generation**
  - [x] 🟩 Script: voice-align version (155 words); QuickBooks customer ID printed 3× → `ARRAYUNIQUE` rollup and fix the level; a generated PDF does not change after it is created, so plan for the second submission
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Magazine Ads → *Contracts*: lookup "123, 123, 123" next to the `ARRAYUNIQUE(values)` rollup; Fillout PDF field mapped to the rollup; change data → PDF unchanged → resubmit → new PDF
  - [ ] 🟥 Render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 10: Module 6: Interface & Access Design**
  - [x] 🟩 Script: voice-align version (167 words); 148 caseworkers vs the 50-page limit; one page filtered on the logged-in user; HIPAA (definition pending Step 4 check); handoff as a constraint
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Course Enrollment → Interface designer: page filter `Caseworker Email` is the current user's email; Preview as 2 users; Share menu showing public page vs read-only collaborator
  - [ ] 🟥 Render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 11: Module 7: Project Management for Solo Consultants**
  - [x] 🟩 Script: voice-align version (169 words); a task is a record from a Template Tasks table; one record per status change; build only what the client will ask about
  - [x] 🟩 Scene list: 8 scenes
  - [x] 🟩 Screen-recording shots: Demo · Magazine Ads → *Tasks* grid (Project link, Status, date, owner); automation "When record created" in *Projects* → *Find records* in *Template Tasks* → repeating group *Create record* in *Tasks*; create Project D → tasks appear
  - [ ] 🟥 Render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do

- [ ] 🟨 **Step 12: Module 8: Client Communication**
  - [x] 🟩 Script: voice-align version (169 words); "the client is always right" vs "the client's reason is a good one"; Insertion Order table as a naming preference; sort constraint vs preference on the first call
  - [x] 🟩 Scene list: 7 scenes
  - [x] 🟩 Screen-recording shots: Demo · Magazine Ads → Interface designer: rename the page to "Insertion Orders" over *Contract Line Items*; hide the insertion-order fields in the layout
  - [ ] 🟥 Render with the locked template, Rachael's voiceover and recordings
  - [ ] 🟨 Caption: LinkedIn drafted (check against the voice-align script); IG to do
