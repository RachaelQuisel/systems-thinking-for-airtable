# Systems Thinking for Airtable

### A Masterclass by Rachael Quisel

*Built from eleven months of production builds, July 2025 – June 2026*

---

## Why this exists

For eleven months I built two production systems end to end. The first was a medical-coding education platform (Client A) running on WooCommerce, Airtable, Fillout, and Zapier, tracking students, orders, and progress. The second was a magazine advertising operation (Client B) running on Airtable and QuickBooks, tracking advertisers, contracts, line items, insertion orders, inventory, and billing.

This course is what I pulled out of that work. The patterns that stayed true across both systems. The decisions I got right. The ones I reversed. And the handful of ideas that changed how I build.

It is written in first person because it is my record of how I think about building on Airtable. Every lesson names the real field, table, and tool. If a lesson is about a rollup, it says rollup and names the table it lives on. That is the only level of detail where these lessons transfer to your own work.

## Who this is for

Anyone building operational systems on Airtable for real clients with messy data and strong opinions. That includes Airtable on its own, or Airtable plus forms plus automation plus accounting. If you have ever shipped something that worked in the demo and broke the moment the client touched it, this is for you.

## How the course is built

Eight modules. Each one opens with a short frame on why the topic matters in the actual work, and what you should have read first. Then a set of lessons. Each lesson has four parts:

1. The pattern in one sentence.
2. A case study from a real build, with the actual field, table, and tool names, the problem, and the fix.
3. What the pattern generalizes to.
4. Where it later broke or got replaced, when that happened.

Each module closes with **"What I'd do differently now"** and two or three exercises that make you try the pattern on your own base.

## The eight modules

1. **Schema Design in Airtable** — model the thing before you automate it. The Contract to Line Item structure, when a junction table earns its place and when it's a one-to-one you should delete, why a total belongs on the child record, and how to build product selection out of attributes that filter each other.
2. **Data Normalization** — split students from orders, match CSV imports by a real unique key, remove duplicates, and link rows of migrated data to their parents with a formula match-key instead of guesswork.
3. **Workflow Building** — build the pipeline by hand first, then automate the parts worth automating. Fillout parent and child forms, routing by state, WooCommerce to Airtable to Fillout to QuickBooks, and the difference between an update form and a create form.
4. **Automation Architecture** — Zapier versus n8n versus Airtable's own automations, search first then create-or-update, writing the link from the one-side, and the rule that you never create anything you didn't mean to create.
5. **PDF & Document Generation** — a generated PDF is frozen, and what that forces you to design around. Mapping to a rollup and not a lookup, and replacing DocuSign with signature fields.
6. **Interface & Access Design** — a public share versus a read-only base, one page filtered per user, the caseworker page limit, and when Airtable interfaces stop being enough.
7. **Project Management for Solo Consultants** — how to track the work itself (template tasks as records, a changelog as one record per status change), and how to run a build when the client is editing the base underneath you.
8. **Client Communication** — separating what the client asked for from what they need, defending a schema decision and then committing to it, saying no gracefully, and the difference between "the client is always right" and "the client's reason is a good one."

## The order to read it in

- **1 and 2 are the foundation.** You can't normalize what you haven't modeled, so schema comes before normalization.
- **3 and 4 are execution.** Build the pipeline by hand first, then automate the parts that repeat. Workflow comes before automation.
- **5 depends on 1, 2, and 3.** PDF templates read rollups, and those only make sense once the model is settled.
- **6 depends on 1 and 2.** Interface fields point back into the schema.
- **7 and 8 sit above the technical work.** You can read them after 1 through 6 in either order, but project management comes first here, because the cadence produces the artifacts the client actually sees.

## Appendices

- **A — Build index**: the sessions this is drawn from, each with a one-line summary.
- **B — Glossary**: the working vocabulary (rollup, lookup, primary-field formula, cascade filter, junction table, search-or-create, template task) in plain English.
- **C — Principles worth keeping**: the lines that carry the most weight.
