# Module 2 — Data Normalization

*Rachael Quisel · Systems Thinking for Airtable · July 2025 – June 2026*

---

## Frame

Across the eleven months of client builds behind this course, the thing that broke was almost never the automation. It was the data the automation ran on. A WooCommerce export put a student and their purchase on the same row. A Blackboard CSV had no stable identifier to match a grade back to a person. An AAPC number was stored as a number, which quietly dropped the leading zero that made it eight digits, so every lookup missed. Seven hundred migrated line items sat in a table with no link to the contract they belonged to.

None of these were logic problems. They were structure problems. The data arrived structured wrong, or with the wrong key, or duplicated across two places that would eventually disagree.

This module is about getting data into a structure a model can use. It is also about matching records to each other by something real, instead of by a name a student mistyped on their fourth purchase. Every lesson here is a specific move on a specific table with a specific field. That is the only level where the move is repeatable.

The pattern is never "normalize the data." The pattern is "the AAPC number lost its leading zero because it is stored as a number field, so rebuild it with a length formula and stamp it as single-line text." That is the level I work at, and it is the level that transfers.

I am also going to show you the places where I changed my own recommendation partway through a build, and the calls I reconsidered later. Those are not footnotes. The reversal on the Blackboard key is the single most useful thing in this chapter. It shows that "pick a unique key" is not a one-shot decision. It is something you get wrong, notice, and correct.

## Prerequisites — you can't normalize what you haven't modeled

Module 1 is the prerequisite everything in this module depends on, and the order is not arbitrary. Every normalization move below assumes you already know what the entities are and how they relate.

You cannot decide that a student and an order are two records instead of one until you have decided that "student" and "order" are two different things in your model. You cannot match a Blackboard grade row to the right person by a stable key until you have decided which table owns student identity. You cannot paste-link 700 orphan line items to their contracts until you know that a line item belongs to exactly one contract.

So the whole of Module 2 rests on one sentence from Module 1: model the thing before you touch the data. If the model is wrong, normalization will faithfully produce consistent, deduplicated, correctly-keyed garbage. Get the entities and their cardinality (whether each record links to one other record or to many) right first. Then come back here.

---

## Lesson 1 — One import, two tables: upsert the entity, always create the event

**A recurring event and the entity it belongs to are two tables; you search-or-update the entity on a unique key and you always create the event.**

### Case study — Client A, 2025-07-29

The Client A base had one WooCommerce feed and one problem. Every purchase appended a new row, so a student who bought three products showed up as three students. The client, Janine, was also having students re-enter their Social Security number and AAPC number on every purchase. That meant the "student" data got worse with each order, not better.

The first move is to split the one feed into two tables. Students is one record per person, deduplicated. Orders is one record per purchase, never deduplicated. One WooCommerce order writes to both. It searches Students by a unique key and either updates or creates that one record, and it always creates an Orders record.

Here is the mechanism in plain terms. By mapping the matching fields from WooCommerce, you ask the Students table one question: do I already have a record with this exact email address? If I do, update that record. If I don't, create it. In a tool like Make, that combined find-then-write is called an upsert. Then you go to the Orders side and search nothing. You just create, because every order should be created. An order is an event, and events never get deduplicated.

The second half of the lesson is link direction, and it is the part that is easy to get wrong. The tempting instinct is to create the order, then update the student to point at it. That is the mistake. Writing a link from the student side overwrites the student's whole set of orders every time.

Here is why. If a student already has orders, then when you upsert the student and link the order you just created, you are writing a single order into a field that used to hold one or several. You overwrite the existing set with the one new value.

Go the other way around instead. First find-or-create the student. Then, at the order level, link the student. You always get exactly one link at the order level, because an order belongs to exactly one student, while a student can belong to many orders.

So the link gets written from the many-side. The order links to the student, because an order has exactly one student, and writing exactly one value never overwrites a set.

### Principle

A transaction and the party to the transaction belong in different tables. Upsert the party on a stable key so you never duplicate people. Always create the transaction so you never lose a purchase. And write the one-to-many link from the side that holds exactly one value, because a write to the one-side is a single value and a write to the many-side is an overwrite.

### A call I made, and one I reconsidered

Two decisions on this design are worth pulling out.

The first is which submission wins on a repeat purchase. The obvious default is to update the student's fields with the latest submission, on the reasoning that newer data replaces older data. I thought about it and decided the opposite. On this base, later submissions were less trustworthy than the first, because students kept mistyping their SSN and AAPC on repeat purchases. There was no reason to believe the fourth entry was more correct than the first, and good reason to believe it was worse.

So the design became first-submission-wins. On a repeat purchase, the automation links the new order and touches nothing else on the student. That is a normalization decision disguised as an automation decision. When later inputs are no more reliable than the first, freezing the value is the correct move. If I had defaulted to "newest wins" without asking whether newer was actually better, the base would have degraded a little with every repeat buyer.

The second decision I reconsidered months later, when the students-to-orders cardinality came back on a different field. On 2025-11-25 I was deciding where the course start and end dates should live. My first thought was to put them at the student level, precisely so a lookup (a field that pulls in a value from a linked record) wouldn't return an array. A student can have multiple orders, so if you look up start and end date from orders, you get an array of start dates and end dates, one per order. That is awkward to read and awkward to build on.

Then I looked at the actual product model and reversed my own reasoning. Each of the three products has its own start-and-end window, so the date is an attribute of the order, not the student. Moving it to the student level would have been putting a value at the wrong level to avoid a display problem. The date stayed at the order level, and the array problem is handled where it actually needs handling: filter the lookup to the active order, sort by date, and take one.

The deeper lesson: cardinality decides where a value lives. "A lookup would return an array" is a sign that you put the field on the wrong side, not a reason to move the data.

---

## Lesson 2 — Match-and-update by a real unique key, and be willing to change your mind about which key

**A recurring import should find the target record by a stable unique key and update it, never insert; pre-create the target so the import is pure update; and expect to get the key wrong the first time.**

### Case study — Client A / Blackboard, 2025-09-23

I was importing Blackboard grade CSVs and had no reliable way to attach a grade row to the right student. Names change and get transcribed differently across systems. If the import ran as a plain create, every run would insert students who already existed, and I would be back to duplicates.

The structure has two parts. First, guarantee the target record exists before the grades arrive. When a student is created in the Students table, an automation immediately creates one linked record in the Blackboard table. Now there is always exactly one Blackboard record per student to match into. For every student, you have one Blackboard record, created the moment the student is.

Second, the CSV import loops each row and updates that record. For each row in the sheet, a loop node finds the student on the Students table by email address, finds the matching record in the Blackboard table for that student, and updates it with everything on the row. Find-if-exists, update; never insert.

### The reversal — this is the part to keep

The whole lesson hinges on the phrase "based on email address," and that key was my second answer, not my first. Earlier in the same working session I had argued the opposite to myself: store the Blackboard learner ID on the student record and match on that. The idea was to keep a Blackboard ID on each student so that, when I built the API connection later, I could ask the Blackboard query table whether a student with a given ID already existed and branch on that.

Then I traced it through the actual workflow and realized the Blackboard ID gave me nothing if the match was still going to run on email. Storing the ID did not make the import any simpler. It is a pleasant thing to have a tidy database with every learner's ID on the record, but that was not something I couldn't add later, equally well, once I actually had an API connection to populate it. So I reversed my own advice and dropped the ID as the match key.

And then email failed too. The Blackboard export does not carry an email address at all. So the match fell to first name and last name, which is exactly the fragile key the whole exercise was trying to avoid. From Blackboard you do not get an email, so you are forced to match on first name and last name. That is not great, and knowing it is the point.

I am keeping all three steps because the sequence is the point. Blackboard ID, then email, then first-and-last-name against my own better judgment. The unique key is the part that matters most, and picking it is iterative. You propose a key, trace it through the actual import, and demote it the moment you find the field it depends on does not exist in the source file.

### Principle

Recurring imports are updates keyed on a stable field, not inserts. Pre-create the record you are going to update so the import never has to create. And treat "which field is the unique key" as a hypothesis you test against the real export, not a decision you make once up front. The best key that is not actually in your data is worse than a mediocre key that is.

### The delivery decision I held to

By 2025-11-25 the delivery mechanism for these Blackboard updates changed, and this is a place where I chose a lean solution over a heavier one and kept it. I had built a small CSV-export table plus a lookup so the latest Blackboard values were always available to interfaces.

I weighed the tradeoff honestly. The lean version is lean, and I liked that. What I did not love is that it manufactures records purely to stage a value, and that has three real costs. It is not the tidiest structure, it increases record count, and it requires lookups, and lookups reduce base performance. The heavier alternative was an n8n flow mapping incoming data straight into the right tables, with no staging records and no extra lookups.

I kept the lean version anyway, and the reason was the operator, not the architecture. The real person running this on the client side was a non-technical admin who needed something as simple as emailing a CSV to an address. The value of the emailed-CSV approach is that you can hand it to someone with no technical background and they just use the email address. For them, loading a CSV into a database through an import screen is hard; sending an email is not.

Airtable's CSV-via-email sync upserts by a chosen unique field on receipt, so the match discipline is preserved, and the operator never touches an import screen. The extra records and lookups were a cost I accepted to remove that difficulty. Plenty of production bases run hundreds of lookups without trouble.

The constant across every version of the delivery: the match-and-update discipline stayed the same. Whether the update arrived via n8n or an emailed CSV, it was always find-by-unique-key-then-update, never insert.

---

## Lesson 3 — Reconstruct a mangled key before you match on it

**When a number field has stripped the leading zeros off an identifier, rebuild the identifier with a length-based padding formula, then convert to single-line text and stamp the values so downstream matches work and the processing can be removed.**

### Case study — Client A, 2025-07-30

The AAPC number is the identifier that ties a Client A student to their record, and I was matching WooCommerce orders to students on it. The matches were failing for a whole set of students, and I could not see why.

The reason was that AAPC numbers were stored in a number field. An AAPC number like `00241908` is eight digits with two leading zeros. A number field cannot hold a leading zero, so it stored `241908` as six digits. The exact-match lookup was comparing a six-digit stripped value against the true eight-digit identifier and missing every time.

I looked at one student's number, Stacey's, and worked it out in real time: the true values were eight digits, and the field was holding six or seven. So I built the reconstruction directly on the table. The formula reads the length of the stored number and pads it back to eight. If the length equals six, put two zeros in front of the AAPC number. If the length equals seven, put one zero in front. Otherwise, leave it blank, because that record has no number at all.

The formula alone was not the end, because a formula field is live and computed, and I needed a stable text value to match on. So I duplicated the field, changed the type to single-line text, and stamped the reconstructed values in place. Once the values are stamped, you have the real AAPC numbers sitting as static text, and you can delete all of the reconstruction processing. The first time I stamped a formula field down to static values, I did not know Airtable would let me do that. It turns a live computation into a permanent stored value in one step.

### Principle

An identifier with significant leading zeros is text, not a number, and storing it as a number silently corrupts it. When that has already happened, you can rebuild the original by keying the padding off the string length. But the reconstruction has to be frozen as text before you rely on it, because a match key needs to be a stable stored value, not a live formula that could recompute.

### The shortcut I moved away from

My first idea that session was the shortcut, and I flagged it to myself as the lesser option before building the better one. The shortcut was to change the number field to single-line text and leave it there. That is not ideal, and here is the specific reason: converting the number field to text would not have brought the missing zeros back, because they were already gone the moment the value was stored as a number. Changing the type preserves the six-digit damage; it does not undo it. The zeros had to be reconstructed from length first, then frozen.

The general rule this leaves me with: when a key is mangled, figure out exactly what transformation mangled it and reverse that specific transformation. Do not hide it with a type change that keeps the damage.

---

## Lesson 4 — Link migrated rows with a formula match-key, and let a formula primary field guard the write

**To connect migrated records to their parents without creating new records, build a formula match-key, make it the primary field on the target table, then paste the key into the link field so equal keys link and nothing new can be created; leave a row blank rather than force a wrong link.**

### Case study — Client B, 2026-05-22

Client B's migration left roughly 693 contract line items with no link to the contract they belonged to. The obvious move, pasting a column of values into the link field (the field that connects a record to records in another table), is dangerous by default. Airtable will create a brand-new record for any value that does not exactly match an existing one, so a near-miss produces a new contract by mistake instead of a link.

The method removes that danger by construction. Step one: build a formula field that concatenates several fields into one unique match-key. Step two: make that formula field the primary field (the first field in a table, which Airtable shows as the record's name) on the target table. Step three: paste the match-keys into the link field. Because the primary field is a formula, it cannot be written to, which means the paste can only link to a row that already exists and can never create a new one.

That single design choice solves two problems at once. First, you now have something exact to map against: the concatenated key. Second, because the primary field on the other side is a formula and therefore not writable, pasting into the link field physically cannot create a new record. You only get links to rows that already exist. The one thing you have to get right is that the key is genuinely unique and genuinely maps, so spend your attention there.

The second half of the rule is what you do with a row that does not match exactly. You leave it blank. If two values look similar but are not exactly the same, you do not force the link. You leave the row blank and go figure out what is actually going on with it, rather than guessing.

This is the same paste-to-link move I had used a year earlier on Client A, when I linked 643 already-imported students and orders by pasting the AAPC column into the link field. Back then it worked and I could not fully explain why. The mechanism is this: when you paste the full list of AAPCs into the link field, each pasted value finds the primary-field record with the exact same AAPC and links the two together. The Client B version added the safeguard that makes it safe on messy data: make the primary field a formula so the paste physically cannot create a record.

### Principle

A formula primary field stops a paste from creating new records by accident during a bulk link operation. It gives you something exact to match against, and because it is not writable, it turns "paste to link" into "link only, never create." A blank link is recoverable at any time. A wrong link is silent corruption that nobody will notice until it produces a wrong number in a report. So require an exact key match, and reject anything fuzzy for an identity link.

### The shortcut I turned down, and how the key evolved

I proposed exactly the shortcut you would expect, an agent field doing fuzzy matching on net rate to close the near-misses, and I rejected it. A few weeks later, on 2026-06-08, I restated the rule for the remaining orphans as a hard test. If a line item does not match, you are probably looking at a different contract. So you find the unique identifier that actually distinguishes contracts, and if a single field is not enough, you build it from a combination: years, QuickBooks ID, date, account executive. If everything in that combination matches, you link. If it does not, you create a new record instead of forcing the link.

The evolution was in how the key got built, not in the rule. When a single field was not unique enough, the key became a combination of fields, years plus QuickBooks ID plus date plus account executive, until it was actually unique. The discipline held: exact match or nothing.

---

## Lesson 5 — Convert lookup-to-static to move data during a migration, and turn migration-only links into plain text

**To move a field's data off a table you are about to delete, create a lookup of it on the surviving table, change the lookup's field type to plain text so the value freezes, then delete the source; and any link you keep only for migration provenance should be converted to text so it stops acting like a live relationship.**

### Case study — Client B, 2026-05-22

Client B had a Contract Line Item table and a separate Insertion Order table, and every line item produced exactly one insertion order. That is a persistent one-to-one, which meant 14,000 duplicate records carrying only lookup fields. I decided to delete the Insertion Order table. The problem: several fields the client actually used (artwork status, current stage, designer, editor) lived only on the insertion order, and deleting the table would delete them.

The method moves those fields down onto the surviving Line Item table without a script. It is a little inelegant, but it works. On the line item, create a lookup of each field you need to keep. A lookup is live, so at this point it is still reading from the insertion order. Then change each lookup's field type to single-line text, single-select (a field where you pick one option from a fixed list), or checkbox as appropriate. Changing the type ends the live connection and freezes whatever value the lookup was showing into a real, native field on the line item. Before this, the line item did not have those fields of its own; after it, it does.

Once the type change has frozen the values, rename the new fields to whatever they should be called on the line item. At that point all of the data has been migrated onto the surviving table, as long as the link was in place while you did it. Then you delete the insertion order records and delete the insertion order table.

The order is the whole method: lookup first (copies the value live), type-change second (freezes it), delete third (removes the source). Skip the freeze step and deleting the source wipes the value you just moved, because a lookup holds nothing of its own.

### The second half — migration-only links become inert text

Once the data is moved, you are often left with link fields that exist only to remember where a row came from. On 2026-06-08 I ran into this with line items that carried both a new Contract link and an old Contract-Line-Item link, plus contacts linked at two levels. A link kept for provenance is not inert. Airtable treats it as a live relationship, which produces double-links and makes the base contradict itself for anyone reading it later.

The rule: if you are keeping a reference only to record where something came from, it should be text, not a link. Rather than leave them linked, convert them into a single-line text field with a name like "migration source," so the value stays as a note and stops behaving like a relationship. Otherwise you have double entries everywhere, meaning double links, which produce inconsistency and a base that is hard to maintain.

### Principle

A lookup reflects its source live; a converted field is a static snapshot. That single distinction is the entire in-place migration method. Create the lookup to copy, change the type to freeze, then delete the source. And a reference you keep for history should be inert text, because a live link asserts a relationship your model no longer means, and two links to the same parent is a contradiction that will eventually show up in a rollup (a field that combines values from linked records).

### Where it extended

The same 2026-06-08 pass revealed a related defect the migration had left behind: contacts were linked per line item, when a contact relates to a whole contract. Linking a contact to each line item instead of to the contract is the wrong level, and it shows up as the same contact repeated across every line of a contract. The fix was a repeatable pipeline rather than a one-off. Build a filtered view of the inconsistency (contract is empty) to isolate the orphaned line items, create-or-link their parent contracts by the exact-match rule from Lesson 4, then move the misplaced contact up to the contract level using the same lookup-then-paste-then-delete move from this lesson. The convert-lookup-to-static move is not just for deleting a table. It is the copy step of any in-place data move.

---

## What I'd do differently now

**I would decide the unique key before I decide anything else, and I would confirm the field it depends on is actually in the source file.** The Blackboard sequence, ID then email then first-and-last-name, cost real time because I picked keys that were not in the export. Now the first question on any import is: what field uniquely identifies this record, and can I see it in the file in front of me? If I cannot, I have not chosen a key yet.

**I would store every identifier as text from the start, not as a number.** The leading-zero AAPC failure was avoidable. Anything I match on, or that a human reads as a code rather than counts as a quantity, goes in a single-line text field the day the table is created. A number field is for things you do arithmetic on.

**I would build the safeguard before the bulk operation, not after I got scared.** Making a primary field a formula, so paste-to-link cannot create records, is a thirty-second setup that removes an entire class of silent corruption. I now do it before any bulk link, not only on migrations I have already decided are risky.

**I would treat "a lookup returns an array" as a signal I put the field on the wrong side.** My reflex used to be to filter and sort the lookup until the array collapsed. That is sometimes the right fix, but first I ask whether the value simply belongs at the other level, the way the course dates belonged on the order, not the student.

**I would leave rows blank without apologizing for it.** A blank link I can find and fix any time. A wrong link hides until it produces a wrong total. "Leave unmatched over wrong match" is now a default, not a fallback.

---

## Exercises

**Exercise 1 — Split one feed into two tables.**
Take any single-source import you have where one row mixes a person with an event (a purchase, a booking, a submission). Model it as two tables: the entity (deduplicated, one record per person) and the event (one record per occurrence). Connect the import so it searches the entity by a unique key and updates-or-creates, and unconditionally creates the event. Then write the link from the event side and prove to yourself that a second event for the same person does not overwrite the first. Write one sentence naming your unique key and one sentence naming the field it depends on in the source.

**Exercise 2 — Break and rebuild a mangled key.**
Put a set of identifiers that have leading zeros (ZIP codes, member IDs, anything eight digits starting with a zero) into a number field on purpose and watch the zeros disappear. Then rebuild them: write a formula that pads each value back to its correct length based on its current length, convert the result to single-line text, and stamp the values. Confirm an exact-match lookup against the rebuilt field succeeds where it failed against the number field. The point is to feel the difference between a live formula and a stamped static value.

**Exercise 3 — Paste-to-link a backlog without creating anything.**
Take two tables that should be linked but are not (invent 20 rows if you have to, with a handful of deliberate near-misses that are close but not exactly equal). Build a formula match-key, make it the primary field on the target table, and paste the keys into the link field. Verify two things: every exact match linked, and every near-miss stayed blank instead of creating a spurious record. Then, for each blank, decide by an exact-key test whether it should link to an existing parent or get a newly created one. Do not fuzzy-match your way out of the blanks.
