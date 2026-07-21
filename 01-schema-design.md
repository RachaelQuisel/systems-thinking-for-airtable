# Module 1 — Schema Design in Airtable

*Systems Thinking for Airtable · Rachael Quisel*

---

## Frame

Every system I build starts as tables and links before it is ever an automation, a form, or a PDF. That order is deliberate. On the AY Media build, a magazine advertising operation running on Airtable, Fillout, and QuickBooks, a wrong table shape cost me weeks. A total read zero because it was connected to the wrong record. A QuickBooks ID printed three times on a contract because it sat one level too low. 14,000 duplicate rows appeared because I had modeled a relationship that did not need its own table. None of those were automation bugs. They were schema decisions I made too early and then had to take back.

Schema design is where the build either works or slowly breaks. Every form field, every rollup (a field that adds up or combines values from linked records), every PDF mapping points back to the tables underneath. Get the tables right and the rest is just connecting them. Get them wrong and you fix the same defect at four different layers for a month.

This module is the set of table-shape decisions I got wrong, reconsidered, and eventually settled. I tell each one with the real fields and tables so you can see exactly where it lands.

## Prerequisites

None. This is the foundation of the course. You need an Airtable base you can experiment in and a willingness to delete a table you spent time building.

---

## Lesson 1 — When two tables are always one-to-one, delete one of them.

**Case study — AY Media, 2026-05-22 and 2026-06-08.** I had three levels in the base: Contract, Contract Line Item, and Insertion Order. The Insertion Order table held one row for every line item, and every line item produced exactly one insertion order. That meant roughly 14,000 insertion order rows that carried nothing but lookup fields (fields that pull a value from a linked record) pointing back at their line item. The table doubled in size and told me nothing new.

Whenever I have a one-to-one relationship, I tend to think there is something there. That is my own first check on a schema. It fires on the shape before I even read the field list. A separate Insertion Order table is not a bad idea by itself. If the client will ever generate more than one insertion order per line item, say a piece handled by designer A and a piece handled by designer B, then the separate table earns its place and you want it. But if that split is not real, one row in and one row out, the second table is a duplicate of the first.

The two reasons I had kept the table were: a handful of products get a line item but never an insertion order, and the staff did not want to read the words "line item" on their screen. Neither holds. The first is solved by leaving the insertion-order fields empty on those line items. The second is solved by renaming an interface page, which costs nothing. You can call an interface page whatever you want while the backend stays the same table. You can hide the insertion-order fields on the line-item level so no one reads them. So neither the display wording nor the occasional missing insertion order is a reason to carry a duplicate table.

**Principle.** A relationship that is one-to-one now, and that you have no concrete future reason to split, is the same table twice. The test is not "could these ever diverge in theory." The test is "is there a real, named reason a single line item will produce more than one insertion order," like the designer-A-and-designer-B split. If the answer is no, combine the two into one table. The backend name and the label the user reads are separate decisions. You rename a page for free, and you hide fields for free, so neither is a reason to carry a duplicate table.

**A call I reconsidered.** I defended keeping the Insertion Order table for a while, on the grounds that the client did not want to call it or see it written as a line item. I was on the wrong side of that for two calls. The point I kept pressing, hide the fields and rename the page, is the right practice, and I wanted to be sure we were following it before we walked away from it. But once a client wants a thing as a separate table, the practice argument stops mattering. A stated client wish outranks the tidy-schema position. The moment I said the quiet part myself, that it makes no sense to have an insertion order table when every line item is an insertion order, the decision was easy. I stopped defending the table and deleted it.

I keep one caution attached to that call, because it is worth carrying as its own small lesson about how sure to be. We could have been missing something, either in the current context or on the future roadmap. Combining a one-to-one is the right default, but I make the call knowing a future requirement could reopen it, and I say so out loud rather than pretending the decision is permanent.

One more step before the delete, which is easy to skip and expensive to skip. An Insertion Order table is not a standalone object. Several other tables link to it. Deleting it without care leaves broken references behind. Before you delete a table like this, delete the backlinks as well and confirm there are no dependencies that will break.

The model went from Contract → Contract Line Item → Insertion Order to Contract → Contract Line Item, with the insertion-order-only fields moved onto the line item first. That migration method is in Module 2. My earlier defense of the separate table was the thing I overturned.

---

## Lesson 2 — Store each value at the level where it is actually true.

**Case study — AY Media, 2026-05-08 and 2026-06-08.** Three separate values in this base were sitting at the wrong level, and each caused its own visible symptom.

First, the contract total was reading zero. The multiply that produces a line amount had been placed at the Contract level, above the quantity it needed. The calculation belongs on the Contract Line Item, where Quantity and Per Unit Cost both live, and the Contract sums those up. I do the calculation at the line-item level and give it a name that carries the rule. I call it line total, not order total, because the value applies to the line itself, not to the order. Quantity is the initial value, and I multiply it by Per Unit Cost, which is found within the product. The parent only rolls those lines up.

Second, the QuickBooks Customer ID. It was stored on the Contact table, so a single contract PDF printed the ID three times, once per contact linked to that advertiser. The root cause was not the PDF. The ID lived one level too low. QuickBooks assigns one ID to a customer, not to the individual contacts inside that customer, and in this base the customer is the Advertiser. So the field belongs on the Advertiser. There is a rollup-with-ARRAYUNIQUE workaround for the triple-print symptom, covered in Module 2, but the correct fix is the placement, not the workaround.

Third, the contact itself. Migrated data had contacts linked at the Contract Line Item level, one per line item, which double-counts the relationship and puts it at the wrong level. You cannot have line items without a contract, and a contact is a party to the agreement, so a contact belongs at the contract level, not the contract line item level. Linking a contact per line item, rather than a contact per contract, is the migration importing a relationship at a finer level than the relationship actually has.

**Principle.** Every value has one level where it is uniquely and natively true. The calculation lives with the quantity it multiplies, which is the child line, and the parent sums. An external system's key lives at the level that system assigns it, which is the customer, not the customer's contacts. A party to an agreement lives on the agreement, which is the contract, not on each line inside it. When you store a value one level too high, you cannot compute it, which is the total that read zero. When you store it one level too low, you get duplicates, which are the tripled QuickBooks ID and the per-line contact. The symptom shows up downstream at the form or the PDF, but the correction is always in the schema: move the field to the level where the value is singular.

---

## Lesson 3 — Build on the Contract → Line Item structure, and put each attribute at the level where it is first uniquely known.

**Case study — AY Media, 2026-04-14 and 2026-02-12.** Before any of the later combining happened, I settled the core shape of the base. A contract has line items. Each line item has a frequency (1x, 4x, and so on). The frequency spawns that many dated placements. Three layers: invoice, invoice line item, and then insertion order, where the insertion orders are spawned from the frequency, the 3x or whatever, creating that many records.

The three-level structure is the part everything else depends on. It has to be right first. You add the individual fields afterward. Each additional field is a must-have or a nice-to-have, but the database architecture, the schema itself, is the thing that has to work. Get the structure settled, then add the fields.

Then comes the rule that decides where a field goes. Take the Product field: should it sit on the insertion order? The answer keys on the Special Section attribute, which is only chosen at the insertion-order level. If the product includes section, you need it at the insertion order level, because section is only resolved there. A lookup of section from higher up, at the contract line item or the contract, returns multiple sections, and that array is not enough to select the exact combination at the more granular level. Because the product cannot be resolved without the section, and the section is only singular at that bottom level, the product has to live there too.

**Principle.** An attribute lives at the level where its inputs first become single-valued. If you try to place a field higher than that, a lookup from above returns an array of possible values, and an array cannot drive a unique selection. Section is chosen at the placement, so section, and anything that depends on section, like the exact product, belongs on the placement. This is the same rule as Lesson 2 read from the other direction. Lesson 2 says do not store a value where it duplicates or vanishes. This lesson says the correct level is the most granular one where the value resolves to exactly one.

**Where the levels changed.** The number of layers is a choice, not a given, and it moved during the build. My test for whether the middle table earns its place is whether I need line-item reporting or line-item rules. The middle layer earns its keep when you need to do reporting per line item, or enforce certain rules per line item. Go straight from contract to insertion orders and you would have to carry the frequency inside the insertion order, and then you get four records, 4x, 4x, 4x, 4x, with no line-item layer to report or rule on.

That test is exactly why Lesson 1 could later delete the Insertion Order table. Once every line item mapped to exactly one insertion order, the bottom layer stopped earning its keep, and the middle layer, Contract Line Item, was the one doing the real reporting and rule work. Between the February and April builds, Month and Special Section also moved down from the line-item level to the insertion-order level, and that forced me to re-map the Fillout form. The core structure was stable. The exact level of individual attributes was not, and every move cost re-mapping.

---

## Lesson 4 — Model a product as a set of attributes that filter each other, not as one product dropdown.

**Case study — AY Media, 2026-02-12 through 2026-05-14.** The client refused to let their account executives pick from a flat product dropdown. New products appear every couple of weeks, and a product here is really a combination: publication, ad size, ad type, ad position, frequency, special section, issue month, issue year. My model is to ask for each attribute in sequence and let a dynamic filter resolve the single matching product at the end. Collect all the attributes, then give the product a link-record field (a field that links to records in another table) whose dynamic filter says: only show the product records whose conditions match everything chosen above. The attributes above become the filter.

For the attributes to filter each other, each one has to be a table of allowed values, not a single-select field (a field that stores one choice from a fixed list). I call these tables libraries. I want the cascade logic, where each choice narrows the next, living in the data model, not buried in Fillout configuration where it is fragile and hard to debug. You could avoid the libraries and set the logic in Fillout instead, but I would rather have the logic in Airtable, at least in Airtable and maybe in both. Either way, go with the libraries.

**Principle.** When the thing you sell is defined by the intersection of several attributes, and those attributes change often, do not model the product as one dropdown you have to hand-maintain. Model each attribute as its own link table, and let a dynamic filter on the product field show only the record whose attributes match everything chosen above it. The attributes are the filter. Adding a new product becomes adding a new row that already sits in the right attribute combination, instead of extending a hand-kept list.

**An approach I moved away from.** This is the lesson where my first instinct was right, I let it go for about ninety minutes while I built the wrong thing, and then it came back around. On 2026-05-14 I built the issue-slot inventory keyed on product. I could not make it work, because inventory is not sold per product. It is sold per position: front cover, page four. Within a bought position, the client picks whatever product they want. The issue slot should not be per product but per position. We are selling positions, and within a position the client chooses whatever product they want, which is where I had started before I talked myself out of it.

The other piece I held the line on: I had considered dropping the separate ad-size selector on the theory that if ad size lived on the slot it was redundant. It is not redundant, because ad size is not one-to-one with a slot. It needs to be filtered. What is one-to-one with an issue slot is the issue year, the issue month, and the ad position. Those three, and only those three, are one-to-one for issue slots. Size is not, so it stays a filtered choice.

The inventory cost of getting this wrong is the part worth carrying forward. If you build a multi-valued attribute into the parent record, you stop being able to count inventory. Ad position is one-to-one with the slot, so it can live on the slot. If ad size were forced onto the slot too, you would end up with issue slot X size 1, issue slot X size 2, issue slot X size 3, each a unique record, because you have to track inventory for each of those separately, and now your slot count is wrong.

So the rule that came out of the reversal is narrower than "attributes filter each other." It is this: build an attribute into the parent record only when it is genuinely one-to-one with that record (issue year, issue month, ad position). Everything with multiple valid options (ad size, ad type) stays a filtered choice, or you under-count. And the meta-lesson I attached, after swinging between per-product and per-position twice, is to stop and confirm the assumption everything else depends on with the client before building on it again. Double-check with the client whether the understanding is correct before going all the way through the build, so you do not get to the end and find out inventory goes per product after all, not per ad position.

---

## Lesson 5 — Use one attachment field plus a record-level type, not one field per document type.

**Case study — Coding Clarified, 2025-08-19.** On the earlier build, a medical-coding education platform, I had done exactly the thing this lesson warns against. I had built separate fields on the form-submissions table: one called "attachment internship," one called "attachment practicode." Every new document type would have meant another parallel column and another mapping to maintain. The fix is to combine it into a single attachment field, with each record carrying its own type. Do not have one attachment field per attachment type. Have one attachment field, and let records carry their own types.

The reason is about what happens downstream. One attachment field can be filtered by type wherever you need it. Parallel fields force you to know, at every read site, which of several columns to look in. If you can still make reference to only one unique attachment field, that is the one to use, because when you need to look it up on a different table you can apply a condition like show me this if type is internship.

**Principle.** When several things differ only by a category, do not encode the category as the field name. Store one field and put the category in a record-level type field. "One field per type" feels organized while you are building it and becomes a maintenance cost the moment you add the next type or read the data somewhere new, because every downstream lookup has to branch across the parallel columns. A single field plus a type filters with one condition and grows by adding a type value, not by adding a column. This pairs with how the submissions table already worked. Each form submission is its own record with its own attachment, so nothing is overwritten and the table itself is the history. A record-level type is the same move applied to the field layout that one-record-per-event applies to the rows.

---

## Lesson 6 (optional) — Give every record a real name with a primary-field formula, which also guards your links.

**Case study — Coding Clarified 2025-08-19, and AY Media 2026-04-14.** Airtable shows a record's primary field (the first field in a table, which Airtable displays as the record's name) as its name. When that field is blank, the record reads "Unnamed record," which is unusable in link pickers, interfaces, and emails. The fix is to set the primary field to a formula so every record has a readable, unique name. An unnamed record shows when the primary field is blank, and the primary field is blank when there is no formula for it. I do not want the primary field blank, so I set it to a formula that concatenates a couple of distinguishing values, for the Coding Clarified submissions something like student, day of the week, and form submission, so every row reads as itself.

The second reason to make the primary field a formula is that a formula cannot be written to. When you paste values into a link-record field, Airtable will happily create a brand-new record on the far side for anything that does not match. If the far side's primary field is a formula, a paste can only link to rows that already exist. It can never fabricate one. On the AY Media migration this is what stopped a bulk paste from creating junk library records. Paste values into a new field that do not exist within, say, the ad-size library, and Airtable creates records for them, which is a problem because you want to spot what you are about to create rather than let it happen silently. So when migrating, I make the primary field a formula. Copy and paste the values in, and if the exact name does not match the formula to a hundred percent, nothing maps and the cell is left blank. Then I go through the blanks by hand.

**Principle.** The primary field is doing two jobs. It is the record's display name, so it should never be blank; a formula that concatenates a couple of distinguishing values gives every record a readable, unique label. And because a formula is not writable, making the primary field a formula stops a paste from creating new records by accident on the far side of a link: paste-to-link either matches an existing record or leaves the cell blank, and blanks are recoverable while silently-created junk records are not. One formula, two problems solved. The full migration method that rests on this is in Module 2, but the schema-level habit is: name every table with a primary-field formula, always.

---

## What I'd do differently now

Draw the whole model on one screen before I build a single field, and mark next to every attribute the exact table level where it is first singular. Most of the pain in this module came from placing a field one level off, the total that read zero, the tripled QuickBooks ID, the per-line contact, and only finding out at the form or the PDF, which is the most expensive place to find out. If I had written "section is only known at the insertion order, so product lives there too" at the start, I would not have re-mapped Fillout twice.

I would also treat a one-to-one relationship as a question to answer out loud, not a table to keep by default. The Insertion Order table survived for months because "the client does not want to read 'line item'" felt like a data reason and was actually a label reason. I now separate those two the moment they come up: what does the backend need to be, and what does the screen need to say. They are almost never the same decision, and confusing them is what put a 14,000-row duplicate table in the base.

And I would be slower to abandon my own first instinct. I was right that inventory sells per position, right that ad size is not one-to-one with a slot, and right that a lookup was correct for net rate. In all three I went along with a reversal before it came back around. A confident correction is not the same as a correct one, and the calls where I held my line are the ones the final schema actually reflects.

## Exercises

1. **Find your one-to-one.** Open a base you maintain and list every pair of tables joined by a link. For each pair, ask the Lesson 1 test in words: is there a concrete, nameable reason a single parent row will ever have more than one child row here? If you cannot name one, sketch what combining the two tables into one would look like, including which fields become hidden rather than deleted, and which inbound links you would have to clear first.

2. **Place three attributes.** Pick three fields in your base and, for each, write the single table level where its inputs first become single-valued. Then check where the field actually lives today. For any field that sits higher than its correct level, predict the symptom (a value that will not compute) or lower than it (duplicates), and confirm the prediction against real records before you move it.

3. **Collapse a field-per-type.** Find a table where you have parallel fields that differ only by a category (attachment-A / attachment-B, note-internal / note-client, date-start-course / date-start-internship). Rebuild it as one field plus a single-select type, migrate a few records by hand, and write the one filter condition (type = X) that now replaces having to know which column to read. Notice what your downstream lookups no longer have to branch on.
