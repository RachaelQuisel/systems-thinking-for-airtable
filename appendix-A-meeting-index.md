# Appendix A — Build Index

The sessions this course is drawn from, in order. **Build** is which system I was in: **Client A** (medical-coding education platform) or **Client B** (magazine advertising).

| # | Date | Build | What I worked on |
|---|---|---|---|
| 1 | 2025-07-29 | Client A | First WooCommerce export: should it land in Students or Orders? Split the feed, link by a unique ID, decide which table each field belongs to. |
| 2 | 2025-07-30 | Client A | Built the first Zapier zap: WooCommerce order to search Orders by AAPC number to create-or-update. The "why search Orders, not Students" edge case. |
| 3 | 2025-07-31 | Client A | Deduplicated students by hand, linked trackers to product purchases, worked through tracker end-conditions and active-order rollups. (2h46m, the long one.) |
| 4 | 2025-08-12 | Client A | ERD review, attachment mapping per tracker, the form-submission to generated-document to automation-trigger chain. |
| 5 | 2025-08-19 | Client A | Full tracker lifecycle (course to Practicode to internship to HCC exam to graduate), primary-field formulas to get rid of "unnamed record", retiring the active-order field. (2h15m.) |
| 6 | 2025-08-26 | Client A | State-conditional enrollment forms (Fillout generates every mapped PDF on submit, so you can't branch), duplicating the form per state, Tracker 3 simplification, HCC exam scoring. |
| 7 | 2025-08-28 | Client A | HCC exam integration, the 148-caseworker interface-limit problem, Texas multi-attachment handling, tracker cleanup. |
| 8 | 2025-09-18 | Client A | Moving PDF parsing off Replit into native n8n. |
| 9 | 2025-09-23 | Client A | Blackboard CSV to Airtable: match-and-update by email so no duplicates; a dynamic, parameter-driven reporting system for case managers. |
| 10 | 2025-10-03 | Client A | n8n workflow refinement; Airtable interface sharing (public page vs read-only base, button fields); the comma-vs-period currency bug. |
| 11 | 2025-10-14 | Client A | n8n dynamically creating Monday.com boards/groups from a parsed PDF; a lookup field for the Practicode end date so students can't edit it. |
| 12 | 2025-11-25 | Client A | CSV email-import config (update vs replace, unique identifier); the project-management architecture: tasks as records from a template, changelog as one-record-per-status-change. |
| 13 | 2026-02-12 | Client B | New build. Products are a set of attributes, not a single dropdown; libraries (link tables) for cascading selection; a product link field with a dynamic filter matching the attributes chosen above it; CSV dashes break currency fields. |
| 14 | 2026-03-17 | Client B | Working notes on the invoice to line item to insertion order three-layer model. |
| 15 | 2026-04-14 | Client B | The three-layer contract/line-item/insertion-order model spelled out; sequential month/section selection; the junction-table role of insertion orders. |
| 16 | 2026-04-30 | Client B | Connecting the year library as a link (not a dropdown) so it filters; where a field belongs as a library vs a single select. |
| 17 | 2026-05-08 | Client B | Collapsing to Contract to Product-at-line-item (dropping the insertion-order form); Line Total = Quantity × Per Unit Cost on the child; a rollup (not lookup) for a unique QuickBooks-ID array on the PDF; the "No Contract" backfill via a formula match-key; converting migration-only links to text. |
| 18 | 2026-05-14 | Client B | The issue-slots inventory model (one record per position per issue, filter out sold), selling positions not products, and the long back-and-forth over ad-size vs ad-page vs ad-position. (2h27m.) |
| 19 | 2026-05-22 | Client B | Deleting the Insertion Order table once it proved one-to-one with line items; migrating its fields down via lookups-converted-to-text; a formula match-key to link the strays. |
| 20 | 2026-06-08 | Client B | Proposed vs resulting contract total; the manager-approval one-revision workflow; update-form vs create-form; the 700-orphan-line-items backfill; the case for custom-coded frontends over Fillout as complexity grows. |

*The full recordings and transcripts of these sessions are held privately as the raw source material for this course.*
