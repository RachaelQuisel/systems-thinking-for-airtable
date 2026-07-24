# Module 3 — Workflow Building

*Systems Thinking for Airtable. How I turn a form into a working pipeline: parent/child forms, branching upstream, the cascade selector, fanning one submission out into many records, and the update-vs-create distinction. Built from my Client A and Client B work, July 2025 through June 2026.*

---

## Frame

A workflow is the path a piece of data takes. It starts when a person types it into a form. It ends when the data lands, correctly shaped, in the right rows of the right tables.

Module 1 was about modeling the thing. Module 2 was about getting normalized data into the model. This module is about the forms themselves: the Fillout forms that clients, students, and sales reps actually touch, and the automations that catch what those forms produce.

Two ideas run through everything here.

The first: build the manual pipeline first, then automate the parts that repeat. On Client A I hand-created records to place existing students at the right stage before I set up a single scheduled automation. On Client B I built one contract form, mapped it, and tested it. Only then did I talk about duplicating anything. The automation is the last step, not the first.

The second: know exactly what your tool can and cannot do, and move the hard part to the layer that can do it. Fillout generates every mapped PDF on submission and cannot branch its outputs. Fillout cannot compute a calendar date. Fillout cannot read a value out of a linked-record field. Fillout writes multi-layer records from the bottom up, and it leaves the child records with no parent when someone abandons the form.

Every lesson in this module is a version of the same move. The tool cannot do something, so you resolve the branch, or the calculation, or the identity one layer earlier, in Airtable. I call that place upstream: earlier in the flow, before the form runs. That is where the logic is easy to write and easy to inspect.

I want to be honest up front about where this approach went. Fillout's limits kept costing time on the Client B calls. I spent months weighing whether Airtable "Site," or eventually a custom-coded frontend, would be a better entry point. I kept choosing Fillout because the client had chosen Fillout. I still think Site would not have solved their specific problem.

The Fillout PDF work that fills much of these sessions is an approach I dropped entirely once I moved PDF generation to Adobe. So read this module for what it is: a set of patterns that were correct for the tool in front of me, some of which I would not use again. The patterns transfer to other tools. The tool itself was a phase.

### Prerequisites (Modules 1 and 2)

You cannot build a form until the tables it writes into are settled. A form is just a set of writes into a schema.

- **From Module 1 (Schema Design):** the Contract → Line Item structure. The rule that a value lives at the level where it is uniquely known (the calculation on the child record, a total rolled up to the parent with a rollup, a field that adds up values from linked records). And the difference between a lookup (a live, read-only field) and a direct field (one you can write into). A form can only write into direct fields. If a destination is a lookup, the form's data has nowhere to land.
- **From Module 2 (Data Normalization):** match keys, and the rule that you link records on a stable unique identifier, never on a name a human can edit. The fan-out pattern in this module keys entirely on a submission ID. The parent/child pattern keys child records to their parent by a record ID passed in a URL. If you have not internalized "link on the ID," none of this works.

One dependency is worth naming, because it caused a rebuild on Client B. Fields that receive Fillout data must be direct fields, not lookups. Everything coming in from Fillout into the Invoice table has to be a direct field, so the data lands in the right place.

One of those destinations turned out to be a lookup. The incoming Fillout data had nowhere to go. I had to create a separate direct field for it, and that new field no longer matched the historical record. That single mismatch, a form writing into a field that was actually a lookup, is why I deleted and rebuilt the table. Settle the schema, then build the form.

---

## Lesson 1 — Fillout parent/child forms: the contract is the parent, the line item is the child

**A multi-record submission is built as a parent form (the contract, one record) with a child form nested inside it (the product line item, one record per product added); the child form is how a user adds more than one line item to a single contract.**

### Case study — Client B, 2026-05-08 (call 665069340)

Client B sells magazine advertising. A single contract has many line items, one per product an advertiser buys. The question was how one Fillout submission could create one contract record plus a variable number of line-item records linked to it.

The answer is Fillout's parent/child form structure. The parent form collects the contract-level fields: advertiser, contact, contract total. A child form nested inside it collects one product line item at a time. Each time the user adds another product, the child form produces another line-item record. All of them link to the one parent contract.

By this call the client had simplified the model. They dropped a third form layer they had originally wanted for insertion orders. That left just the parent form and the child form. The parent form is the contract, the child form is the product, and each product is one line item. Cutting the third layer made the whole build much simpler.

The thing that broke, and that I spent the first twenty minutes of that call on, was the total. The parent form has to show a contract total that sums the child line items.

Trace the calculation from the top. There are two layers. The contract is the parent form, and it carries a calculation for the total of the invoice. That total adds up the line-item totals. Each line-item total is computed on its own line item.

That is the whole structure. The child form computes a line total on each line item: quantity times per-unit cost. This is Module 1's rule that the calculation lives on the child. The parent form then runs a Fillout calculation that sums those line totals into the contract total.

I used Fillout's own calculation for the sum, not an Airtable rollup. The reason is a timing fact covered in Lesson 4: the Airtable rollup is not filled in time for the PDF fill.

### Principle

A one-to-many relationship (one contract, many line items) maps to a parent form with a nested child form. The parent is the "one" and holds the total. The child is the "many," and it is how a user adds more than one of them in a single submission. Anything the parent needs to display that depends on the children, a total or a count, has to be computed inside the form or has to already exist at the time the PDF is filled.

### Where it broke / changed

Multi-layer Fillout forms write records from the bottom up, and that is a real risk. On the three-layer version of this form the problem was plain. As soon as the grandchild form is filled, it creates the grandchild record. Submit the child form and you get the child record. If a person abandons the form before submitting all the way up to the parent, you are left with records that have no parent: partial submissions sitting in the base. I call these orphan records.

So a person who fills the child form and then closes the tab leaves a line-item record with no parent contract. Two consequences followed.

First, give every level a primary field built from a concatenated formula, never a blank one. The primary field is the first field in a table, which Airtable shows as the record's name. With a formula there, an orphan record is at least readable instead of showing as "unnamed record."

Second, build an inconsistency view that finds the orphan records: created before today, parent link empty, submission ID not empty. Delete them on a schedule, because orphan records overstate any per-product sales count. That scheduled deletion is a Module 4 automation, but the reason it exists is this form behavior.

And the larger change. This parent/child form produced a Fillout-generated PDF. By April I had moved PDF generation off Fillout to the client's Adobe template, filled by API. Much of the mapping work in these calls was for an output I later abandoned. The parent/child record structure survived. The PDF integration built on top of it did not.

---

## Lesson 2 — Branch upstream, not in the tool

**Fillout generates every mapped PDF on every submission. It cannot conditionally branch its outputs. So when you need different documents for different cases, you duplicate the form once per case and select the right one with a single Airtable formula field, not with logic inside the tool.**

### Case study — Client A, 2025-08-26 (call 390509922)

Client A enrolls students in four states plus a headquarters default: Florida, Indiana, South Carolina, Texas, and HQ. Each state has its own enrollment agreement PDF. I wanted one enrollment form that would produce only the state-appropriate PDF.

Fillout cannot do that. By default it will not let you decide, based on a URL parameter or any other condition, whether a given document should be generated. The PDF integrations always run on submission. You cannot set conditional branches like "if California then fill this PDF but not the other three."

The fix moves the branch out of Fillout and into the data. You build one enrollment form per state, each with exactly one PDF integration. Then you put a single formula field in Airtable that outputs the correct form URL based on the student's state. The automation that emails the student just sends whatever that one dynamic field resolves to.

There are two ways to write the selector formula: nested IF or SWITCH. I went with SWITCH because it gives you a shorter formula. You name the field you are checking once, then say: if it contains FL do this, if it contains IN do that, and so on. It reads the field's value and outputs a result without any nested IF formulas.

The ordering rule that makes this manageable: get one form right, then duplicate. Do not duplicate first and then fix five copies. Delete the state copies. Get everything working on the headquarters original. Only then create a duplicate. Map everything correctly on that one form first, and once it works as expected, duplicate it. Otherwise you spend all your time fixing each copy.

### Principle

When a tool cannot branch its own output, do not force the branch inside the tool. Make one copy of the form per case. Resolve which copy to use once, upstream, in a formula that already knows the answer. Then let the automation carry a single dynamic value. The branch lives in exactly one place, and it lives in the layer you can read and edit.

### Where it broke / changed

I made the exact mistake this lesson warns against, and I caught it two days later. I had started building the state conditional inside the automation, keyed off base-structure field IDs. That is the wrong layer. Writing "where the field ID of some base-structure field is TX, then do something" is not the correct way to do it. The better move is to drop that logic entirely and keep only the email action. The URL is already dynamic and already captures the state.

That is the whole principle stated as a correction. The URL formula already captures the state, so the automation must not repeat the same conditional. Resolve the branch once. It belongs in the formula field, not the send step.

---

## Lesson 3 — The product-selection cascade: attributes filter down to one product

**When users refuse a flat product dropdown, model the product as the combination of its attributes and build the form as a cascade where each attribute filters the next, ending in a product link-record field with a dynamic filter that matches everything chosen above it.**

### Case study — Client B, 2026-02-12 (call 564364653) and 2026-05-08 (call 665069340)

Client B adds new products every couple of weeks, and the client would not accept picking a product from one long dropdown. A "product" there is really a combination: publication, ad size, ad type, ad position, frequency, issue month, issue year, special section.

So stop asking for the product at all. Ask for each attribute in order, then let a dynamic filter resolve the single matching product. This ordered set of questions, where each answer narrows the next, is what I call a cascade.

You fill out the attributes. Rather than have an automation decide which product that is afterward, you put a product link-record field at the bottom (a field that links to a record in another table). Its dynamic filter says: only show the options that match every condition chosen above. The attributes above become the filter.

I chose the dynamic filter over letting an automation guess because it is safer. The attributes are the filter, so the product cannot come out inconsistent with the choices. For this to work, each attribute has to be its own link-record table, which I call a library. That way the selections can filter each other. You set the logic in Airtable, not inside Fillout, and you build out the libraries. Either way you need the libraries for the filters to constrain one another.

By the May 8 call I had defined the exact filter order and the operator. The cascade is strict: every level filters on every level above it, using `contains`. The order is class, publication type, publication, issue year, ad size, ad type, ad position, frequency, month, special section. Then the product field filters on all of them above it. I kept `contains` as the operator across every level, because it was already working and mixing operators was part of what had broken.

The bug I was fixing when I worked this out: the picker showed no products at all. Filters were skipping intermediate levels and mixing operators. The rule that fixed it: every attribute filters on the full set above it, always `contains`, and the product field filters on all of them.

### Principle

A dependent picker is a cascade, and the logic belongs in the data model, in link-record library tables, not buried in form configuration. Each level filters on every level above it, consistently. The product is not selected. It is the only option left once every attribute has narrowed the set. That is safer than an automation deciding the product afterward, because there is no moment where the attributes and the product can disagree.

### Where it broke / changed

Two things. First, one of these attributes turned out not to be one-to-one with the sellable unit, and I had to keep it as a separate choice. When I modeled inventory as "issue slots," there was a case for saying that if ad size lived on the slot, the separate size selector was redundant. It is not, because a slot can be sold at several sizes. The relationship there is not one-to-one, so it has to stay a filtered choice. What actually is one-to-one for issue slots is the issue year, the issue month, and the ad position, and only those.

The lesson inside the lesson: an attribute only merges into the parent record if it is genuinely 1:1. Anything that can have several values stays a filtered choice in the cascade, or you undercount inventory.

Second, I later found redundant libraries. Ad Size ("half") and Ad Pages ("0.5") stored the same fact in two tables, both with duplicated rows, and that confused the cascade. Two libraries storing one fact is redundant, so I kept one. The cascade is only as correct as the libraries feeding it.

---

## Lesson 4 — Fan one submission out into many records

**A single Fillout submission that contains many rows (seven day-answers, a variable list) is sent both to Airtable and to a webhook automation; the automation waits a few seconds for the parent record to land, fetches it by matching submission ID, then creates one child record per row and links each back to the parent.**

### Case study — Client A, 2025-07-29 (call 364852797)

The weekly attendance form has one submission carrying seven day-answers: Monday attended, Tuesday attended, and so on. Each day needs to become its own record in the Attendance table. But the direct Fillout-to-Airtable integration writes one field per question into a single record. It cannot turn one submission into seven records in a different table.

The pattern sends the submission down two paths at once. Path one is the normal Fillout-to-Airtable integration. It creates one Form Submissions record carrying a submission ID that Fillout itself generates. Path two is a webhook that triggers an Airtable automation. A webhook is a message the form sends to trigger the automation. The automation waits about five seconds, so the Form Submissions record is guaranteed to exist, then finds it by submission ID and creates the per-day records against it.

The wait is deliberate. Two integrations run at once. One sends the answers to the Form Submissions table along with a submission ID. The webhook fires in parallel. Waiting five seconds makes sure the Fillout-to-Airtable integration has finished, so a new Form Submissions record exists with its submission ID. Only then does the automation look up the form submission where the submission ID equals the submission ID from the webhook call. It searches on that submission ID, links each new record to the matching form submission, and creates one record per day.

The whole thing keys on the submission ID. That ID is the stable unique identifier that ties the resulting child records back to the one parent submission. This is Module 2's "link on the ID," applied to an event instead of an entity.

There is a companion technique that makes the reverse case work: one shared form that has to know who is submitting. Each order's tracking-form link carries the student's record ID as a URL parameter. The form has a hidden field that reads that parameter as its default value, so the submission attaches to the right student without asking. You set up the URL parameter in the form settings under URL parameters, add a new one, then tell the hidden field to prefill with the value found in the URL parameter called student record ID.

### Principle

To turn one submission into many linked records, do not look for a built-in form feature that does it. There usually is not one. Send the submission to Airtable and to a webhook automation in parallel. Key the automation on the submission ID. Give it a short wait, so the parent record lands before the automation goes looking for it. One submission, one parent record, N child records, all tied together by an ID the form tool generated for you.

### Where it broke / changed

The reason this has to be a webhook automation, and not one scheduled automation, is a hard Airtable limit. Airtable does not let you use both a repeating group and conditional logic in the same automation. If it did, I could handle every tracking-form case in one automation. Because it does not, you need multiple automations.

You cannot loop over found records and branch per record in the same Airtable automation. That single constraint shapes a lot of the automation architecture in Module 4. It is why the fan-out lives in its own webhook-triggered automation, rather than folding into the weekly send.

The pattern worked well. It is one of the few from this era I would build the same way again. The only weak point is the five-second wait, which is a timing assumption, not a guarantee. If the Fillout-to-Airtable write is ever slower than the wait, the search finds nothing. On a higher-volume build I would key the create step off the record's own arrival, rather than a fixed wait.

---

## Lesson 5 — Update form versus create form

**An edit to an existing record is a different job from creating one, so you build a separate update form (often a single field), turn off Fillout's native edit-link email, and send your own email carrying the update form's dynamic URL, so you control who gets it and which form they land on.**

### Case study — Client B, 2026-06-08 (call 700311737) and 2026-05-22 (call 682399168)

Two needs on Client B were both edits, not creations, and both wanted their own small form.

The first: after a sales rep downloads a contract, sends it for signature, and gets it back signed, that signed file has to land back on the right record. That is a one-field update, and it should stay one field. It is an update-record form, just one field. Any larger version adds complexity the job does not need.

The second: the manager-approval loop. A rep submits a contract with a proposed total flagged for review. The manager needs to open an update form, not a create form, to approve, reject, or send back one revision.

Fillout has a built-in "send them a link to edit the submission" email. But that URL is opaque, and you cannot control where it goes. So I turned it off and rebuilt the notification myself. In the old workflow, the form was submitted and Fillout sent its own email for the recipient to update the form submission. Once I turned that off, I had to rebuild it on my side. Rather than rely on the opaque URL Fillout was sending, I send an email myself using the dynamic value.

Sending the email myself means I choose the recipient (the manager, not the submitter), I choose the form (the update form), and I control the URL. That is also where the manager reprint button lives. A generated PDF is static, so an approved change to the total does nothing to the already-generated document until someone re-submits the update form to regenerate it. A PDF is fixed once created. It still shows the old contract total, so someone has to go into the form and regenerate or resubmit. Because this is an update form, that is just a few clicks and a submit, which re-triggers the integration and generates a fresh document. On the June 8 call I confirmed it worked: the record was regenerated with the new version of the PDF.

The reprint button is just a button field that opens the update form URL for that record. The manager clicks it, the update form re-submits, the PDF integration runs again, and a fresh PDF replaces the old one.

### Principle

Creating and editing are different jobs and deserve different forms. A create form makes a record. An update form changes an existing one, and it should be exactly as big as the change: one field for a file, one field for a revised total. When a vendor's built-in edit notification is opaque, replace it with your own automation, so you control the recipient, the routing, and the URL. And remember that any rendered document is fixed at the moment it is created. Changing the underlying data changes nothing until you render it again, which is why the update form doubles as the reprint mechanism.

### Where it broke / changed

The update mechanism is a call I reconsidered, because I was answering two slightly different questions at once. One framing said the edit needs a Fillout update form, or Site, because sales reps do not have Airtable edit permissions. But a plain button can update a field without any edit rights. People can click a button without having editing access. So why not just a button that updates the Airtable field directly?

Both framings are right, and the real distinction is what the edit touches. For changing a status, a button is enough. For a rep editing the actual content of their own submission, they need a form. Which one you build depends on whether the edit is one value or many. The split I shipped reflects exactly that: a button for the reprint (one action), an update form for the manager's content edits (several fields).

### Coda — the date Fillout could not compute

One more edit-shaped problem from Client A, because it is the clearest example of the discipline in this whole module. The enrollment agreement had to show an estimated end date equal to the start date plus 120 days. Fillout cannot do date arithmetic to a calendar date. Its calculation only returns a duration. It can do a date-time difference, which tells you the gap between two dates is 120 days, but it cannot set an exact calendar date.

I spent real effort building delays and lookups so the emailed PDF would show a filled-in end date. Then I realized the requirement did not need a computed date at all. The agreement can simply state the rule: the start date is such-and-such, and the end date is 120 days after the start date, with no specific calendar date named. Restating the requirement as text removed the computation, the dependency, and the delay at once. It was the simpler answer, and once I saw it, the obvious one.

Before automating a hard calculation, ask whether the requirement can be restated so the calculation is not needed. Printing "120 days after start date" as text removes the computation, the dependency, and the delay at once. If the tool cannot do the thing, sometimes the answer is not a workaround. It is a smaller requirement.

---

## What I'd do differently now

**I would settle whether Fillout is even the right entry point before building a single form.** For months I built one Fillout workaround on top of another: the state-branch problem, the static PDF, the opaque edit URL, the orphan records, the no-dynamic-line-items limit, the date it could not compute. The case for moving off Fillout kept getting stronger. Even when a code-based frontend looks like more work to start, as soon as things get complicated, which they always do, being able to change code directly is usually easier from that point on. By June I agreed with that for the next client.

But I want to be precise about where I was right to stay on Fillout, because "just use Site" is too broad a rule. The Client B build genuinely needed a dashboard, and Site would not have delivered that. Site would not have helped me avoid any of this, given that the client also wanted a dashboard. If they had not wanted a dashboard, and only wanted the "do not allow me to select something already sold" behavior, that part could have been built with Site. But the dashboard requirement ruled it out.

And the reason I kept choosing Fillout at all was not stubbornness. The client had chosen it, and at the time I had to go with what they were telling me.

So what would I actually change? I would run the tool decision as its own explicit step at the start. I would weigh the real requirements (dashboard? per-record editing? dynamic documents? client maintaining it without me?) against each tool's known limits, and I would put that decision in writing before building forms. The frontend is a handoff decision, not just a question of build power. My own concern about custom code was exactly ownership: I build things for myself on Vercel, but my clients cannot maintain that.

**I would stop building Fillout PDFs before I understood the PDF was going elsewhere.** A large share of these sessions was Fillout-PDF mapping that I abandoned when PDF generation moved to Adobe, filled by API. By April I was no longer creating the PDF in Fillout, which made a lot of that mapping work pointless. The record structures (parent/child, cascade, fan-out) all survived that switch. The PDF integration built on top of them did not. The lesson: separate the durable part of a workflow (how records are shaped and linked) from the disposable part (which tool renders the document). Do not over-invest in the disposable part before it is locked.

**I would replace the fixed five-second wait in the fan-out with something that keys off the record actually arriving.** It worked at Client A's volume. It is a timing assumption, and timing assumptions are the bugs you find at the worst moment.

---

## Exercises

1. **Build the parent/child pair.** In a scratch base, model one Order (parent) with many Line Items (child). Build a Fillout form where the parent form collects the order-level fields and a nested child form adds one line item at a time. Compute a line total on each child (quantity times unit price) and a sum on the parent using Fillout's own calculation, not an Airtable rollup. Now abandon the form after adding one child and before submitting the parent. Find the orphan line item. Write the three-condition inconsistency view (created before today, parent link empty, submission ID not empty) that would catch it.

2. **Branch upstream.** Take a form that must produce one of three different outputs by category. Instead of putting the branch in the form, build three copies of the form, then write a single SWITCH formula field that outputs the correct form URL by category. Confirm that your send automation references only that one field and contains no category logic of its own. Then deliberately add the branch to the automation as well, and delete it, to feel why the duplicated logic is the wrong layer.

3. **Cascade a product out of its attributes.** Model a product as three attribute libraries (each its own link-record table). Build a Fillout picker that asks for each attribute in order, then a product link-record field whose dynamic filter matches all three attributes above it, using `contains`. Verify the product field shows exactly one option once all three attributes are chosen, and shows none when the filters skip a level. Then check each attribute: is it genuinely 1:1 with the product, or does it need to stay a filtered choice? Justify each answer.
# Module 3 — Workflow Building

*Systems Thinking for Airtable. How I turn a form into a working pipeline: parent/child forms, branching upstream, the cascade selector, fanning one submission out into many records, and the update-vs-create distinction. Built from my Coding Clarified and AY Media work, July 2025 through June 2026.*

---

## Frame

A workflow is the path a piece of data takes. It starts when a person types it into a form. It ends when the data lands, correctly shaped, in the right rows of the right tables.

Module 1 was about modeling the thing. Module 2 was about getting normalized data into the model. This module is about the forms themselves: the Fillout forms that clients, students, and sales reps actually touch, and the automations that catch what those forms produce.

Two ideas run through everything here.

The first: build the manual pipeline first, then automate the parts that repeat. On Coding Clarified I hand-created records to place existing students at the right stage before I set up a single scheduled automation. On AY Media I built one contract form, mapped it, and tested it. Only then did I talk about duplicating anything. The automation is the last step, not the first.

The second: know exactly what your tool can and cannot do, and move the hard part to the layer that can do it. Fillout generates every mapped PDF on submission and cannot branch its outputs. Fillout cannot compute a calendar date. Fillout cannot read a value out of a linked-record field. Fillout writes multi-layer records from the bottom up, and it leaves the child records with no parent when someone abandons the form.

Every lesson in this module is a version of the same move. The tool cannot do something, so you resolve the branch, or the calculation, or the identity one layer earlier, in Airtable. I call that place upstream: earlier in the flow, before the form runs. That is where the logic is easy to write and easy to inspect.

I want to be honest up front about where this approach went. Fillout's limits kept costing time on the AY Media calls. I spent months weighing whether Airtable "Site," or eventually a custom-coded frontend, would be a better entry point. I kept choosing Fillout because the client had chosen Fillout. I still think Site would not have solved their specific problem.

The Fillout PDF work that fills much of these sessions is an approach I dropped entirely once I moved PDF generation to Adobe. So read this module for what it is: a set of patterns that were correct for the tool in front of me, some of which I would not use again. The patterns transfer to other tools. The tool itself was a phase.

### Prerequisites (Modules 1 and 2)

You cannot build a form until the tables it writes into are settled. A form is just a set of writes into a schema.

- **From Module 1 (Schema Design):** the Contract → Line Item structure. The rule that a value lives at the level where it is uniquely known (the calculation on the child record, a total rolled up to the parent with a rollup, a field that adds up values from linked records). And the difference between a lookup (a live, read-only field) and a direct field (one you can write into). A form can only write into direct fields. If a destination is a lookup, the form's data has nowhere to land.
- **From Module 2 (Data Normalization):** match keys, and the rule that you link records on a stable unique identifier, never on a name a human can edit. The fan-out pattern in this module keys entirely on a submission ID. The parent/child pattern keys child records to their parent by a record ID passed in a URL. If you have not internalized "link on the ID," none of this works.

One dependency is worth naming, because it caused a rebuild on AY Media. Fields that receive Fillout data must be direct fields, not lookups. Everything coming in from Fillout into the Invoice table has to be a direct field, so the data lands in the right place.

One of those destinations turned out to be a lookup. The incoming Fillout data had nowhere to go. I had to create a separate direct field for it, and that new field no longer matched the historical record. That single mismatch, a form writing into a field that was actually a lookup, is why I deleted and rebuilt the table. Settle the schema, then build the form.

---

## Lesson 1 — Fillout parent/child forms: the contract is the parent, the line item is the child

**A multi-record submission is built as a parent form (the contract, one record) with a child form nested inside it (the product line item, one record per product added); the child form is how a user adds more than one line item to a single contract.**

### Case study — AY Media, 2026-05-08 (call 665069340)

AY Media sells magazine advertising. A single contract has many line items, one per product an advertiser buys. The question was how one Fillout submission could create one contract record plus a variable number of line-item records linked to it.

The answer is Fillout's parent/child form structure. The parent form collects the contract-level fields: advertiser, contact, contract total. A child form nested inside it collects one product line item at a time. Each time the user adds another product, the child form produces another line-item record. All of them link to the one parent contract.

By this call the client had simplified the model. They dropped a third form layer they had originally wanted for insertion orders. That left just the parent form and the child form. The parent form is the contract, the child form is the product, and each product is one line item. Cutting the third layer made the whole build much simpler.

The thing that broke, and that I spent the first twenty minutes of that call on, was the total. The parent form has to show a contract total that sums the child line items.

Trace the calculation from the top. There are two layers. The contract is the parent form, and it carries a calculation for the total of the invoice. That total adds up the line-item totals. Each line-item total is computed on its own line item.

That is the whole structure. The child form computes a line total on each line item: quantity times per-unit cost. This is Module 1's rule that the calculation lives on the child. The parent form then runs a Fillout calculation that sums those line totals into the contract total.

I used Fillout's own calculation for the sum, not an Airtable rollup. The reason is a timing fact covered in Lesson 4: the Airtable rollup is not filled in time for the PDF fill.

### Principle

A one-to-many relationship (one contract, many line items) maps to a parent form with a nested child form. The parent is the "one" and holds the total. The child is the "many," and it is how a user adds more than one of them in a single submission. Anything the parent needs to display that depends on the children, a total or a count, has to be computed inside the form or has to already exist at the time the PDF is filled.

### Where it broke / changed

Multi-layer Fillout forms write records from the bottom up, and that is a real risk. On the three-layer version of this form the problem was plain. As soon as the grandchild form is filled, it creates the grandchild record. Submit the child form and you get the child record. If a person abandons the form before submitting all the way up to the parent, you are left with records that have no parent: partial submissions sitting in the base. I call these orphan records.

So a person who fills the child form and then closes the tab leaves a line-item record with no parent contract. Two consequences followed.

First, give every level a primary field built from a concatenated formula, never a blank one. The primary field is the first field in a table, which Airtable shows as the record's name. With a formula there, an orphan record is at least readable instead of showing as "unnamed record."

Second, build an inconsistency view that finds the orphan records: created before today, parent link empty, submission ID not empty. Delete them on a schedule, because orphan records overstate any per-product sales count. That scheduled deletion is a Module 4 automation, but the reason it exists is this form behavior.

And the larger change. This parent/child form produced a Fillout-generated PDF. By April I had moved PDF generation off Fillout to the client's Adobe template, filled by API. Much of the mapping work in these calls was for an output I later abandoned. The parent/child record structure survived. The PDF integration built on top of it did not.

---

## Lesson 2 — Branch upstream, not in the tool

**Fillout generates every mapped PDF on every submission. It cannot conditionally branch its outputs. So when you need different documents for different cases, you duplicate the form once per case and select the right one with a single Airtable formula field, not with logic inside the tool.**

### Case study — Coding Clarified, 2025-08-26 (call 390509922)

Coding Clarified enrolls students in four states plus a headquarters default: Florida, Indiana, South Carolina, Texas, and HQ. Each state has its own enrollment agreement PDF. I wanted one enrollment form that would produce only the state-appropriate PDF.

Fillout cannot do that. By default it will not let you decide, based on a URL parameter or any other condition, whether a given document should be generated. The PDF integrations always run on submission. You cannot set conditional branches like "if California then fill this PDF but not the other three."

The fix moves the branch out of Fillout and into the data. You build one enrollment form per state, each with exactly one PDF integration. Then you put a single formula field in Airtable that outputs the correct form URL based on the student's state. The automation that emails the student just sends whatever that one dynamic field resolves to.

There are two ways to write the selector formula: nested IF or SWITCH. I went with SWITCH because it gives you a shorter formula. You name the field you are checking once, then say: if it contains FL do this, if it contains IN do that, and so on. It reads the field's value and outputs a result without any nested IF formulas.

The ordering rule that makes this manageable: get one form right, then duplicate. Do not duplicate first and then fix five copies. Delete the state copies. Get everything working on the headquarters original. Only then create a duplicate. Map everything correctly on that one form first, and once it works as expected, duplicate it. Otherwise you spend all your time fixing each copy.

### Principle

When a tool cannot branch its own output, do not force the branch inside the tool. Make one copy of the form per case. Resolve which copy to use once, upstream, in a formula that already knows the answer. Then let the automation carry a single dynamic value. The branch lives in exactly one place, and it lives in the layer you can read and edit.

### Where it broke / changed

I made the exact mistake this lesson warns against, and I caught it two days later. I had started building the state conditional inside the automation, keyed off base-structure field IDs. That is the wrong layer. Writing "where the field ID of some base-structure field is TX, then do something" is not the correct way to do it. The better move is to drop that logic entirely and keep only the email action. The URL is already dynamic and already captures the state.

That is the whole principle stated as a correction. The URL formula already captures the state, so the automation must not repeat the same conditional. Resolve the branch once. It belongs in the formula field, not the send step.

---

## Lesson 3 — The product-selection cascade: attributes filter down to one product

**When users refuse a flat product dropdown, model the product as the combination of its attributes and build the form as a cascade where each attribute filters the next, ending in a product link-record field with a dynamic filter that matches everything chosen above it.**

### Case study — AY Media, 2026-02-12 (call 564364653) and 2026-05-08 (call 665069340)

AY Media adds new products every couple of weeks, and the client would not accept picking a product from one long dropdown. A "product" there is really a combination: publication, ad size, ad type, ad position, frequency, issue month, issue year, special section.

So stop asking for the product at all. Ask for each attribute in order, then let a dynamic filter resolve the single matching product. This ordered set of questions, where each answer narrows the next, is what I call a cascade.

You fill out the attributes. Rather than have an automation decide which product that is afterward, you put a product link-record field at the bottom (a field that links to a record in another table). Its dynamic filter says: only show the options that match every condition chosen above. The attributes above become the filter.

I chose the dynamic filter over letting an automation guess because it is safer. The attributes are the filter, so the product cannot come out inconsistent with the choices. For this to work, each attribute has to be its own link-record table, which I call a library. That way the selections can filter each other. You set the logic in Airtable, not inside Fillout, and you build out the libraries. Either way you need the libraries for the filters to constrain one another.

By the May 8 call I had defined the exact filter order and the operator. The cascade is strict: every level filters on every level above it, using `contains`. The order is class, publication type, publication, issue year, ad size, ad type, ad position, frequency, month, special section. Then the product field filters on all of them above it. I kept `contains` as the operator across every level, because it was already working and mixing operators was part of what had broken.

The bug I was fixing when I worked this out: the picker showed no products at all. Filters were skipping intermediate levels and mixing operators. The rule that fixed it: every attribute filters on the full set above it, always `contains`, and the product field filters on all of them.

### Principle

A dependent picker is a cascade, and the logic belongs in the data model, in link-record library tables, not buried in form configuration. Each level filters on every level above it, consistently. The product is not selected. It is the only option left once every attribute has narrowed the set. That is safer than an automation deciding the product afterward, because there is no moment where the attributes and the product can disagree.

### Where it broke / changed

Two things. First, one of these attributes turned out not to be one-to-one with the sellable unit, and I had to keep it as a separate choice. When I modeled inventory as "issue slots," there was a case for saying that if ad size lived on the slot, the separate size selector was redundant. It is not, because a slot can be sold at several sizes. The relationship there is not one-to-one, so it has to stay a filtered choice. What actually is one-to-one for issue slots is the issue year, the issue month, and the ad position, and only those.

The lesson inside the lesson: an attribute only merges into the parent record if it is genuinely 1:1. Anything that can have several values stays a filtered choice in the cascade, or you undercount inventory.

Second, I later found redundant libraries. Ad Size ("half") and Ad Pages ("0.5") stored the same fact in two tables, both with duplicated rows, and that confused the cascade. Two libraries storing one fact is redundant, so I kept one. The cascade is only as correct as the libraries feeding it.

---

## Lesson 4 — Fan one submission out into many records

**A single Fillout submission that contains many rows (seven day-answers, a variable list) is sent both to Airtable and to a webhook automation; the automation waits a few seconds for the parent record to land, fetches it by matching submission ID, then creates one child record per row and links each back to the parent.**

### Case study — Coding Clarified, 2025-07-29 (call 364852797)

The weekly attendance form has one submission carrying seven day-answers: Monday attended, Tuesday attended, and so on. Each day needs to become its own record in the Attendance table. But the direct Fillout-to-Airtable integration writes one field per question into a single record. It cannot turn one submission into seven records in a different table.

The pattern sends the submission down two paths at once. Path one is the normal Fillout-to-Airtable integration. It creates one Form Submissions record carrying a submission ID that Fillout itself generates. Path two is a webhook that triggers an Airtable automation. A webhook is a message the form sends to trigger the automation. The automation waits about five seconds, so the Form Submissions record is guaranteed to exist, then finds it by submission ID and creates the per-day records against it.

The wait is deliberate. Two integrations run at once. One sends the answers to the Form Submissions table along with a submission ID. The webhook fires in parallel. Waiting five seconds makes sure the Fillout-to-Airtable integration has finished, so a new Form Submissions record exists with its submission ID. Only then does the automation look up the form submission where the submission ID equals the submission ID from the webhook call. It searches on that submission ID, links each new record to the matching form submission, and creates one record per day.

The whole thing keys on the submission ID. That ID is the stable unique identifier that ties the resulting child records back to the one parent submission. This is Module 2's "link on the ID," applied to an event instead of an entity.

There is a companion technique that makes the reverse case work: one shared form that has to know who is submitting. Each order's tracking-form link carries the student's record ID as a URL parameter. The form has a hidden field that reads that parameter as its default value, so the submission attaches to the right student without asking. You set up the URL parameter in the form settings under URL parameters, add a new one, then tell the hidden field to prefill with the value found in the URL parameter called student record ID.

### Principle

To turn one submission into many linked records, do not look for a built-in form feature that does it. There usually is not one. Send the submission to Airtable and to a webhook automation in parallel. Key the automation on the submission ID. Give it a short wait, so the parent record lands before the automation goes looking for it. One submission, one parent record, N child records, all tied together by an ID the form tool generated for you.

### Where it broke / changed

The reason this has to be a webhook automation, and not one scheduled automation, is a hard Airtable limit. Airtable does not let you use both a repeating group and conditional logic in the same automation. If it did, I could handle every tracking-form case in one automation. Because it does not, you need multiple automations.

You cannot loop over found records and branch per record in the same Airtable automation. That single constraint shapes a lot of the automation architecture in Module 4. It is why the fan-out lives in its own webhook-triggered automation, rather than folding into the weekly send.

The pattern worked well. It is one of the few from this era I would build the same way again. The only weak point is the five-second wait, which is a timing assumption, not a guarantee. If the Fillout-to-Airtable write is ever slower than the wait, the search finds nothing. On a higher-volume build I would key the create step off the record's own arrival, rather than a fixed wait.

---

## Lesson 5 — Update form versus create form

**An edit to an existing record is a different job from creating one, so you build a separate update form (often a single field), turn off Fillout's native edit-link email, and send your own email carrying the update form's dynamic URL, so you control who gets it and which form they land on.**

### Case study — AY Media, 2026-06-08 (call 700311737) and 2026-05-22 (call 682399168)

Two needs on AY Media were both edits, not creations, and both wanted their own small form.

The first: after a sales rep downloads a contract, sends it for signature, and gets it back signed, that signed file has to land back on the right record. That is a one-field update, and it should stay one field. It is an update-record form, just one field. Any larger version adds complexity the job does not need.

The second: the manager-approval loop. A rep submits a contract with a proposed total flagged for review. The manager needs to open an update form, not a create form, to approve, reject, or send back one revision.

Fillout has a built-in "send them a link to edit the submission" email. But that URL is opaque, and you cannot control where it goes. So I turned it off and rebuilt the notification myself. In the old workflow, the form was submitted and Fillout sent its own email for the recipient to update the form submission. Once I turned that off, I had to rebuild it on my side. Rather than rely on the opaque URL Fillout was sending, I send an email myself using the dynamic value.

Sending the email myself means I choose the recipient (the manager, not the submitter), I choose the form (the update form), and I control the URL. That is also where the manager reprint button lives. A generated PDF is static, so an approved change to the total does nothing to the already-generated document until someone re-submits the update form to regenerate it. A PDF is fixed once created. It still shows the old contract total, so someone has to go into the form and regenerate or resubmit. Because this is an update form, that is just a few clicks and a submit, which re-triggers the integration and generates a fresh document. On the June 8 call I confirmed it worked: the record was regenerated with the new version of the PDF.

The reprint button is just a button field that opens the update form URL for that record. The manager clicks it, the update form re-submits, the PDF integration runs again, and a fresh PDF replaces the old one.

### Principle

Creating and editing are different jobs and deserve different forms. A create form makes a record. An update form changes an existing one, and it should be exactly as big as the change: one field for a file, one field for a revised total. When a vendor's built-in edit notification is opaque, replace it with your own automation, so you control the recipient, the routing, and the URL. And remember that any rendered document is fixed at the moment it is created. Changing the underlying data changes nothing until you render it again, which is why the update form doubles as the reprint mechanism.

### Where it broke / changed

The update mechanism is a call I reconsidered, because I was answering two slightly different questions at once. One framing said the edit needs a Fillout update form, or Site, because sales reps do not have Airtable edit permissions. But a plain button can update a field without any edit rights. People can click a button without having editing access. So why not just a button that updates the Airtable field directly?

Both framings are right, and the real distinction is what the edit touches. For changing a status, a button is enough. For a rep editing the actual content of their own submission, they need a form. Which one you build depends on whether the edit is one value or many. The split I shipped reflects exactly that: a button for the reprint (one action), an update form for the manager's content edits (several fields).

### Coda — the date Fillout could not compute

One more edit-shaped problem from Coding Clarified, because it is the clearest example of the discipline in this whole module. The enrollment agreement had to show an estimated end date equal to the start date plus 120 days. Fillout cannot do date arithmetic to a calendar date. Its calculation only returns a duration. It can do a date-time difference, which tells you the gap between two dates is 120 days, but it cannot set an exact calendar date.

I spent real effort building delays and lookups so the emailed PDF would show a filled-in end date. Then I realized the requirement did not need a computed date at all. The agreement can simply state the rule: the start date is such-and-such, and the end date is 120 days after the start date, with no specific calendar date named. Restating the requirement as text removed the computation, the dependency, and the delay at once. It was the simpler answer, and once I saw it, the obvious one.

Before automating a hard calculation, ask whether the requirement can be restated so the calculation is not needed. Printing "120 days after start date" as text removes the computation, the dependency, and the delay at once. If the tool cannot do the thing, sometimes the answer is not a workaround. It is a smaller requirement.

---

## What I'd do differently now

**I would settle whether Fillout is even the right entry point before building a single form.** For months I built one Fillout workaround on top of another: the state-branch problem, the static PDF, the opaque edit URL, the orphan records, the no-dynamic-line-items limit, the date it could not compute. The case for moving off Fillout kept getting stronger. Even when a code-based frontend looks like more work to start, as soon as things get complicated, which they always do, being able to change code directly is usually easier from that point on. By June I agreed with that for the next client.

But I want to be precise about where I was right to stay on Fillout, because "just use Site" is too broad a rule. The AY Media build genuinely needed a dashboard, and Site would not have delivered that. Site would not have helped me avoid any of this, given that the client also wanted a dashboard. If they had not wanted a dashboard, and only wanted the "do not allow me to select something already sold" behavior, that part could have been built with Site. But the dashboard requirement ruled it out.

And the reason I kept choosing Fillout at all was not stubbornness. The client had chosen it, and at the time I had to go with what they were telling me.

So what would I actually change? I would run the tool decision as its own explicit step at the start. I would weigh the real requirements (dashboard? per-record editing? dynamic documents? client maintaining it without me?) against each tool's known limits, and I would put that decision in writing before building forms. The frontend is a handoff decision, not just a question of build power. My own concern about custom code was exactly ownership: I build things for myself on Vercel, but my clients cannot maintain that.

**I would stop building Fillout PDFs before I understood the PDF was going elsewhere.** A large share of these sessions was Fillout-PDF mapping that I abandoned when PDF generation moved to Adobe, filled by API. By April I was no longer creating the PDF in Fillout, which made a lot of that mapping work pointless. The record structures (parent/child, cascade, fan-out) all survived that switch. The PDF integration built on top of them did not. The lesson: separate the durable part of a workflow (how records are shaped and linked) from the disposable part (which tool renders the document). Do not over-invest in the disposable part before it is locked.

**I would replace the fixed five-second wait in the fan-out with something that keys off the record actually arriving.** It worked at Coding Clarified's volume. It is a timing assumption, and timing assumptions are the bugs you find at the worst moment.

---

## Exercises

1. **Build the parent/child pair.** In a scratch base, model one Order (parent) with many Line Items (child). Build a Fillout form where the parent form collects the order-level fields and a nested child form adds one line item at a time. Compute a line total on each child (quantity times unit price) and a sum on the parent using Fillout's own calculation, not an Airtable rollup. Now abandon the form after adding one child and before submitting the parent. Find the orphan line item. Write the three-condition inconsistency view (created before today, parent link empty, submission ID not empty) that would catch it.

2. **Branch upstream.** Take a form that must produce one of three different outputs by category. Instead of putting the branch in the form, build three copies of the form, then write a single SWITCH formula field that outputs the correct form URL by category. Confirm that your send automation references only that one field and contains no category logic of its own. Then deliberately add the branch to the automation as well, and delete it, to feel why the duplicated logic is the wrong layer.

3. **Cascade a product out of its attributes.** Model a product as three attribute libraries (each its own link-record table). Build a Fillout picker that asks for each attribute in order, then a product link-record field whose dynamic filter matches all three attributes above it, using `contains`. Verify the product field shows exactly one option once all three attributes are chosen, and shows none when the filters skip a level. Then check each attribute: is it genuinely 1:1 with the product, or does it need to stay a filtered choice? Justify each answer.
