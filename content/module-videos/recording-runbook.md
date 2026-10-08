# Recording Runbook: Systems Thinking for Airtable module videos

Sandbox bases only, with dummy data. Both live in Rachael's own **Demos** workspace (`<DEMOS_WORKSPACE_ID>`). Built Wed Oct 7, 2026 (PT).

| Base | Base ID | URL |
|---|---|---|
| Demo · Magazine Ads | `<DEMO_BASE_ID_1>` | https://airtable.com/<DEMO_BASE_ID_1> |
| Demo · Course Enrollment | `<DEMO_BASE_ID_2>` | https://airtable.com/<DEMO_BASE_ID_2> |

**Before every session**
- Use a browser profile with no client bases open. Hide the left sidebar and any base list that shows client names.
- For 1080×1920 output, zoom the browser to about 150% and record a tight region, or record 16:9 and crop.
- Nothing in these bases is real. Names are "Sample Advertiser N", "Sample Contact N", "Student A–L"; emails are `@example.com`; AAPC numbers are patterns like 00111111.
- **Don't** turn on any automation that sends email. Don't use "Test step" on a send-email action unless the recipient is your own address.
- Fields marked **LIVE** below don't exist yet on purpose. You create them on camera.

**Recommended order:** Session 1 (Magazine Ads): M5 → M1 scenes 4–5 → M7 → M8 → M1 scene 7 (in a copy). Session 2 (Course Enrollment): M2 → M3 → M4 → M6. M4 depends on the text field M2 creates.

---

## Module 1: Schema Design in Airtable
**Base:** Demo · Magazine Ads, https://airtable.com/<DEMO_BASE_ID_1>

### Scene 4: line total on the line item, contract total as a rollup
- **Table:** Contract Line Items, https://airtable.com/<DEMO_BASE_ID_1>/<TABLE_ID>, then Contracts, https://airtable.com/<DEMO_BASE_ID_1>/<TABLE_ID>
- **Starting state:** Contract Line Items has Line Item, Product, Issue, Quantity, Per Unit Cost, Contract and Insertion Orders. There is no Line Total. Contracts has no total field.
- **On camera:**
  1. In Contract Line Items, add field **Line Total** (LIVE): Formula `{Quantity} * {Per Unit Cost}`. Format it as currency.
  2. Show the values. The first row, C-1001 · Full Page, shows 2 × $1,200 = $2,400.
  3. Open Contracts and add field **Contract Total** (LIVE): Rollup, link field `Contract Line Items`, field `Line Total`, aggregation `SUM(values)`.
  4. Show the totals: C-1001 = $3,400, C-1003 = $3,200, C-1006 = $2,900, C-1010 = $3,150.

### Scene 5: QuickBooks ID belongs on the advertiser
- **Table:** Contacts, https://airtable.com/<DEMO_BASE_ID_1>/<TABLE_ID>, then Advertisers, https://airtable.com/<DEMO_BASE_ID_1>/<TABLE_ID>
- **Starting state:** Contacts has a QB Customer ID field. Sample Contact 1, 2 and 3 all belong to Sample Advertiser 1 and all show `123`. Advertisers has no QuickBooks field of its own.
- **On camera:**
  1. In Contacts, group or sort by Advertiser so the three `123` rows sit together.
  2. Open Advertisers and add field **QuickBooks Customer ID** (LIVE, single line text).
  3. Type `123` on Sample Advertiser 1. One value, one place.
- **Don't** delete the QB Customer ID field on Contacts. Module 5 needs it.

### Scene 7: delete the one-to-one Insertion Orders table (in a copy)
- **Prep, off camera:** duplicate the base with records. Use the base name menu → Duplicate base and name it "Demo · Magazine Ads (copy)". The API can't do this. Record this scene only in the copy, because Module 8 needs the original's Insertion Orders link.
- **Table:** Insertion Orders (in the copy)
- **Starting state:** 14 insertion orders, IO-0001 to IO-0014, one per line item. Apart from the IO name and the link, every field is a lookup: Contract, Product, Issue, Quantity and Per Unit Cost (each "from Contract Line Item").
- **On camera:**
  1. Open Insertion Orders and open a few field configs to show they're lookups.
  2. Show that each IO links to exactly one line item.
  3. Move the needed fields to the line item. Every lookup already exists on Contract Line Items. If you want to keep the IO name, add **Insertion Order #** (single line text or autonumber) on Contract Line Items.
  4. In Contract Line Items, delete the **Insertion Orders** link field. That removes the backlink.
  5. Delete the **Insertion Orders** table.

---

## Module 2: Data Normalization
**Base:** Demo · Course Enrollment, https://airtable.com/<DEMO_BASE_ID_2>

### Scene 3: a number field drops leading zeros
- **Table:** Students, https://airtable.com/<DEMO_BASE_ID_2>/<TABLE_ID>
- **Starting state:** **AAPC Number** is a **Number** field (integer). Values show without zeros: 111111, 222222 … 999999. Student F shows 1234567, Student G shows 123 and Student H shows 12345678. The matching orders hold the full eight-digit text (00111111 and so on).
- **On camera:**
  1. Show the AAPC Number column.
  2. Open the field config to show the type is Number.
  3. Optional: open Orders and show WC-5001 with AAPC Number `00111111` (text).

### Scene 4: pad back to eight digits, then convert to text
- **Table:** Students
- **On camera:**
  1. Add field **AAPC Padded** (LIVE): Formula `REPT("0", 8 - LEN({AAPC Number} & "")) & {AAPC Number}`. This is the formula I suggest using.
     - The scene card shows the simpler length-6 / length-7 version: `IF(LEN({AAPC Number}&"")=6, "00"&{AAPC Number}, IF(LEN({AAPC Number}&"")=7, "0"&{AAPC Number}, {AAPC Number}&""))`.
     - That version doesn't pad Student G (123). Use the REPT version if Student G is in frame.
  2. Duplicate AAPC Padded and change the copy's type to **Single line text**. Name it **AAPC Number (Text)** (LIVE).
  3. Show the exact match. Search the Students grid (Ctrl/Cmd+F) for `00111111`. It now finds Student A in AAPC Number (Text). Before step 2 that search found nothing, because the number field stores 111111.

### Optional: one feed, two tables
- **Table:** Students and Orders, https://airtable.com/<DEMO_BASE_ID_2>/<TABLE_ID>
- **Starting state:** 14 orders, WC-5001 to WC-5014, each linked to one student. Student A has two orders (WC-5001, WC-5007), and so does Student D (WC-5004, WC-5013).
- **On camera:** Expand Student A to show one person with two order records.

---

## Module 3: Workflow Building
**Base:** Demo · Course Enrollment

### Scene 4: one SWITCH formula picks the form
- **Table:** Students
- **Starting state:** State has Florida, Indiana, South Carolina, Texas, Georgia and Ohio. Georgia and Ohio fall to the headquarters default. There is no Enrollment Form URL field yet.
- **Prep, off camera (outside Airtable):** in a sandbox Fillout account, duplicate one enrollment form five times: Florida, Indiana, South Carolina, Texas and HQ default. I couldn't create these. Fillout isn't connected.
- **On camera:**
  1. Add field **Enrollment Form URL** (LIVE): Formula
     ```
     SWITCH({State},
       "Florida", "<Fillout FL form URL>",
       "Indiana", "<Fillout IN form URL>",
       "South Carolina", "<Fillout SC form URL>",
       "Texas", "<Fillout TX form URL>",
       "<Fillout HQ default form URL>")
     ```
  2. Show a Georgia or Ohio student getting the HQ link.
  3. Cut to the Fillout dashboard showing the five forms.

### Scene 5: the email step reads one field
- **Area:** Automations, in Demo · Course Enrollment
- **On camera:**
  1. Create an automation (LIVE). Any trigger works for the shot, for example "When record created" in Students.
  2. Add the action **Send email**: To = `{Email}`, and in the body insert `{Enrollment Form URL}`.
  3. Show the config only. **Don't** turn it on or test it to the example.com addresses.

---

## Module 4: Automation Architecture
**Base:** Demo · Course Enrollment
- **Area:** Automations
- **Starting state:** Orders link to Students through **Student**. Each order has one student. AAPC Number (Text) on Students must already exist from Module 2.
- **On camera (LIVE automation):**
  1. Trigger: "When webhook received". Send one sample payload such as `{"order":"WC-5015","aapc_number":"00111111","product":"Sample Course A"}`, or pick any trigger that supplies an AAPC value.
  2. Action **Find records** in Students where `AAPC Number (Text)` is the trigger's `aapc_number`.
  3. Add conditional groups:
     - **Found** (records found > 0): **Create record** in Orders with Order, AAPC Number, Product, and **Student** = the found record's ID.
     - **Not found:** **Create record** in Students (Student, AAPC Number (Text)), then **Create record** in Orders with **Student** = the new student's ID.
  4. Point at the Student field on the new order. The link is written from the order side, so the student's other orders stay.
- Turn the automation off after recording.

---

## Module 5: PDF & Document Generation
**Base:** Demo · Magazine Ads

### Scene 4: lookup vs ARRAYUNIQUE rollup
- **Table:** Contracts, https://airtable.com/<DEMO_BASE_ID_1>/<TABLE_ID>
- **Starting state:** **QB Customer ID (lookup)** looks through Advertiser to Advertisers' "QB Customer ID (from Contacts)". C-1001 and C-1002 (Sample Advertiser 1) show `123, 123, 123`. C-1003 and C-1010 show `124, 124`. I verified this through the API.
- **On camera:**
  1. Show the lookup column.
  2. Add field **QB Customer ID (unique)** (LIVE): Rollup, link field `Advertiser`, field `QB Customer ID (from Contacts)`, aggregation `ARRAYUNIQUE(values)`. It should show `123`.
     - I didn't test whether a rollup over a lookup flattens here. If it doesn't, create the ARRAYUNIQUE rollup on Advertisers (over Contacts → QB Customer ID) and look that up from Contracts.
  3. Cut to the Fillout PDF template with the customer ID field mapped to the rollup.
- **Prep, off camera (outside Airtable):** a sandbox Fillout form that writes a PDF to **Contract PDF** on Contracts. I couldn't create it.

### Scene 6: a generated PDF doesn't update
- **Table:** Contracts
- **Starting state:** Contract PDF is empty. Submit the Fillout form once off camera, so one contract (for example C-1001) has a PDF.
- **On camera:**
  1. Change a value on C-1001, for example a line item's Quantity.
  2. Open the existing PDF. It's unchanged.
  3. Resubmit the form. A new PDF appears in Contract PDF.

---

## Module 6: Interface & Access Design
**Base:** Demo · Course Enrollment
- **Area:** Interface designer
- **Starting state:** Students has **Caseworker Email**, with caseworker1, 2 and 3 @example.com spread across the 12 students. There are no interfaces yet.
- **Prep, off camera:**
  - "Preview as" only lists real base collaborators. Before recording, set Caseworker Email on a few rows to your own Airtable login email and on a few others to a second collaborator's email. Set them back afterward.
  - I didn't change these values. They need real accounts.
- **On camera (LIVE):**
  1. Create an interface ("Caseworker Portal") with a list or grid page over Students.
  2. Add the page filter: `Caseworker Email` is **current user's email**. Check that option appears for an email field in the current Airtable UI before recording.
  3. Use "Preview as" for the two collaborators. Each sees only their own students.
  4. Open the Share menu and show **Publish page publicly** next to **Invite as read-only**. **Don't** publish.

---

## Module 7: Project Management for Solo Consultants
**Base:** Demo · Magazine Ads

### Scene 4: a task is a record
- **Table:** Tasks, https://airtable.com/<DEMO_BASE_ID_1>/<TABLE_ID>
- **Starting state:**
  - 12 tasks across Project A, B and C. Each has a Project link, Status (Pending / In Progress / Complete), Due Date and Owner (Team Member A/B/C).
  - Template Tasks has 8 rows: Assign writer, Write article, Edit copy, Photograph, Design pages, Lay out issue, Proofread, Send to print. Each has an Order, a Default Owner and Days Before Due.
- **On camera:** Show the Tasks grid, optionally grouped by Project.

### Scene 5: templates create the checklist
- **Area:** Automations
- **On camera (LIVE automation):**
  1. Trigger: "When record created" in **Projects**.
  2. Action **Find records** in **Template Tasks** (all records).
  3. **Repeat for each** found record → **Create record** in **Tasks** with:
     - Task = Template Task
     - Project = the trigger record ID
     - Status = Pending
     - Owner = Default Owner
  4. Turn the automation on. Create **Project D** in Projects, then show 8 tasks appear in Tasks, all Pending.
- **Retakes:** delete Project D and its 8 tasks. Turn the automation off when done.

---

## Module 8: Client Communication
**Base:** Demo · Magazine Ads (the original, not the copy)
- **Area:** Interface designer
- **Starting state:** Contract Line Items still has the **Insertion Orders** link field, and the Insertion Orders table exists. There are no interfaces yet.
- **On camera (LIVE):**
  1. Create an interface page over **Contract Line Items**.
  2. Rename the page **Insertion Orders**.
  3. In the page layout, hide the insertion-order fields (the Insertion Orders link).

---

## What the recordings create or change (left out on purpose)
| Module | Live change | Base |
|---|---|---|
| 1 | Line Total formula; Contract Total rollup; QuickBooks Customer ID on Advertisers; delete Insertion Orders (in the copy) | Magazine Ads |
| 2 | AAPC Padded formula; AAPC Number (Text) | Course Enrollment |
| 3 | Enrollment Form URL formula; send-email automation | Course Enrollment |
| 4 | Find-or-create automation | Course Enrollment |
| 5 | ARRAYUNIQUE rollup; Fillout PDF mapping; PDF regeneration | Magazine Ads |
| 6 | Caseworker interface, page filter, share menu | Course Enrollment |
| 7 | Template-tasks automation; Project D | Magazine Ads |
| 8 | Interface page renamed "Insertion Orders" | Magazine Ads |

To reset for retakes, delete the LIVE fields and records listed above. Don't delete the starting fields.
