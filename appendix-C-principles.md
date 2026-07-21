# Appendix C — Principles Worth Keeping

The lines I come back to, one per idea, grouped by the discipline they belong to. Each one is worked through with a real case study in its module. This is the short version, the thing to remember when you are deep in a base and trying to decide.

## Schema design

- Whenever I have a one-to-one relationship, I assume there is something there. Two tables that always map one row to one row are usually the same table twice.
- Store each value at the level where it is actually true. A line total lives on the line item, not the contract. A customer ID lives on the customer, not on every contact.
- An attribute lives at the level where it is first uniquely known.
- Model a product as a set of attributes that filter each other, not as one flat dropdown. The product is the last thing left once every attribute has narrowed the set.
- Give every record a real name with a primary-field formula. "Unnamed record" is a bug, not a cosmetic issue.

## Data normalization

- Make the match key a formula, so pasting values into a link field can only link to existing rows and can never create new ones.
- If you will still have to search by the email address later, then the email is the key. Don't pick a key you won't actually use.
- Rebuild a broken key on purpose, don't eyeball it. A number field that strips leading zeros gets them back with a padding formula, then you stamp the result as text so lookups match.
- To move a value off a linked table and onto the record itself: create the lookup, change the field type to text, then delete the link. Copy it down, then cut the link.

## Workflow building

- When the tool can't branch, move the decision earlier. If a form generates every mapped PDF on submission, don't fight it. Duplicate the form and use a single formula field to choose which one runs.
- Turn one submission into many records with a webhook that waits, fetches the parent by submission ID, then creates and links the children.
- A create form and an update form are different tools. Don't make one do both.

## Automation architecture

- Write the link from the one-side, never the many-side. Link the order to the student, not the student to the order, or you overwrite the student's whole set of orders.
- Search on a unique key, then update if found and create if not. The key is the part that matters most.
- Filter before you sort, then take the last. A later unrelated purchase should never be able to take over the active record.
- Keep the whole flow in one place you can debug. Use AI to parse messy input instead of brittle regex.

## PDF and document generation

- A generated PDF is frozen by definition. Changed data does not update it. Someone has to resubmit the form to make a new one. Design around that fact, don't be surprised by it.
- Map the PDF to a rollup, not a lookup, when the value needs to be unique or stable. A lookup will happily print the same ID three times.

## Interface and access design

- Airtable caps interfaces at 50 pages each and 50 interfaces per base. If you need one page per person for hundreds of people, the answer is one page that filters to the logged-in user, not hundreds of pages.
- A public page share and a read-only base share expose different things. Choose on purpose.
- The frontend choice is a maintainability decision, not a taste decision. I build custom things for myself, but a client has to be able to keep it running after I'm gone.

## Project management

- Model a task as its own record, pulled from a template, linked to the thing it belongs to. Not a single-select option, not one field per task. That is what lets you add a one-off task or automate one without changing the schema.
- To measure how long something sat in each stage, write a new record on every status change. The history is the rows.
- Add a junction table at the exact moment a relationship becomes many-to-many, and not one moment before.

## Client communication

- "The client is always right" and "the client's reason is a good one" are two different sentences. Build what they asked for, and know which of their reasons actually hold.
- You can rename an interface page anything you want while the backend stays one table. Most "we need a separate table for this" requests are really "we need a separate view."
- Look before you touch. On a base someone built with you, look first, write down your thoughts, and change nothing until you both understand what is there.
- Let the form carry one revision, then move to a phone call. The form is not where the negotiation happens.
- Settle table ownership in writing before a shared build starts, not five months in. The most expensive thing in a shared build is an ownership boundary nobody wrote down.
- Say the cost out loud, in plain numbers, early. "This base has two editors, that is why it is slow, here is what it takes to make it yours to keep." Said early, it resets expectations. Said never, it turns into a missed date nobody understands.
