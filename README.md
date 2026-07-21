# Systems Thinking for Airtable

### A Masterclass by Rachael Quisel

*Built from eleven months of production builds, July 2025 – June 2026*

Start with the syllabus, then read the modules in order. Every lesson names the real field, table, and tool, and says where the pattern later broke. Read it front to back the first time. The later modules assume you have read the earlier ones.

## Contents

- **[00 — Syllabus](00-syllabus.md)** — why this exists, who it's for, how it's built, and the order to read it in.

### The eight modules

1. **[Schema Design in Airtable](01-schema-design.md)** — model the thing before you automate it: the Contract to Line Item structure, when a one-to-one table should be deleted, storing each value at the right level, and modeling a product as a set of attributes.
2. **[Data Normalization](02-data-normalization.md)** — split students from orders, match imports by a real unique key, rebuild a broken key, and link stray rows with a formula match-key instead of guesswork.
3. **[Workflow Building](03-workflow-building.md)** — Fillout parent and child forms, moving a decision earlier in the flow when the tool can't branch, the attribute cascade, turning one submission into many records, and update forms versus create forms.
4. **[Automation Architecture](04-automation-architecture.md)** — search first then create-or-update on a unique key, writing the link from the one-side, filter before you sort, keeping the flow in one place you can debug, and letting AI parse messy input instead of regex.
5. **[PDF & Document Generation](05-pdf-docs.md)** — a generated PDF is frozen and what that forces you to design around, mapping to a rollup and not a lookup, and why Fillout can't choose between outputs.
6. **[Interface & Access Design](06-interface-access.md)** — the caseworker page limit, a public share versus a read-only base, one page filtered per user, and when interfaces stop being enough.
7. **[Project Management for Solo Consultants](07-project-management.md)** — tasks as records and not fields, a changelog as one record per status change, and running a build while the client edits the base underneath you.
8. **[Client Communication](08-client-communication.md)** — "the client is always right" versus "the client's reason is a good one," defending a schema decision and then committing, the approval workflow as communication design, and saying the cost out loud.

### Appendices

- **[A — Build Index](appendix-A-meeting-index.md)** — the sessions this is drawn from, one line each.
- **[B — Glossary](appendix-B-glossary.md)** — the working vocabulary in plain English.
- **[C — Principles Worth Keeping](appendix-C-principles.md)** — the lines that carry the most weight.

## A note on honesty

This is a working notebook, not a polished success story. Every module includes at least one place where a decision I made turned out wrong, where an approach I built later got replaced, or where the thing I did first was the thing I should have kept. The point is to teach the reversals, not just the finished patterns.
