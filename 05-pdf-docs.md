# Module 5 — PDF & Document Generation

*From "Systems Thinking for Airtable." Built from the Client A and Client B work, July 2025 – June 2026.*

---

## Frame

Every operational system I built eventually had to hand a person a document. A student's enrollment agreement. An advertiser's contract. An insertion order a designer works from. The database is where the true values live. The document is what the client signs, files, and argues about. So the document has to be right, and it has to stay right after the data underneath it changes.

That last part is what this whole module is about. A generated document holds the values that existed at the one moment it was generated. The database keeps changing after that. The generated document does not. Almost every hard lesson here comes from that one gap. The PDF said one number, the base said another, and someone had to decide which was true and how to make them agree again.

I spent months inside Fillout's PDF integration on two different clients before I understood how narrow its real capability is. Fillout is a form-building tool. It can write values into a template when a form is submitted. It cannot recompute. It cannot branch its outputs. It cannot render a variable number of line items. It cannot read a linked record. Each of those limits cost me a real debugging session before it became a design rule. This module is those rules, in the order I learned to respect them.

Here is the honest ending, stated up front so you read the rest correctly. On Client B, the entire Fillout-generated-PDF approach was abandoned. By April 2026 I stopped generating the contract PDF in Fillout at all. I moved to filling the client's own Adobe PDF by API. A lot of the mapping work in the middle of this module was for an approach I later dropped. I kept the lessons anyway. The reasons the approach failed are the reasons you design documents the way you do, whatever tool renders them.

## Prerequisites

Read Modules 1 and 2 first, then Module 3.

- **Module 1 (Schema Design)** and **Module 2 (Data Normalization)** come first because a PDF template reads fields, and the fields worth mapping are almost never the raw ones. They are rollups, formula fields, and coalesced override fields that only exist once the model has settled. A rollup is a field that combines values from linked records. In this module I map a rollup with `ARRAYUNIQUE` (a function that returns only the distinct values) for a QuickBooks ID. I map a `resulting = custom if not blank else computed` override field for a contract total. And I map a concatenated formula field that imitates a structured line. None of those fields make sense until you have read how the Contract → Line Item structure is built and where each attribute belongs. If you map a document onto a half-modeled base, you will map the wrong field. You will get record IDs where you wanted names, and duplicates where you wanted one value. I did all three.
- **Module 3 (Workflow Building)** comes next because the document is one step in a pipeline, not a standalone file. Whether a total can appear on the PDF at all depends on whether the value exists at fill time. That depends on how the form and the automation are ordered. You cannot design the document until you know the sequence of writes that feeds it.

If you have those three, the main idea here is simple to say and hard to fully take in: **a rendered document is a snapshot (a copy of the data as it stood at one moment), so design the base so the snapshot is worth taking, and design the workflow so you can retake it on demand.**

---

## Lesson 1 — The generated PDF is static, and that single fact drives the whole design

**The pattern:** Once Fillout generates a PDF on form submission, it is fixed. Changing the data in Airtable does nothing to the already-generated document. To show a new value, a person has to re-submit the form. That re-triggers the integration and writes a fresh PDF. Design around the re-render, not around a document that updates itself.

### Case study — Client B, 2026-06-08

I was building the manager-approval loop for advertising contracts. A sales rep submits a contract with a proposed total. A manager can approve it, reject it, or propose a revised total. That revised number lands in Airtable in a field I was calling the proposed contract total. A `resulting` field decides which number is the real one: the proposed figure when it exists, the computed line-item total otherwise.

Here is the bug I hit. I changed the proposed total. I watched the `resulting` field update correctly in Airtable. Then I opened the already-generated contract PDF and it still showed the old number. I assumed the mapping was broken. Nothing was broken. The PDF had been generated at the original submission. It had no idea the data moved.

A PDF is static by definition. It still shows the contract total that existed at the moment it was generated. So somebody has to go into the form and regenerate it by resubmitting. In this case the approval goes through an update form. That update form carries the same PDF integration. The manager clicks through the fields, submits, and the integration re-runs against whatever the data says at that moment.

The fix was not a fix to the PDF. It was accepting that the update form is what re-renders the document. Twenty minutes later we proved it live. I opened the file after the resubmit and it had been regenerated, now showing the revised total.

Two supporting pieces of the design exist only because the PDF is static. First, the `resulting` override field, so the document has exactly one total to map instead of a choice to make at render time. I set up a custom total-cost field. If the custom contract total is not blank, the `resulting` field shows the custom number. If it is blank, `resulting` shows the number computed from the line items. One field, one value, no decision left for render time.

Second, a conditional on the PDF, so the revised-total block only appears when a revision actually exists. Without it the document always prints an empty proposed line. The block shows only if the proposed total is full, meaning not empty.

### Principle

A rendered document is a copy of the data at render time, not a live view of it. Changing the data does nothing until you re-render. So you build two things. One is a single field the document maps to, never a runtime choice. The other is an explicit, cheap re-render action, here an update-form re-submit, that a non-technical person can trigger with a few clicks. If your design assumes the document tracks the data, your design is wrong.

### Where it changed

The re-render workflow worked. It shipped for the proposed-versus-resulting total. But notice what it cost. A person has to remember to re-submit. If they do not, the filed PDF silently disagrees with the base. That fragility is one of the reasons the whole Fillout-PDF approach did not last on Client B. When the document has to stay in agreement with fast-moving data, "someone clicks re-submit" is not a strong enough guarantee. Lesson 5 and the closing note return to this.

---

## Lesson 2 — Map the PDF to a rollup, not a lookup, and to names, not record IDs

**The pattern:** The field you map onto a document is almost never the raw linked field. A lookup (a field that pulls a value from each linked record) across a one-to-many link repeats values. Map a rollup with `ARRAYUNIQUE` to get one distinct value instead. A raw link-record field (a field that links a record to records in another table) carries record IDs. Map the human-readable name or formula field instead. The document exposes exactly the modeling shortcuts you took, so take none.

### Case study — Client B, 2026-05-08

The contract PDF was printing the advertiser's QuickBooks Customer ID three times. My first honest reaction, on the recording, was that the duplication was partly my own test data. I had put three of the same QuickBooks IDs in for three different testing records, so some of that was on me.

But test data only exposed the real defect. The QuickBooks ID was stored on the Contact table, and one advertiser has several contacts. The PDF field was a lookup of QuickBooks ID across contacts, so it returned the value once per contact. Three contacts, three copies of the same ID. Two problems stacked on top of each other. The root problem was level: the ID was stored one level too low.

How QuickBooks assigns the ID settles where it belongs. QuickBooks gives an ID to a customer, not to each contact inside that customer. So the ID belongs on the Advertiser (customer) table. That is the correct long-term fix. But we also needed the document to stop showing three IDs immediately. For that the answer is a rollup. Make the field a rollup that picks up QuickBooks ID from contacts and runs `ARRAYUNIQUE` over it, and the fix is quick.

A rollup aggregates the linked values through a function. `ARRAYUNIQUE` reduces "the same ID three times" to the one distinct value. That is what you map onto the PDF. Same underlying links, different output, because a rollup can de-duplicate and a lookup cannot.

The name-versus-record-ID version of this same lesson had cost me a session weeks earlier, on the line-item product. The PDF was showing raw record IDs where the product name should be. I had mapped the link-record field itself. The mapped value was the exact record reference rather than the readable value. Once I pointed the mapping at the field that carries the name, the product name came through. It was not the lookup. It was the concatenated three-line field that gave me the name.

A link-record field is, underneath, a set of record IDs. Map it into a document and you print `recXXXXXXXX`. Map the readable name or formula field the record shows, not the link.

### Principle

A document renders whatever the mapped field actually holds, which is not always what you think it holds. A lookup holds one value per linked row, so it repeats. A link field holds record IDs, so it prints gibberish. A rollup can hold one distinct, aggregated value. A name or formula field holds readable text. When mapping to a document, map the field whose stored value is already the exact string you want a person to read. If it is not, build that field first.

### Where it broke

This one has an honest mistake in it. In the middle of remapping the QuickBooks field to the rollup, I deleted the wrong field. There were two fields with almost the same name, QuickBooks ID from Contacts versus QuickBooks Customer ID. The one I deleted was the latest one, the one we were actually going to use. One was the target, one was the leftover, and under time pressure I removed the keeper.

The lesson inside the lesson. When you are combining duplicate fields down to one source of truth for a document, name the survivor unmistakably. Delete the loser last, after the mapping already points at the survivor and you have confirmed the render. Deleting first and re-mapping second is how you lose the field you meant to keep.

---

## Lesson 3 — Fillout can't branch its PDF outputs, so branch upstream

**The pattern:** Fillout runs every PDF integration you configure on every submission. There is no "if this condition, generate this PDF and not those." If different cases need different documents, you cannot select the document inside one form. You move the branch upstream: one form per case, and a single formula field that hands the right form's URL to the right person.

### Case study — Client A, 2025-08-26

Client A enrolls medical-coding students, and the enrollment agreement is legally different by state. Florida, Indiana, South Carolina, Texas, and a headquarters default each have their own document. My instinct was one enrollment form that generates the state-appropriate PDF based on the student's state. That instinct is wrong.

Fillout by default will not let you select, based on a URL parameter or any other condition, whether a given document should be generated. PDF integrations always run on form submission. You cannot set conditional branches. You cannot tell it: if Florida, then fill out this one PDF and not the other three.

If I had put all five state PDFs on one form, every submission would have generated all five. A Florida student would get an Indiana agreement and a Texas one along with the Florida one. So the branch has to live before the form, not inside it. The design became: one enrollment form per state, each carrying only its own PDF, and one Airtable formula field that outputs the correct form's URL by the student's state.

For that selector I used `SWITCH` rather than nested `IF`. `SWITCH` is an Airtable formula function that gives you a shorter formula. You name the field you are assessing, then for each value you give the output. If it contains FL, do this, and so on. No stacking of nested `IF` statements. You assess the content once and map each value to its output.

Two consequences follow from "one form per state." First, build the original HQ form completely before you duplicate it. Every mapping error you copy is an error times five. Delete the half-built Florida version. Get everything working on the headquarters original. Confirm every field is mapped correctly. Only then create the duplicates. Duplicate a broken form and you will spend a long time fixing each one.

Second, resolve the branch once and only once. I made the mistake of also re-implementing the state conditional inside the automation, keyed on base-structure field IDs. Two days later I saw why that was wrong. The pattern I had written was "where the field ID of some base-structure field is TX, then do something." That is not the correct way to do it. The better move is to drop that logic entirely and just have the email action send the dynamic URL. The URL already captures the state.

The formula field already knows the state and already produces the right URL. The automation should just send that URL. Encoding the same branch twice, once in the formula and once in the automation, gives you two places to keep in agreement and two places to break.

### Principle

When a tool cannot branch its outputs, do not try to make it. Move the decision to the layer that can make it without repetition, resolve it exactly once, and pass the resolved result downstream. Here the layer is a single Airtable formula that maps state to form URL. Everything after it, the email and the automation, consumes that one resolved value and adds no logic of its own.

### Where it changed

This design held for Client A because the number of branches was small and fixed: five states. It does not scale to a case where the branches multiply or change often. "One form per case, built and re-tested by hand" is linear human work per case. The moment you feel yourself duplicating and re-mapping forms as a routine chore, the form tool is no longer the right choice. That is exactly the direction the Client B build eventually went.

---

## Lesson 4 — No dynamic line items, and no letting a model free-choose values: parse deterministically

**The pattern:** A Fillout-generated PDF cannot render a variable-length line-item table. The best it returns is a flat array of products next to a parallel array of quantities. And when you parse messy source data into the fields a document reads, do not ask a model to choose which value each row means. Have the model write a deterministic parsing formula, then audit its output. A deterministic parse is one where the same input always produces the same output, by a rule you can read. The document is only as trustworthy as the parse behind it.

### Case study, part one — Client B, 2026-03-17

I wanted the contract PDF to show each line item as its own row: product, quantity, size, position, one line each. The integration cannot do that. Set the expectation before you over-build toward it. This integration cannot generate dynamic line items.

The best you get with this workflow is an array of products next to an array of quantities, one array beside or below the other. You would see bananas, oranges, potatoes, and below it 1, 2, 3. It does not look nice, and it is not a real table.

The closest workaround is to pack each line's pieces into one formula field, so a single field reads like a structured line. If you name your line item something like product, then the quantity in parentheses, you get something that resembles a real line.

And here is its ceiling, which I had filed as a feature request more than once. Formulas do not handle rich text. If they could, you could put line breaks inside the line-item name. No rich text in a formula means no line breaks inside the concatenated line. So the imitation structured line is one long string, not a real table. That limit is a large part of why the AY contract PDF eventually moved off Fillout entirely.

### Case study, part two — the parse behind the document, Client B 2026-04-14 and the currency bugs

A document is only as correct as the data mapped into it. Client B's historical data was roughly 15,000 rows of free-text memos. Ad sizes, sections, and positions were buried in a memo column with typos and inconsistent formatting. The tempting move is to hand the whole column to Claude and say "pick the right library value for each row." I did not trust that.

I did not want to trust a model to choose what value should be there without very strict logic. There are two ways to go. One is to tell the model to go through the rows and choose whatever value it thinks should be selected. The other is to use the data from the memo column and ask the model to help build a formula to parse the values. The parsing route also surfaces the typos. The formula can say that if a cell reads "half-horizontal" or "half-horizonta" without the final letter, treat it as half-horizontal page. If there is nothing to map a cell to, tag it as unknown.

The difference is where the judgment lives. Letting the model choose a value per row means 15,000 unaudited decisions you cannot inspect. Having the model author a deterministic parsing formula means one artifact you can read, test, and correct. This pattern of characters maps to this library value; non-matches tag as "unknown." You also get a clear list of "unknown" rows to review by hand. The model writes the rule. The rule makes the choices. You audit the rule.

Currency was where deterministic parsing mattered most, because currency is where format bugs are hardest to see. On the CSV import side, the client's source files carried literal dashes as placeholders in numeric columns. A dash mapped to a currency field errors the import. A dash does not hurt a text field, but it does hurt single-select fields (fields that store one chosen option from a list), currency fields, and others. If you try to map a dash to a currency field in Airtable on import, it can error, because Airtable expects specific formats for currency.

The subtler cousin of that bug is the comma-versus-period separator problem. It took real debugging in the n8n PDF-parsing workflow on Client A, in the 2025-10-03 session. n8n is a workflow automation tool. A unit price that should have printed as $110 was coming through as $11,000, because a comma was being read where a period belonged. It was supposed to read $110 and it was reading $11,000. The value needed a period where it had a comma.

The whole lesson is in the open question we did not resolve in the room. Was the bug coming from the model, or did it need to be fixed in the workflow. We argued it out. My read was that the value came from the model, since the whole thing was flowing out of the LLM, and it could be coming out of the LLM in a strange format.

The other read was that the destination field's own format was in play, and that the real fix is making the producing format and the consuming format agree. In Airtable you can get this issue depending on how the field is typeset for periods versus commas. So you may want to match the format the source system is using with the format the LLM is using. We left it as something to look at rather than solving it on the call.

We did not resolve it in the room, and that is the honest and useful part. A value like `1,000.00` versus `1.000,00` parses to wildly different numbers, depending on whether the comma is read as a thousands separator or a decimal point. A document that prints the wrong one is worse than a document that errors, because it looks correct. The design lesson is not a single answer. It is knowing the bug lives at the parse, not in the PDF template and not in the field's display. It is somewhere between the LLM's output format and the destination field's typeset, and you fix it by making those two agree at the point the number is produced. Fix it once at the parse and every downstream document inherits a correct value. Reformat it on the document and you have corrected one already-generated file, while the next parse still produces the wrong number.

### Principle

Know the hard limits of your document tool: no dynamic rows, no rich-text line breaks. Design the document to what it can actually render, not to what you wish it could. And upstream of the document, keep value selection deterministic. A model writes the parsing rule. The rule assigns values. Non-matches are tagged and reviewed. Currency is normalized at the point of parse. A pretty document over a guessed value is a liability, because it hides the guess.

### Where it changed

The concatenated-line-item workaround and the parse both worked. But both are evidence for the same conclusion. Fillout could not render the real line-item table AY needed. The workaround, one long formula string with no line breaks, was never going to satisfy a client looking at a real invoice. That is a direct input into abandoning Fillout PDF generation. The parse itself kept working after the tool was gone. A deterministic parsing formula does not care what renders the final document, which is exactly why it worked through the switch to Adobe.

---

## Lesson 5 — Replace DocuSign with signature fields in the form

**The pattern:** If the only reason a separate signing tool exists is to collect a signature on a document you are already generating, move the signature into the form. Fillout has a signature field type. Used well, it removes DocuSign from the workflow and keeps signing, generating, and storing in one place.

### Case study — Client A, early build, 2025-07-28

Client A's enrollment agreement was running through DocuSign. The student filled out enrollment, then went to a separate tool to sign. The signed document lived apart from the base that tracked the student. The plan from the start of the Fillout build was to combine those. Rebuild the enrollment agreement as a Fillout form, populate it dynamically from Airtable, and use Fillout's signature field, a paid feature, to capture the signature in place. Then the generated PDF is already signed and already attached to the student's record.

A note on sourcing, in the spirit of the rest of this course. This early call exists only as a Fathom summary, not a full verified transcript. So I am reconstructing the decision from that summary rather than a word-for-word record. What the summary records is the decision and its shape: transition from DocuSign to Fillout, using Fillout's signature field type, a paid feature, to replace the DocuSign functionality. The action item that followed was mine. Copy the full enrollment-agreement text into the Fillout form and add signature fields for each page.

The move is a tool-count reduction. Every additional tool in a document workflow is another integration to maintain. It is another place the document can go out of agreement with the base. It is another system the client has to own after I leave. Signing inside the form means the signed document is generated and attached in one submission, with no separate signing tool in between.

### Principle

Count the tools in a document workflow and delete the ones that exist only to bridge a gap the form can already close. A signature is data the form can collect. When the form generates the document and captures the signature in the same submission, the signed file and the record that tracks it are never separated. And there is one fewer subscription and integration to hand off.

### Where it changed

Two honest qualifications. First, the Fillout signature field is a paid feature. So "remove DocuSign" is not "remove cost." It is "consolidate cost into the tool you already run," which is only a win if the form tool is one you are keeping. Second, on Client B the whole Fillout-generated-PDF approach was abandoned for Adobe, and the signing story moved with it. The AY workflow became: download the generated contract, send it for signature outside the form, and attach the signed copy back through a deliberately minimal one-field update form. So "signature fields in the form" was the right consolidation for Client A's enrollment agreement. It was not where the more document-heavy AY build ended up. The consolidation instinct was right. The specific tool was not permanent.

---

## What I'd do differently now

**I would decide whether the document must stay live before I chose the tool.** The static-PDF fact is not a Fillout quirk to work around. It is the first design question. If the document is a one-time file, like a signed enrollment agreement that never changes after signing, a generated-on-submission PDF is genuinely fine, and the re-render problem never arises. If the document reflects data that keeps moving, like a contract total that a manager revises, then "static snapshot plus a manual re-submit" is a weak guarantee. I should have priced in a rendering approach that recomputes on read, or filled the client's own PDF by API, from the beginning. On AY I learned this by building the fragile version first and abandoning it. I would now ask "does this document change after it is first generated, and who is responsible for keeping it in agreement?" before writing a single mapping.

**I would build the field the document maps to before I opened the PDF integration.** Every document bug in this module, the record IDs, the triple QuickBooks IDs, the wrong total, was really a field problem that only became visible on the document. If I had built the rollup, the name formula, and the `resulting` override field as first-class parts of the schema, then mapping would have been a matter of pointing at already-correct fields. Instead I mapped raw fields, saw garbage in the render, and worked backward. Map last, model first.

**I would stop re-encoding the same branch in two places.** The state conditional lived correctly in one formula field, and I still went and rebuilt it inside the automation. Resolve a decision once, at the layer that owns it, and let everything downstream consume the resolved value. Two copies of one rule is two things to keep in agreement and one silent disagreement waiting to happen.

**I would keep the parse and drop the renderer sooner.** The deterministic parsing formula was the most durable thing I built in this entire module, because it does not care what draws the final document. The Fillout PDF integration was the least durable. I spent months on the renderer and it did not last. The parse kept working after the switch to Adobe, unchanged. Invest in the layer that keeps working after the tool is gone.

## Exercises

1. **Break the snapshot on purpose.** On a practice base, build a Fillout form that generates a PDF from a total field and submit it. Then change the total in Airtable and re-open the generated PDF. Confirm with your own eyes that it still shows the old number. Now build the update-form re-submit path and regenerate it. Write two sentences: which of your real documents must stay in agreement with moving data, and who on the client side is responsible for re-triggering the render when the data changes. If the answer to "who" is "nobody remembers," that document should not be a generated-on-submission PDF.

2. **Turn a lookup into one distinct value for a document.** Take any table where a parent links to several children that share a repeated value. An advertiser with multiple contacts sharing one external ID is the standard case. Map a plain lookup of that value onto a document and observe the repetition. Then replace it with a rollup using `ARRAYUNIQUE`, re-map, and confirm the document now shows one value. As a second pass, find one place you mapped a link-record field directly and confirm whether it renders a name or a record ID. If it renders an ID, build and map the name or formula field instead.

3. **Write the parser, do not let the model choose.** Take a column of messy free-text values: ad sizes, categories, statuses, anything with typos and inconsistent formatting. Give a model the full list of allowed target values plus a sample of the raw column. Ask it to write a deterministic parsing formula that maps patterns to allowed values and tags every non-match as "unknown." Run it, then read the "unknown" rows by hand. Count how many rows you would have gotten wrong if you had instead asked the model to free-choose a value per row. That count is the argument for this whole lesson. For extra credit, seed the column with one `1,000.00` and one `1.000,00` and confirm your parse produces the correct number for both, rather than silently reading a decimal as a thousands separator.
