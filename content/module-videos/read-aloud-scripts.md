## Module 1: Schema Design in Airtable

On a magazine advertising build, I got three table decisions wrong. A contract total read zero. A QuickBooks customer ID printed three times on one contract. About fourteen thousand duplicate rows appeared.

None of those were automation bugs. They were decisions about my tables and links. I made them too early and had to take them back.

Every value has one level where it is actually true.

The line total belongs on the line item, with the quantity and unit cost. The contract adds up the line totals.

The QuickBooks customer ID belongs on the advertiser. QuickBooks assigns it to the customer, not each contact.

A value one level too high cannot be calculated. A value one level too low creates duplicates.

My second table matched the first, record for record. It held the duplicates. Nothing required it. So I deleted it.

Now I draw the whole model on one screen first. I mark where each value first has one answer. This is module one of Systems Thinking for Airtable.

## Module 2: Data Normalization

Every match between orders and students failed. Two missing zeros caused it.

On an education build, I matched WooCommerce orders to students by AAPC number. That eight-digit identifier can start with zeros.

It was stored in a number field. Number fields drop leading zeros. So <EXAMPLE_AAPC_NUMBER, read digit by digit> became six digits.

A formula fixed it. It counts the digits and adds zeros to the front until there are eight. I copied the results into a single line text field. The match now runs on that fixed text.

That build also split one data feed into two tables. Students has one record per person. Orders has one record per purchase. Each import updates the student and creates a new order.

Now I pick the unique key first. A unique key belongs to only one record. I confirm it is in the source file. I store identifiers as text from the first day. Number fields are for math.

This is module two of Systems Thinking for Airtable.

## Module 3: Workflow Building

My form tool could not make a decision. So I moved the decision to an earlier step.

On an education build, the enrollment agreement differs by state. There were versions for Florida, Indiana, South Carolina, Texas, and a headquarters default.

Fillout, the form tool, creates every PDF set up on a form at each submission. It cannot choose just one.

So I made one copy of the form per state. One Airtable formula field uses the SWITCH function to return the right form link for each student's state.

The email automation reads that one field. No other step checks the state.

I build each process by hand first and watch it work from start to finish. Then I automate the steps that repeat. I learn what each tool cannot do. Then I move that step to a tool that can.

This is module three of Systems Thinking for Airtable.

## Module 4: Automation Architecture

One automation step can remove every order linked to a student.

I can fix a table mistake before it runs. An automation mistake reaches more records. It also reaches them faster.

On a WooCommerce to Airtable build, I first planned to create the order. Then I would point the student at it.

A link field connects records across tables. A student's link field holds a set of orders. Writing one order into it replaces the whole set.

Now the automation finds or creates the student by a unique key. Only one record has that key. Then it writes the student onto the order. An order has only one student. So nothing gets replaced.

That pattern held for all eleven months.

I ask four questions on every automation. Am I creating or updating? Am I sure? Which side holds one value? Did I filter before I sorted? If a step runs where I cannot see it, do I know why it failed?

This is module four of Systems Thinking for Airtable.

## Module 5: PDF & Document Generation

A contract PDF printed the same customer ID three times.

The document was not broken. It showed a shortcut I had taken in the tables.

The PDF read a lookup. A lookup pulls a value from each linked record. The advertiser had three linked contacts. So the lookup returned the ID three times.

The quick fix is a rollup that uses ARRAYUNIQUE. A rollup combines values from linked records. ARRAYUNIQUE keeps one copy of each value. I also send names to the PDF, not Airtable's internal record codes.

The real fix was in the tables. The QuickBooks customer ID belongs on the advertiser, not on each contact.

A generated PDF does not change after it is created. Changing the data in Airtable leaves the document the same. Someone has to submit the form again to get a new PDF.

So I plan for that second submission.

This is module five of Systems Thinking for Airtable.

## Module 6: Interface & Access Design

I needed one page for each of one hundred forty-eight caseworkers. Airtable does not allow that many.

An interface is a custom screen on top of an Airtable base. One interface can have up to fifty pages. One base can have up to fifty interfaces.

The built-in answer is one page with a filter. It shows records where the caseworker email matches the logged-in user's email. One page then works for every caseworker.

That filter needs each viewer to have a paid Airtable account.

A public page with a manual filter would expose other students' records. HIPAA, the United States health privacy law, ended that plan.

One filtered page works well for a small internal team. A large group without Airtable logins needs a portal outside Airtable.

The front end is the screen people use. A more capable front end is harder for the client to maintain after I leave. I treat that handoff as a real constraint.

This is module six of Systems Thinking for Airtable.

## Module 7: Project Management for Solo Consultants

A one-off task should not need a new field. If it does, the tasks are set up wrong.

On a magazine build, I first stored the production stages as status fields. The stages were written, photographed, designed, and laid out.

Then a one-off task came up. The only place to put it was a new field.

Now each task is its own record in a Tasks table. Each task links to its project. Each task has its own status, date, and owner.

A Template Tasks table holds the standard list. When someone creates a project, an automation goes through the template tasks. It creates one linked task for each one, set to Pending.

To see how long a task stayed in one stage, I create a new record at every status change. Those records are the history.

This full setup was more than one of my two clients needed. Now I build only what the client will actually ask about.

This is module seven of Systems Thinking for Airtable.

## Module 8: Client Communication

"The client is always right" and "the client's reason is a good one" are two different statements.

On a magazine build, every line item created exactly one insertion order. So the Insertion Order table had about fourteen thousand records. Those records held only lookup fields. A lookup field pulls a value from a linked record.

Staff gave one reason to keep that table. They did not want to see the words line item on screen.

That reason is a preference, not a constraint. Renaming a page costs nothing. An extra table has a cost. So I rename the interface page and hide the fields.

I defended keeping that table for two calls. Then I said it plainly. Every line item is already an insertion order.

Now I sort every reason on the first call. Each is a constraint or a preference. I sort out loud. Then the client can correct me. I also state the cost in plain numbers early.

This is module eight of Systems Thinking for Airtable.
