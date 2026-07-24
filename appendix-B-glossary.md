# Appendix B — Glossary

My working vocabulary, in plain English. These are the words that carried the actual weight in the builds. Where Airtable has a precise meaning, I use it.

**Link record field** — a field that points a row in one table at one or more rows in another table. This is the connection at the center of every model in this course. A link works in both directions: Airtable creates the reverse field on the other side automatically, so when you delete a table you have to remove those reverse fields too, or you leave broken references behind.

**Lookup** — a field that pulls a value across a link. It is read-only and updates live. Convenient, but it can lag while it updates, and it copies whatever is on the other side. My rule: a lookup is for display, not for a value you need to be stable or unique.

**Rollup** — like a lookup, but it aggregates the linked values through a function (sum, max, a unique array, a concatenation). I used a rollup on the Advertiser table to produce a *unique* array of QuickBooks IDs for the PDF, because the plain lookup from Contacts gave duplicates. Rollup is the tool when you need one settled value out of many linked rows.

**Primary field formula** — the first field of a table, which Airtable shows as the record's name. If it's blank you get "Unnamed record", which breaks link pickers and interfaces. I set the primary field to a formula (e.g. day-of-week + form-submission) so every record has a readable, unique name. Making the primary field a **formula** also matters when you paste values into a link field: because a formula can't be written to, you can only *link* to existing rows, never accidentally *create* new ones.

**Junction table** — a table that sits between two others to record a many-to-many (or a per-instance) relationship. Insertion orders were supposed to be a junction between line items and something else; the lesson was that when a "junction" turns out to be one-to-one with the thing above it, it isn't a junction, it's a duplicate, and it should be deleted.

**One-to-one relationship** — when every row in table A has exactly one row in table B and vice versa. My heuristic: whenever I have a one-to-one relationship, I assume there is something there — meaning the two tables probably want to be one table, unless I have a concrete future reason (e.g. one line item might later spawn multiple insertion orders) for keeping them apart.

**Library** — my word for a small link-record table of allowed values (publications, ad sizes, ad positions, years). Not a single-select field — a *table* — because the values need to filter each other. A cascade of libraries is what lets a form ask for one attribute at a time and narrow the next dropdown.

**Cascade filter / conditional filter** — a filter on a form field that references the fields chosen above it, so each dropdown only shows options consistent with the earlier choices. The whole Client B product-selection form was a cascade: class → publication type → publication → issue year → ad size → ad type → ad position → frequency → issue month → special section → product.

**Product-as-filter (the dynamic-filter link field)** — instead of a form asking "which product?", the form asks for each attribute, then a product link-record field with a **dynamic filter** shows only the product whose attributes match everything chosen above. The attributes *are* the filter. This is safer than an automation guessing the product after the fact.

**Search-or-create (create-or-update)** — the automation pattern where you first *search* a table by a unique key, then *update* the row if found or *create* it if not. The Zapier zap for WooCommerce did this: search Orders by AAPC number, then update or add. The unique key is the part that matters most.

**Match key** — a value you build specifically so you can link two sets of records that don't otherwise share an ID. When 700 migrated line items had no contract link, the move was to build a formula field combining several fields into one unique string, make it the primary field on one side, and paste-to-link — so equal keys link and unequal keys stay unlinked (and nothing new gets created).

**Convert-lookup-to-static** — the migration step: to move a field's data from a linked table down onto the table itself, create a lookup of it, then change the field type from lookup to single-line-text (or single-select), which freezes the value in place. Then you can safely delete the link. It is a blunt move, but it works.

**Tasks as records (not fields)** — the project-management architecture: don't model a checklist as one checkbox field per step. Model each task as its own record in a Tasks table, pulled from a template, linked back to the thing it belongs to. That way you can add an ad-hoc task, automate it, and track time in status — none of which a one-field-per-task layout allows.

**Changelog as one-record-per-status-change** — to know how long something spent in each stage, you don't overwrite a status field; you write a new record every time the status changes. The history is the rows.

**Static PDF** — once a Fillout PDF integration generates a document on form submission, that PDF is frozen. If the data changes later, the old PDF still shows the old numbers until the form is re-submitted to regenerate it. This single fact drove a lot of the contract-total design (proposed vs resulting total, and the reprint button).

**Site / Canvas / custom code** — the fallback options when Fillout gets too limiting: Airtable's own "site" and Canvas features, or a fully custom frontend (Next.js, deployed to Vercel) with Airtable as the backend. Once the logic gets complicated, being able to write code is usually easier than working around a form builder.
