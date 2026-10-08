# Systems Thinking for Airtable: short vertical videos, one per module

Drafted Wed Oct 7, 2026 PT. Written as Rachael, first person.

**Source:** `github.com/RachaelQuisel/systems-thinking-for-airtable` (public; cloned to `src/repo/`). It's 8 modules plus a syllabus and 3 appendices, about 43,000 words, "built from eleven months of production builds, July 2025 – June 2026."

**What the examples are:** every case study in the course comes from two client builds. **Client A** is a medical-coding education platform (WooCommerce + Airtable + Fillout + Zapier). **Client B** is a magazine advertising operation (Airtable + Fillout + QuickBooks). **The course has no host examples.** So the scripts use the course's real cases, kept anonymous the way the course does it ("an education build", "a magazine advertising build"). Voiceovers follow the voice-align skill and contain no analogies; the earlier host-angle notes were removed.

**Rules I followed**
- Every number, field name and story comes from the module text. Student and client first names in the course (e.g. in Modules 2 and 4) are left out on purpose.
- No hype or absolutes. Where the course says "always" or "never" (e.g. "name every table with a primary-field formula, always"), the scripts soften it or attribute it as Rachael's own habit.
- **Screen-recording markers:** `🎥 SCREEN REC` marks scenes where real Airtable footage should replace the animated slide. Record those in a **demo/sandbox base with dummy data, not the client bases.** Client A data is student/HIPAA-scoped.
- Runtimes assume about 150 words a minute. Each script is 45–75 s.

---

## Module inventory

| # | Title | Learning goals (from the module) | Key concepts | Examples / exercises |
|---|---|---|---|---|
| 1 | Schema Design in Airtable | Model the thing before you automate it; place every value at the right level | One-to-one tables → delete one; store each value where it's true; Contract → Line Item structure; attribute lives where it's first single-valued; product as attributes that filter each other; one attachment field + type; primary-field formula | Client B: ~14,000 Insertion Order rows of only lookups; contract total reading zero; QuickBooks ID printed 3×; inventory per *position* not product (a 90-minute reversal). Client A: "attachment internship / attachment practicode" fields. Exercises: find your one-to-one; place three attributes; collapse a field-per-type |
| 2 | Data Normalization | Get data into a shape the model can use; match records on something real | One import, two tables (upsert entity, always create event); match by a real unique key; rebuild a mangled key; formula match-key + formula primary field guard; lookup-to-static migration | AAPC number `<EXAMPLE_AAPC_NUMBER>` stored as a number lost its leading zeros; Blackboard grade import (ID → email → name key changes); ~693 unlinked migrated line items. Exercises: split a feed; break and rebuild a key; paste-to-link a backlog |
| 3 | Workflow Building | Build the manual pipeline first, then automate; move the hard part to the layer that can do it | Fillout parent/child forms; branch upstream; product cascade; fan one submission out into many records; update form vs create form | State-specific enrollment PDFs (FL, IN, SC, TX, HQ) via one SWITCH formula; weekly attendance form → 7 Attendance records via webhook; signed-contract one-field update form. Exercises: parent/child pair + orphan view; branch upstream; cascade |
| 4 | Automation Architecture | Make automations do exactly what you meant and nothing else | Search-or-create on a unique key with two explicit branches; write the link from the one-side; filter before sort, take last; keep the flow in one debuggable place; AI parsing over regex | WooCommerce Zap keyed on AAPC number; orders → students link direction; active-tracker collapse; PDF parser moved off Replit into n8n; crews' PDFs parsed by AI into fixed JSON |
| 5 | PDF & Document Generation | Design around a frozen document | Generated PDF is static; map a rollup (ARRAYUNIQUE) not a lookup, names not record IDs; branch upstream; no dynamic line items, so parse deterministically; signature field instead of DocuSign | Manager-approval re-render loop; QuickBooks ID printed 3×; state agreements; DocuSign replaced in Client A |
| 6 | Interface & Access Design | Choose share modes and front ends on purpose | 50 pages/interface and 50 interfaces/base cap; public share vs read-only collaborator; one page filtered on the logged-in user; when interfaces stop being enough (Site, Canvas, custom Next.js); live availability = dashboard | 148 caseworkers (quoted as 133 two weeks earlier); HIPAA ended the public-page plan; premium print positions sellable once per issue |
| 7 | Project Management for Solo Consultants | Track the work itself; keep building while the client edits | Task as a record from a Template Tasks table; changelog = one record per status change; roles library + junction table only when needed; free native Airtable form triggers the cascade; co-owned base | Client B production stages (written, photographed, designed, laid out); five months of shared editing; a third of the tables built by the client |
| 8 | Client Communication | Communication as a design problem | "Client is always right" vs "the client's reason is a good one"; asked-for vs needed; defend a schema decision, then commit; bounded approval loop; honest debt conversation; matching the explanation to the need | Insertion Order table (preference, not constraint); "we sell positions, not products"; one-revision discount approval |

Appendices: A (build index), B (glossary), C (principles). Appendix C is a good source of on-screen pull quotes.

---

## Module 1: Schema Design in Airtable ⭐ prototype built (`module-01.mp4`)

**One line:** model the thing before you automate it. Every value has one level where it's actually true.

### Voiceover (Rachael records this herself; voice-align rewrite, 170 words, about 68 seconds; one paragraph per scene, in scene order)
1. On a magazine advertising build, I got three table decisions wrong. A contract total read zero. A QuickBooks customer ID printed three times on one contract. About fourteen thousand duplicate rows appeared.
2. None of those were automation bugs. They were decisions about my tables and links. I made them too early and had to take them back.
3. Every value has one level where it is actually true.
4. The line total belongs on the line item, with the quantity and unit cost. The contract adds up the line totals.
5. The QuickBooks customer ID belongs on the advertiser. QuickBooks assigns it to the customer, not each contact.
6. A value one level too high cannot be calculated. A value one level too low creates duplicates.
7. My second table matched the first, record for record. It held the duplicates. Nothing required it. So I deleted it.
8. Now I draw the whole model on one screen first. I mark where each value first has one answer. This is module one of Systems Thinking for Airtable.

### Scene list
| # | On-screen visual | Caption / on-screen text | Replace with real footage? |
|---|---|---|---|
| 1 | Dark cover; the title, then three symptom cards appear one by one | "Three table decisions I got wrong." · "Total = $0" · "QuickBooks ID ×3" · "~14,000 duplicate rows" | Slide |
| 2 | Cream slide: "Not automation bugs." + build context | "Schema decisions I made too early and had to take back." · "Magazine advertising · Airtable + Fillout + QuickBooks" | Slide (optional b-roll: scrolling a big table) |
| 3 | Big rule statement | "Every value has one level where it's actually true." | Slide |
| 4 | Diagram: Contract → Contract Line Item; `Line Total = Quantity × Per Unit Cost` on the line item; `Total = SUM(Line Total)` on the contract | "The calculation lives with the quantity." | **🎥 SCREEN REC:** in *Contract Line Item*, add formula field `Line Total` = `{Quantity} * {Per Unit Cost}`; then in *Contracts*, add rollup `Contract Total` = `SUM(values)` over Line Items |
| 5 | Diagram: Advertiser → Contacts; QuickBooks ID moves from Contact (×3, red) to Advertiser (✓) | "Store the key where the other system assigns it." | **🎥 SCREEN REC:** *Contacts* grid showing the same QB Customer ID on 3 rows → create the field on *Advertisers* and show one value |
| 6 | Three-row ladder: too high / right level / too low | "Too high → can't compute · Too low → duplicates" | Slide |
| 7 | Diagram: Contract → Line Item → ~~Insertion Order~~ | "No concrete reason to split → same table twice → deleted" | **🎥 SCREEN REC:** in a *copy* of the base, open *Insertion Orders* (fields are all lookups) → move the needed fields to the line item → delete backlinks → delete the table |
| 8 | Dark close: "Draw the model on one screen." + course title | "Systems Thinking for Airtable · Module 1 · airbnbai.rent" | Slide (or Rachael to camera) |

### LinkedIn caption
> Three table decisions I got wrong: a total that read zero, a customer ID printed three times on one contract, and about 14,000 duplicate rows.
>
> None of those were automation bugs. They were schema decisions I made too early, and had to take back, on a magazine advertising build in Airtable.
>
> The rule I use now: every value has one level where it's actually true. Too high and it can't compute. Too low and you get duplicates.
>
> I also learned to treat a one-to-one relationship as a question to answer out loud. Ours was a 14,000-row table of lookups. I deleted it.
>
> Module 1 of my course, Systems Thinking for Airtable: github.com/RachaelQuisel/systems-thinking-for-airtable
>
> Where does a value in your base live one level off?

---

## Module 2: Data Normalization

**One line:** match records on something real. Decide the unique key first and store identifiers as text.

### Voiceover (Rachael records this herself; voice-align rewrite, 170 words, about 68 seconds; one paragraph per scene, in scene order)
1. Every match between orders and students failed. Two missing zeros caused it.
2. On an education build, I matched WooCommerce orders to students by AAPC number. That eight-digit identifier can start with zeros.
3. It was stored in a number field. Number fields drop leading zeros. So <EXAMPLE_AAPC_NUMBER, read digit by digit> became six digits.
4. A formula fixed it. It counts the digits and adds zeros to the front until there are eight. I copied the results into a single line text field. The match now runs on that fixed text.
5. That build also split one data feed into two tables. Students has one record per person. Orders has one record per purchase. Each import updates the student and creates a new order.
6. Now I pick the unique key first. A unique key belongs to only one record. I confirm it is in the source file. I store identifiers as text from the first day. Number fields are for math.
7. This is module two of Systems Thinking for Airtable.

### Scene list
| # | Visual | Caption | Footage? |
|---|---|---|---|
| 1 | "<EXAMPLE_AAPC_NUMBER>" with the two zeros fading away to "<EXAMPLE_AAPC_NUMBER without its two leading zeros>" | "Every lookup missed. Because of two zeros." | Slide |
| 2 | Orders → Students match diagram on the AAPC number | "Matching orders to students by ID" | Slide |
| 3 | Field-type badge "Number" with the stripped value | "Number fields drop leading zeros" | **🎥 SCREEN REC:** *Students* table, `AAPC Number` field (type Number) showing 6-digit values; open the field config to show the type |
| 4 | Formula card: if length = 6 → "00" + value; 7 → "0" + value | "Pad it back. Then stamp it as text." | **🎥 SCREEN REC:** add formula field padding by `LEN()`; duplicate field → change type to Single line text; show an exact-match lookup now succeeding |
| 5 | One feed splitting into two tables: Students (upsert) / Orders (always create) | "Update the person. Create the event." | Optional 🎥: show *Students* and *Orders* tables linked |
| 6 | Two checklist items | "Choose the key first · Store IDs as text" | Slide |
| 7 | Close card | "Systems Thinking for Airtable · Module 2" | Slide |

### LinkedIn caption
> Every lookup was failing, and the reason was two zeros.
>
> An eight-digit ID like <EXAMPLE_AAPC_NUMBER> lived in a number field. Number fields drop leading zeros, so every exact match missed.
>
> The fix was a padding formula, then converting to single-line text and stamping the values. The lasting lesson was earlier in the process: decide the unique key before anything else, and confirm it's actually in the source file.
>
> I picked keys that weren't in the export more than once on that build. Now it's the first question I ask.
>
> Module 2 of Systems Thinking for Airtable (free on GitHub).

---

## Module 3: Workflow Building

**One line:** build the manual pipeline first. When the tool can't branch, move the decision upstream.

### Voiceover (Rachael records this herself; voice-align rewrite, 149 words, about 60 seconds; one paragraph per scene, in scene order)
1. My form tool could not make a decision. So I moved the decision to an earlier step.
2. On an education build, the enrollment agreement differs by state. There were versions for Florida, Indiana, South Carolina, Texas, and a headquarters default.
3. Fillout, the form tool, creates every PDF set up on a form at each submission. It cannot choose just one.
4. So I made one copy of the form per state. One Airtable formula field uses the SWITCH function to return the right form link for each student's state.
5. The email automation reads that one field. No other step checks the state.
6. I build each process by hand first and watch it work from start to finish. Then I automate the steps that repeat. I learn what each tool cannot do. Then I move that step to a tool that can.
7. This is module three of Systems Thinking for Airtable.

### Scene list
| # | Visual | Caption | Footage? |
|---|---|---|---|
| 1 | A fork icon labeled "the tool can't branch" | "Move the decision, not the tool" | Slide |
| 2 | Five state chips: FL · IN · SC · TX · HQ | "One agreement per state" | Slide |
| 3 | One form → five PDFs, all generated | "Fillout generates every mapped PDF" | Optional 🎥: Fillout PDF integrations list |
| 4 | Formula card: `SWITCH({State}, "Florida", url1, …)` | "Branch upstream with one formula field" | **🎥 SCREEN REC:** *Students* table → add formula field `Enrollment Form URL` with `SWITCH({State}, …)`; show the 5 duplicated forms in Fillout |
| 5 | Automation step referencing a single field | "One field. No duplicate logic." | **🎥 SCREEN REC:** Airtable automation "Send email" step inserting `{Enrollment Form URL}` |
| 6 | Three steps: by hand → watch it work → automate repeats | "Manual first. Then automate." | Slide |
| 7 | Close | "Systems Thinking for Airtable · Module 3" | Slide |

### LinkedIn caption
> My form tool couldn't make a decision, so I moved the decision.
>
> Fillout generates every mapped PDF on every submission. We needed a different enrollment agreement for each of five states.
>
> Instead of fighting the tool, I duplicated the form once per state and let one SWITCH formula in Airtable hand each student the right link. The send automation reads one field and holds no state logic.
>
> Honest note: I stacked Fillout workaround on workaround for months. Next time I'd settle whether it's the right entry point before building a single form.
>
> Module 3 of Systems Thinking for Airtable.

---

## Module 4: Automation Architecture

**One line:** search before you write, write links from the one-side, and keep the whole flow where you can debug it.

### Voiceover (Rachael records this herself; voice-align rewrite, 170 words, about 68 seconds; one paragraph per scene, in scene order)
1. One automation step can remove every order linked to a student.
2. I can fix a table mistake before it runs. An automation mistake reaches more records. It also reaches them faster.
3. On a WooCommerce to Airtable build, I first planned to create the order. Then I would point the student at it.
4. A link field connects records across tables. A student's link field holds a set of orders. Writing one order into it replaces the whole set.
5. Now the automation finds or creates the student by a unique key. Only one record has that key. Then it writes the student onto the order. An order has only one student. So nothing gets replaced.
6. That pattern held for all eleven months.
7. I ask four questions on every automation. Am I creating or updating? Am I sure? Which side holds one value? Did I filter before I sorted? If a step runs where I cannot see it, do I know why it failed?
8. This is module four of Systems Thinking for Airtable.

### Scene list
| # | Visual | Caption | Footage? |
|---|---|---|---|
| 1 | Student card with 3 orders → 1 after a bad write | "One write. Three orders gone." | Slide |
| 2 | Two icons: schema (still) vs automation (spreading) | "Automation mistakes travel" | Slide |
| 3 | Arrow from Student → Order (red ✕) | "Wrong direction" | Slide |
| 4 | Link field holding a set being replaced | "A link field write replaces the set" | Slide |
| 5 | Search → found / not found → create Order with Student link | "Write from the side that holds one value" | **🎥 SCREEN REC:** Airtable automation (or the Zap): *Find records* in Students by key → two branches → *Create record* in Orders with `Student` link set |
| 6 | "11 months" badge | "Held the whole time" | Slide |
| 7 | Four-question checklist | "Create or update? · Which side? · Filter then sort? · Can I see it?" | Slide |
| 8 | Close | "Systems Thinking for Airtable · Module 4" | Slide |

### LinkedIn caption
> One automation step can erase a customer's order history.
>
> My first plan on a WooCommerce-to-Airtable build was to create the order, then update the student to point at it. But a student's link field holds a set, and one write replaces all of it.
>
> So I write links from the side that holds one value. Find or create the student by a unique key, then write the student onto the order.
>
> It's one of the few patterns from that build that never needed changing.
>
> Module 4 of Systems Thinking for Airtable.

---

## Module 5: PDF & Document Generation

**One line:** a generated PDF is frozen, so design around the re-render and map rollups, not lookups.

### Voiceover (Rachael records this herself; voice-align rewrite, 155 words, about 62 seconds; one paragraph per scene, in scene order)
1. A contract PDF printed the same customer ID three times.
2. The document was not broken. It showed a shortcut I had taken in the tables.
3. The PDF read a lookup. A lookup pulls a value from each linked record. The advertiser had three linked contacts. So the lookup returned the ID three times.
4. The quick fix is a rollup that uses ARRAYUNIQUE. A rollup combines values from linked records. ARRAYUNIQUE keeps one copy of each value. I also send names to the PDF, not Airtable's internal record codes.
5. The real fix was in the tables. The QuickBooks customer ID belongs on the advertiser, not on each contact.
6. A generated PDF does not change after it is created. Changing the data in Airtable leaves the document the same. Someone has to submit the form again to get a new PDF.
7. So I plan for that second submission.
8. This is module five of Systems Thinking for Airtable.

### Scene list
| # | Visual | Caption | Footage? |
|---|---|---|---|
| 1 | Mock PDF with "QB ID: 123, 123, 123" | "Same ID. Three times." | Slide (or 🎥 the real generated PDF from a demo base) |
| 2 | Magnifier on the mapping | "The document shows your shortcuts" | Slide |
| 3 | Advertiser → 3 Contacts → 3 IDs | "Lookup across one-to-many" | Slide |
| 4 | Lookup vs `ARRAYUNIQUE(values)` rollup | "Map a rollup, not a lookup" | **🎥 SCREEN REC:** *Contracts* table: lookup field showing "123, 123, 123" next to a rollup `ARRAYUNIQUE(values)` showing "123"; then the Fillout PDF template field mapped to the rollup |
| 5 | QB ID moving to Advertiser | "Fix the level, not just the symptom" | Slide |
| 6 | PDF with a lock icon; Airtable value changes, PDF doesn't | "A generated PDF is frozen" | **🎥 SCREEN REC:** change a value in Airtable → show the existing PDF attachment unchanged → resubmit the form → new PDF appears |
| 7 | Loop arrow "re-render" | "Design for the re-render" | Slide |
| 8 | Close | "Systems Thinking for Airtable · Module 5" | Slide |

### LinkedIn caption
> A contract PDF printed the same customer ID three times.
>
> The document wasn't broken. It showed me a shortcut: a lookup across a one-to-many link. Three contacts, three IDs.
>
> A rollup with ARRAYUNIQUE fixes the symptom. Moving the ID to the advertiser, where QuickBooks actually assigns it, fixes the cause.
>
> The other lesson: a generated PDF is frozen. When data changes, someone has to resubmit to get a fresh document, so I design for the re-render.
>
> Module 5 of Systems Thinking for Airtable.

---

## Module 6: Interface & Access Design

**One line:** know the limits (50 pages, 50 interfaces), filter one page per logged-in user, and treat handoff as a real constraint.

### Voiceover (Rachael records this herself; voice-align rewrite, 167 words, about 67 seconds; one paragraph per scene, in scene order)
1. I needed one page for each of one hundred forty-eight caseworkers. Airtable does not allow that many.
2. An interface is a custom screen on top of an Airtable base. One interface can have up to fifty pages. One base can have up to fifty interfaces.
3. The built-in answer is one page with a filter. It shows records where the caseworker email matches the logged-in user's email. One page then works for every caseworker.
4. That filter needs each viewer to have a paid Airtable account.
5. A public page with a manual filter would expose other students' records. HIPAA, the United States health privacy law, ended that plan.
6. One filtered page works well for a small internal team. A large group without Airtable logins needs a portal outside Airtable.
7. The front end is the screen people use. A more capable front end is harder for the client to maintain after I leave. I treat that handoff as a real constraint.
8. This is module six of Systems Thinking for Airtable.

### Scene list
| # | Visual | Caption | Footage? |
|---|---|---|---|
| 1 | Grid of 148 tiny page icons, most greyed out | "148 caseworkers. 50 pages." | Slide |
| 2 | Limits card | "50 pages / interface · 50 interfaces / base" | Slide |
| 3 | One page, filter chip "Caseworker Email = current user" | "One page, filtered per user" | **🎥 SCREEN REC:** Interface designer → page → filter `Caseworker Email` *is* `Current user's email`; then "Preview as" two different users |
| 4 | Seat icon × N | "Each viewer needs a seat" | Slide |
| 5 | Public link with a leak icon; "HIPAA" badge | "Public share + manual filter leaks" | **🎥 SCREEN REC:** Share menu showing *Publish page publicly* vs *Invite as read-only* (demo base) |
| 6 | Small team ✓ / large unauthenticated group → portal | "Pick the pattern by audience size" | Slide |
| 7 | Slider: Interface → Site → Canvas → custom app; client ownership decreasing | "Weigh handoff" | Slide |
| 8 | Close | "Systems Thinking for Airtable · Module 6" | Slide |

### LinkedIn caption
> I needed a page for each of 148 caseworkers. Airtable caps interfaces at 50 pages.
>
> The native answer is one page filtered on the logged-in user, but each viewer needs a paid seat. A public page with a manual filter leaks, and with student records under HIPAA that wasn't an option.
>
> What I took from it: the front-end choice is a maintainability decision, not a taste decision. The more capable the front end, the less the client can keep running after I leave.
>
> Module 6 of Systems Thinking for Airtable.

---

## Module 7: Project Management for Solo Consultants

**One line:** a task is a record pulled from a template, and a changelog is one record per status change.

### Voiceover (Rachael records this herself; voice-align rewrite, 169 words, about 68 seconds; one paragraph per scene, in scene order)
1. A one-off task should not need a new field. If it does, the tasks are set up wrong.
2. On a magazine build, I first stored the production stages as status fields. The stages were written, photographed, designed, and laid out.
3. Then a one-off task came up. The only place to put it was a new field.
4. Now each task is its own record in a Tasks table. Each task links to its project. Each task has its own status, date, and owner.
5. A Template Tasks table holds the standard list. When someone creates a project, an automation goes through the template tasks. It creates one linked task for each one, set to Pending.
6. To see how long a task stayed in one stage, I create a new record at every status change. Those records are the history.
7. This full setup was more than one of my two clients needed. Now I build only what the client will actually ask about.
8. This is module seven of Systems Thinking for Airtable.

### Scene list
| # | Visual | Caption | Footage? |
|---|---|---|---|
| 1 | Grid with a new column squeezed in for one task | "One task shouldn't need a new field" | Slide |
| 2 | Four stage columns | "Stages as fields" | Slide |
| 3 | "+ new column" for a one-off | "Then a one-off shows up" | Slide |
| 4 | Projects → Tasks (rows) | "A task is a record" | **🎥 SCREEN REC:** *Tasks* table grid: linked Project, Status (Pending / In Progress / Complete), date, owner |
| 5 | Template Tasks → automation → Tasks | "Templates create the checklist" | **🎥 SCREEN REC:** automation "When record created" in *Projects* → *Find records* in *Template Tasks* → repeating group *Create record* in *Tasks*; then create Project D and show tasks appear |
| 6 | Timeline of status-change records | "One record per status change" | Optional 🎥: *Changelog* table |
| 7 | "Build less, faster" card | "Match the architecture to the client" | Slide |
| 8 | Close | "Systems Thinking for Airtable · Module 7" | Slide |

### LinkedIn caption
> If a one-off task forces you to add a new field, the tasks are modeled wrong.
>
> I used to model production stages as status fields. Now each task is a record, created from a Template Tasks table the moment a project is created, linked and pending.
>
> Honest note from the build: the full architecture was more than one of my two clients needed. I'd now ask which questions the client will actually ask before building the detailed version.
>
> Module 7 of Systems Thinking for Airtable.

---

## Module 8: Client Communication

**One line:** "the client is always right" and "the client's reason is a good one" are two different sentences.

### Voiceover (Rachael records this herself; voice-align rewrite, 169 words, about 68 seconds; one paragraph per scene, in scene order)
1. "The client is always right" and "the client's reason is a good one" are two different statements.
2. On a magazine build, every line item created exactly one insertion order. So the Insertion Order table had about fourteen thousand records. Those records held only lookup fields. A lookup field pulls a value from a linked record.
3. Staff gave one reason to keep that table. They did not want to see the words line item on screen.
4. That reason is a preference, not a constraint. Renaming a page costs nothing. An extra table has a cost. So I rename the interface page and hide the fields.
5. I defended keeping that table for two calls. Then I said it plainly. Every line item is already an insertion order.
6. Now I sort every reason on the first call. Each is a constraint or a preference. I sort out loud. Then the client can correct me. I also state the cost in plain numbers early.
7. This is module eight of Systems Thinking for Airtable.

### Scene list
| # | Visual | Caption | Footage? |
|---|---|---|---|
| 1 | Two sentences stacked, one highlighted | "Two different sentences" | Slide |
| 2 | Line Item ↔ Insertion Order 1:1, "~14,000 rows" | "A table of lookups" | Slide |
| 3 | Speech bubble: "don't show 'line item'" | "The stated reason" | Slide |
| 4 | Two piles: Constraint / Preference | "A page name is free. A table isn't." | **🎥 SCREEN REC:** Interface designer: rename page to "Insertion Orders" while it's backed by *Contract Line Items*; hide insertion-order fields in the layout |
| 5 | "2 calls" badge | "I defended it too long" | Slide or Rachael to camera |
| 6 | Checklist: sort out loud · say the cost early | "Sort on the first call" | Slide |
| 7 | Close | "Systems Thinking for Airtable · Module 8" | Slide |

### LinkedIn caption
> "The client is always right" and "the client's reason is a good one" are two different sentences.
>
> A client wanted to keep a separate 14,000-row table because staff didn't want to see the words "line item." That's a naming preference. A page name is free. A table isn't.
>
> I was on the wrong side of that for two calls. Now I sort every reason into constraint or preference on the first call, out loud, so the client can tell me if I sorted it wrong.
>
> Module 8 of Systems Thinking for Airtable.

---

## Screen-recording shot list (for planning)

Record in a sandbox base with dummy data. Suggested bases: **"Demo · Magazine Ads"** (Client B shape: Advertisers, Contacts, Contracts, Contract Line Items, Insertion Orders, Products + attribute libraries, Projects, Tasks, Template Tasks) and **"Demo · Course Enrollment"** (Client A shape: Students, Orders, Attendance, with fields State, AAPC Number, Caseworker Email). Vertical 1080×1920: zoom the browser to ~150% and record a tight region, or record at 16:9 and crop.

| Module | Base | Table / area | Action to record |
|---|---|---|---|
| 1 | Demo · Magazine Ads | Contract Line Items → Contracts | Add formula `Line Total = {Quantity} * {Per Unit Cost}`; add rollup `SUM(values)` on Contracts |
| 1 | Demo · Magazine Ads | Contacts → Advertisers | Show the same QB Customer ID on 3 contact rows; create `QuickBooks Customer ID` on Advertisers |
| 1 | Demo · Magazine Ads (copy) | Insertion Orders | Show lookup-only fields; move fields to the line item; delete backlinks; delete the table |
| 2 | Demo · Course Enrollment | Students | `AAPC Number` as Number (zeros gone) → padding formula by `LEN()` → duplicate → convert to Single line text → successful match |
| 2 | Demo · Course Enrollment | Students + Orders | Show two linked tables (optional) |
| 3 | Demo · Course Enrollment + Fillout | Students / Fillout dashboard | Formula `Enrollment Form URL = SWITCH({State}, …)`; show 5 duplicated Fillout forms |
| 3 | Demo · Course Enrollment | Automations | Send-email step inserting `{Enrollment Form URL}` |
| 4 | Demo · Course Enrollment | Automations (or Zapier) | Find Students by key → found/not-found branches → Create Order with Student link |
| 5 | Demo · Magazine Ads + Fillout | Contracts | Lookup "123, 123, 123" vs `ARRAYUNIQUE(values)` rollup; Fillout PDF field mapped to the rollup |
| 5 | Demo · Magazine Ads + Fillout | Contracts | Change data → PDF unchanged → resubmit → new PDF |
| 6 | Demo · Course Enrollment | Interface designer | Page filter `Caseworker Email` is current user; Preview as 2 users; Share menu public vs read-only |
| 7 | Demo · Magazine Ads | Projects / Tasks / Template Tasks / Automations | Tasks grid; "when record created" automation with repeating group; create Project D → tasks appear |
| 8 | Demo · Magazine Ads | Interface designer | Rename page to "Insertion Orders" over Contract Line Items; hide fields |
