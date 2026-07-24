# Module 4 — Automation Architecture

*Rachael Quisel · Systems Thinking for Airtable*

---

## Frame

Automation is where most of my early mistakes did real damage. A schema mistake just sits there. I can find it and fix it before it ever runs. An automation mistake is different. It emails the wrong student. It links an order to the wrong person. It overwrites a field that took me three hours to correct. It sends 100 identical messages to 100 addresses because I mapped the wrong token. An automation mistake reaches more records than a schema mistake, and it reaches them faster.

So this module is not about how to build a Zap (an automation built in Zapier). It is about the few decisions that decide whether an automation does exactly what you meant and nothing else. Four of them came up in almost every build I did:

1. When you write into a table, do you know whether you are creating a new row or updating an existing one, and are you sure?
2. When you write a link between two tables, are you writing it from the side that holds one value, or the side that holds many?
3. When you collapse many child rows into one value an automation reads, are you filtering to the eligible rows before you sort, or after?
4. When part of the flow lives in a tool you can't see into, do you actually know why it failed?

I got every one of these wrong at least once, in a recorded session. The patterns below are what I use now so I don't get them wrong again.

I built these on two production systems. The first was the Client A medical-coding platform, which ran on WooCommerce, Airtable, Fillout, and Zapier, and tracked students, orders, and progress trackers. The second, later, was an n8n pipeline that parsed PDFs into Monday.com and Airtable. The tools change. The four questions do not.

---

## Prerequisites

This module assumes Module 3 (Workflow Building). The order matters, and I hold to it in practice. Build the pipeline by hand first. Watch it work once, end to end. Only then automate the parts that repeat.

The reason is not discipline for its own sake. If you build an automation before you understand the manual flow, the automation encodes your misunderstanding and then runs it on a schedule. When I searched the Orders table instead of the Students table, or trusted a "find or create" action not to update, those were manual-flow misunderstandings. I had already built them into a Zap before I noticed them. Doing the steps by hand once would have shown me the gap before it was running against real customer data.

So: model the thing (Module 1), normalize the data (Module 2), run the workflow by hand (Module 3), and automate only the repeating parts (this module). If you skipped ahead, the case studies below will still make sense. But the corrections will read as avoidable, because they were.

---

## Lesson 1 — Search-or-create on a unique key, with two explicit branches

**The pattern:** Before you write into a table, search it by a unique key. If you find a row, update or link it. If you don't, create one. And when your tool's built-in "find or create" action can't be told to stop updating, replace it with two branches you control: one for found, one for not-found.

### Case study — 2025-07-30, the WooCommerce zap

Every WooCommerce purchase at Client A was adding a new row, which produced duplicate students. The fix was a two-table model (Students, one row per person; Orders, one row per purchase) and a Zap that searched before it wrote. The unique key was the AAPC number, the one identifier a student typed at purchase.

Here is how the Zap works, start to finish. A student makes a purchase in WooCommerce. That order triggers a search for the student. I search the Orders table by the AAPC field, because that is the unique identifier coming from WooCommerce.

The architectural point sits underneath that description, and it is worth naming carefully. This action is a find, not an upsert. An upsert says "if it exists, update it." A find just locates the row and hands it back without touching it. That distinction is the whole lesson. The day before, on 2025-07-29, I had already settled why we could not just use Zapier's find-or-create and trust it. The client did not want student data overwritten on repeat purchases, and find-or-create updates silently. So I split the logic into two paths, one for when the student exists and one for when the student does not. If the student exists, skip the create.

The full flow reads like this. Search Students. If the student exists, link the order to that student and stop. If the student does not exist, create a new student, create the order, and link the order to the student. The order record is always created. The student record is searched, then branched. Found means link only. Not-found means create.

### Principle

The unique key is the part that decides everything. Search on it, then be explicit about what happens on each side of the match. Do not let a convenience action ("find or create," "upsert") make the found-case decision for you when that decision has consequences you care about. Those actions default to updating, and updating is a write you did not ask for.

### Where it broke or changed

Two things.

First, the search failed silently at first, because the key was stored wrong. AAPC numbers had leading zeros that mattered, and the field was a number type, so the zero was dropped. The exact-match search then found nobody. When I typed the AAPC number into the number field, it deleted the first zero, so the value I searched for was not the value stored.

The fix belongs to Module 2. It was a length-based formula that rebuilds the zeros, then a single-line-text field to lock the value in place. But it is worth naming here, because a search-or-create is only as good as the key. A key stored in the wrong type is not unique anymore. An identifier with leading zeros is text, not a number.

Second, there is the question of which table to search, and this is a call I reconsidered rather than settled. On data-modeling grounds, AAPC is a student attribute, so "does this exist?" should query the Students table. An AAPC number at the order level can never exist unless that same AAPC exists at the student level. That is the structured way to think about it. I kept the search on the Orders table for the working build, because in the WooCommerce-only setup, a student only ever entered the system through an order. I shipped the simpler version and flagged the Students-table search as the thing to revisit later. If a CSV of AAPC numbers with no orders had ever arrived, the Orders-table version would have needed to change and the Students-table version would not. That is exactly the kind of decision worth writing down as deferred. The deferral only holds while the assumption behind it stays true, and the assumption here is that every student arrives through an order.

---

## Lesson 2 — Write the link from the one-side, never the many-side

**The pattern:** When you connect a one-to-many relationship in an automation, write the link from the many-side record (the order), which holds exactly one value. Do not write it from the one-side record (the student), which holds a set. A single write to that link field replaces the whole set.

### Case study — 2025-07-29, linking orders to students

My first plan was to create the order, then update the student record to point at that order. That is the wrong direction. Here is the reasoning that turned me around.

Say I write the link from the student's side, and the student already has orders. When I write the one new order into the student's link field, I overwrite the orders that student already had. I would be writing a single order into a link field that used to hold one or several. A single write to that field replaces everything in it.

Go the other way instead. First create (or find) the student. Then, at the order level, link the student. That always gives exactly one link at the order level, because an order links to only one student. A student can link to many orders, but I never write from the student, so I never overwrite that set.

That is the point where the pattern became obvious to me, and it stuck. I have not written a link from the many-value side since.

### Principle

Write a link from the side that holds one value. The order has one student, so write the student onto the order. The student has many orders, so writing an order onto the student replaces the set. This is true in every tool that models one-to-many with a single link field, which is all of them. The direction of the write is not a style choice. One direction preserves the existing data and the other destroys it.

### Where it broke or changed

This one held for the entire eleven months. The only refinement was the fallback key. Some students had no AAPC number, so I linked on the Airtable record ID where the business key was missing, because the record ID always exists. The link direction never changed, because it was correct the first time. That is rare enough that it is worth saying plainly.

---

## Lesson 3 — Filter before you sort, then take the last

**The pattern:** When you collapse a one-to-many into a single current value that an automation reads, filter to the eligible rows first, then sort, then take the last. If you sort first and filter after, an ineligible row can become the selected value.

### Case study — 2025-08-28, the active tracker

A Client A student can hold several active orders at once. The weekly send automation finds students, not orders, so each student needs exactly one current tracker even when they have multiple purchases. Two weeks earlier, on 2025-08-12, I had described the collapse: keep only the active orders, sort them by order date earliest to latest, take the last one, and show its tracker on the student. That gives each student one active tracker even when they hold multiple active orders.

The refinement on 2025-08-28 is the part I want to teach, because it is the difference between "usually right" and "always right." Students buy products that have no tracker at all, for example a practice exam. If I just took the most recent purchase, a later exam purchase would become the student's "latest" and push them onto a blank or wrong tracker. The correction was about order of operations. First, the system filters out any records where the product is not a tracker product. Then, from the records that remain, it sorts. Then it takes the last one. The filtering happens before the sorting.

So: filter out the non-tracker products first. Then sort what remains by date. Then take the last. A later unrelated purchase can no longer become the selected value, because it was removed before the sort ran.

There is a platform reason the trackers were split across several automations in the first place. It is worth knowing, because it looks like a mistake until you understand it. Airtable cannot combine a repeating group with conditional logic in one automation. If it could, I would use one automation to handle every tracking-form automation, looping over every active student and branching per tracker. Because Airtable cannot do that, I split into one automation per tracker instead.

Know your platform's hard limits. This one shaped the whole tracker architecture, and no amount of cleverness gets around it.

### Principle

Inside a lookup or rollup, the order of operations decides the answer. (A rollup is a field that combines values from linked records, for example the latest date or a running total.) Filter to the eligible set first, then sort or limit. An ineligible record must never be present when you ask for the "latest," because "latest" does not know it is ineligible. This applies to any "current value out of a history" question: current status, latest eligible payment, most recent qualifying event. Filter first, always.

### Where it broke or changed — the active-order date logic

This is the sharpest reversal in the whole course, and it is mine. It was an approach I built and then dropped.

Across two full sessions, 2025-08-19 and 2025-08-26, I built and insisted on a date-based "active order" model. Each order would carry its own start date and expected end date, and an order counted as active when today fell between them. I argued for it firmly. Each order should have its own start date, not a start date derived from some student-level date I picked. Order one for product one might have its own start and end date and be active, and each order has unique start and end dates. On the data-modeling logic, that is correct.

Then I reconsidered, and the reservation that won was about the data, not the model. These dates were discretionary and unpredictable. I did not trust them to decide anything as consequential as which tracker a student received. Basing the tracker on them would cause more problems than it solved.

By 2025-08-28 I scrapped the date-based active-order approach entirely. I based the tracker purely on the most recent tracker-eligible product, which is the filter-before-sort logic above, and I deleted the `active order` field. Before deleting it, I checked its dependencies, confirmed nothing relied on it, and removed it. The one nearby name that was still in use was the ActiveTracker field, which is a different thing and stayed.

I was glad to get rid of it. The point is not that the date model was careless. It was the opposite. It was a defensible design, defended across two calls, and abandoned the moment the simpler product-based logic proved it was carrying complexity for no gain. "I built it and argued for it" is not a reason to keep something. The active-order date field existed for about a week and was correctly deleted. If an approach I built and defended can be reversed this simply, so can yours.

---

## Lesson 4 — Keep the whole flow in one place you can debug

**The pattern:** When part of an automation runs in a tool you can't see into, that is the part you can't fix. Keep the whole workflow inside one platform when you can, so you can trace the data step by step and find where it went wrong.

### Case study — 2025-09-18, moving the PDF parser off Replit

By this point I had built a pipeline that parsed PDFs and pushed the results into Monday.com. The parser itself ran on Replit, in Python, outside the n8n workflow. When items and sub-items started going missing, nobody could tell why, because the logic that produced them lived somewhere the rest of the team could not inspect. That is the problem stated plainly. It is very hard to debug a system when you cannot see what it is doing, and anything you can do in Python or Replit you can also do inside n8n.

The move was to replace the external parser with n8n's own nodes (the individual steps of an n8n workflow), so the flow was one continuous, inspectable thing. With the whole thing inside n8n, I did not have to go into Replit at all.

The debugging method that comes with this is the reason it matters. When the flow lives in one place, you can read the item count each node emits and find the first node where the output is already wrong. The trigger says one item. The download says one item. The HTTP node should emit the parsed items, and it should be emitting everything the run needs. If the HTTP node's output is already incomplete, the problem is upstream in the code, not in n8n. You cannot run that trace across a boundary into an external service you can't see into.

The same session produced a related move. n8n's built-in Monday.com node could not handle sub-items. Rather than work around that node's limits, I used a raw HTTP Request node to call Monday's API directly. The built-in Monday node does not behave the way you would expect, but you can do what you need in Monday using an HTTP request, and it is straightforward.

A prebuilt integration node is a convenience, not a limit. When it can't express what you need, use the raw API call. And notice that the API call still lives inside the same workflow you can trace.

### Principle

Every tool you add that you cannot inspect is a part of the flow you cannot debug. Keep the workflow inside one platform when you can, so the whole path is visible and you can trace a failure to a single node. When a native node is too limited, reach for the raw API from inside the same platform rather than setting up a separate service outside it.

### Where it broke or changed

The Replit-in-the-pipeline design was mine, and I did not want it there either. I had been forced into it. I really did not want to bring Replit in, but I had no other way of running the parser at the time.

I had also moved the whole build back and forth between platforms more than once before landing, from Zapier to n8n to Zapier to n8n. That back-and-forth was a symptom of not having decided, early, that the flow should live in one place I could debug. Once I committed to n8n as the single place for the pipeline, the "where did the sub-items go" question became answerable, because there was a node to point at.

---

## Lesson 5 — Use AI to parse messy input, not regex

**The pattern:** When the input format is outside your control, do not try to defend regex against every variation. (Regex is a pattern that matches an exact sequence of characters.) Extract the text, feed it to an AI node, and have it output a fixed JSON shape. (JSON is a structured data format the next step can read.) You stop caring about the input format and only care about the output.

### Case study — 2025-10-14, parsing the LMN PDFs

The client's crews kept formatting their PDFs differently, and every new format broke the regex parser I had written in a code node. I was editing the parser for each new variation. That is an endless, low-value task, because the formatting was never going to be consistent. I had already said so on 2025-10-03. I was not going to edit the parser for every single thing.

By 2025-10-14 the better approach was clear. Parse the document with AI, so I could focus on the rest of the workflow instead of constantly editing the parser for a format that did not depend on me.

The mechanism is simple, and it is why the approach generalizes. Extract the PDF text, push that text into an OpenAI node, and get back a JSON I can map into Monday. Rather than giving the text to a code node that runs regex to pull the data points, I push the text into an OpenAI node. Then, whatever the format, the format stops mattering. OpenAI outputs a JSON I can then use to put the data into Monday. I had already been using the same approach for other documents. Earlier that same day I was parsing bank statements and credit card statements, where a Bank of America extract and a Mercury extract both run through the same flexible node.

The same node reads a Bank of America statement and a Mercury statement without a separate parser for each, because it is reading meaning, not matching a fixed character pattern.

### Principle

When you do not control the input format, regex commits you to something you cannot deliver. It commits you to listing every variation the source will keep inventing. AI parsing to a fixed JSON output puts the stable, predictable shape on the output side, which you do control. This applies to any varied-input problem: statements, invoices, resumes, forms filled by people who will never follow your template.

### Where it broke or changed

This was a documented reversal across meetings, not a one-time choice. From 2025-09-23 through 2025-10-03, the whole n8n build extracted text and used regex in a code node, and I insisted that the client simply had to format the PDFs consistently. By 2025-10-14 I had changed to AI-to-JSON parsing, precisely because the client was never going to format consistently. The thing I had been treating as a client-discipline problem was actually a tooling-choice problem. Once I stopped requiring the input to be regular and let the AI absorb the irregularity, I no longer had to edit the parser for each new format.

There is one constraint to carry with this. Airtable's own AI fields only read PDFs, not images. So if the attachment is an image, you convert it to a PDF first (I used PDF.co for that) before the AI field can read it. Know the format your AI tooling accepts, and normalize to it.

---

## What I'd do differently now

Looking back across these sessions, the corrections cluster into a handful of habits I did not have at the start and do now.

I would build the explicit two-branch search from the first day, instead of trusting a "find or create" action not to update. Every time I trusted the convenience action, it did a write I did not ask for, and I found out later.

I would never store an identifier as a number. AAPC numbers with leading zeros cost me a whole failed search before I understood that a leading-zero identifier is text. Any value where the zero carries meaning is text, and I treat it that way from the moment I create the field.

I would write links from the one-value side by reflex, without having to stop and reason it out. Understanding the direction of the write, that an order holds one student and a student holds many orders, was the moment it became automatic for me. I would give that to myself sooner.

I would resist building date-based "active" logic when the dates are discretionary. I spent two sessions on an active-order date model that I deleted a week later. The simpler product-based logic was there the whole time. When a stakeholder cannot tell me a date will be entered reliably, I do not let that date decide anything downstream.

I would decide early that the whole flow lives in one platform I can debug, instead of adding Replit under pressure and then pulling it back out after the sub-items went missing. And I would reach for AI-to-JSON parsing before writing the first line of regex against a document I do not control, instead of after the third format broke my parser.

None of these are advanced. They are the difference between an automation that does what I meant and one that does something next to what I meant, quietly, at scale.

---

## Exercises

**1. Build a search-or-create with two explicit branches, and break the key on purpose.**
On a base of your own, build an automation that searches a table by a unique key, links on found, and creates on not-found, as two separate branches rather than a single find-or-create action. Then give one test record an identifier with a leading zero (for example `007042`) stored as a number field, and confirm the search fails to find it. Convert the field to text, rebuild the value, and confirm the search now matches. You want to feel the failure, not just read about it.

**2. Collapse a one-to-many with filter-then-sort-then-last, and prove the order matters.**
Take any parent-child relationship where the parent needs one "current" value out of many child rows (latest qualifying order, most recent eligible submission). Build the lookup two ways: sort-then-take-last with no filter, and filter-then-sort-then-take-last. Add a child row that should be ineligible and is more recent than the eligible ones. Confirm the first version selects the wrong row and the second does not.

**3. Replace a regex parse with an AI-to-JSON parse on input you do not control.**
Find a document type your client produces inconsistently (an invoice, a statement, a form). Write a regex parser for the format you have, then feed it two more real examples with different formatting and watch it break. Rebuild the parse as extract-text into an AI node that outputs a fixed JSON shape, and run all three examples through it. Compare the effort of maintaining each as the fourth format arrives.
