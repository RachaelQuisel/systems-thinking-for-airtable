# Module 7 — Project Management for Solo Consultants

*Rachael Quisel · Systems Thinking for Airtable*

---

## Frame

Most of this course is about building the client's system. This module is about building the system that tracks the work itself: who does what, in what order, and how long each stage took. For a solo consultant that is really two problems at once.

The first is a schema problem, and it has a clear answer. Model a task as a record, pulled from a template, linked to the thing it belongs to.

The second is an operating problem that no schema fixes, and it is the one I lived through. How do you keep building when the client is inside the base editing it while you work, deleting the fields you just made, and refusing to let you touch the third of the tables they built themselves?

So this module has two halves. The first half is the project-management architecture. I built it for the magazine advertising client (Client B), who runs articles, ads, photo shoots, and design work through repeatable stages. The architecture is good. It is also more than either of my two clients strictly needed. I will say that plainly as I go, because that is the honest description.

The second half is about running a build while the client edits the base underneath me. The architecture is one thing. Keeping a co-owned base correct while two people edit it is another, and it is the part I want you to see clearly.

One note on scope before the patterns, because I state scope up front in every design. The Client B task model was built for a shop with a handful of staff, a fixed set of repeatable production stages per advertisement, and dozens of projects a month, not thousands. It is not designed for a hundred-person agency that plans capacity per person. The non-goal matters as much as the goal. If you have five people and forty projects, this architecture is the right size. If you have five hundred people, you have outgrown Airtable for this, and no number of junction tables will fix that.

## Prerequisites

This module sits on top of the others. It makes sense only after Modules 1 through 6. Every pattern here is one of those patterns applied to your own workflow instead of the client's.

- **Module 1 (Schema Design).** "Tasks as records" is the same move as "scores as records" and "report line items as records." If you did not take in why repeating attributes become rows and not columns, start there. It is the same lesson, applied to project management.
- **Module 2 (Data Normalization).** The changelog (a running log of every status change over time) is an event log, which is a normalization idea. You never overwrite a status, you add a new row.
- **Module 3 (Workflow Building) and Module 4 (Automation Architecture).** The template-task cascade (the chain of automations that creates a project's tasks from a template) is a search-then-create automation with a repeating group. You need "don't create anything you didn't mean to create" to be second nature already.
- **Module 6 (Interface & Access Design).** The free native form that starts the cascade is an access-design decision: who can create a project without a paid seat.

If you have those six, this module is short. If you do not, this module will read as a pile of tricks instead of one idea applied five ways.

---

## Lesson 1 — Model a task as a record pulled from a template, not a field and not a single-select option

**The pattern in one sentence:** each task is its own record in a Tasks table, linked to its project, with its own status, date, and owner, and the set of tasks for a new project is created automatically by looping a Template Tasks table.

### Case study — 2025-11-25, Client B

I came into this work with a base I had built the previous weekend for the magazine client. They run production work in stages. An advertisement gets written, photographed, designed, and laid out. I had modeled those stages the way most people first do, as status fields and single-select options (a field where you pick one value from a fixed list) on the article and order tables. I wanted a solid pattern for a changelog. I could not answer the changelog question until I answered the task question, so I had to step back one level.

Here is the model. A Projects table (project A, B, C). A Tasks table, where each task is a record linked to its project. Each task record has a `Status` field (Pending, In Progress, Complete), a creation date, and, if you want it simple, a completion date. The key point: a task is not a checkbox field on the project, and not an option in a single-select. It is a row.

Then the part that makes it work with no ongoing maintenance: a Template Tasks table. You store the fixed set of tasks that every project of a given type always gets. When a new project record is created, an automation finds all the template tasks. In a repeating group, it creates one task record per template, matches its `Project` link to the project that was just created, sets its name to the template task's name, and sets `Status` to Pending. Create project D, and the whole checklist for project D is created for you, linked and pending, in one automation run.

The reason this beats the field-per-task layout is the one-off task (an ad-hoc task). If your workflow is fixed forever, you might get away with columns. But the moment someone needs a one-off, like "call Peter about this specific project," a field-per-task base forces you to add a new field just to hold that one task. That is absurd. In the records model, one task or a hundred tasks is the same schema.

Each task is its own record in the Tasks table, pulled from a template, not an option on a single-select and not a set of separate fields. That gives you two things. First, you can always link a task back to its template task, so you have traceability (you can trace each task to where it came from). Second, you can create a task through an automation or by hand, so the same table works as a real task tracker. The one-field-per-task layout gives you neither. As before, in the records model the architecture stays the same whether you have one task or a hundred.

The mechanics of the cascade: when a record is created on the Projects table, find all the template tasks and run a repeating group. For each found task, create a task record, match its project to the one that was just created, set its name to the name of the template task you are on, and always set its status to Pending.

### Principle

Repeating work becomes rows, not columns. A task is its own record, created from a template library, and the schema then holds any number of tasks, including one-off ones, with no structural change. Ownership, status, and timing belong to the record because the record exists. Traceability back to the template is free because the link is right there.

### Where it broke or changed

Two honest marks on this one.

First, this is a lot to take in, and not every client needs all of it. For the medical-coding client (Client A) I never needed the template-task cascade at all. That client's repeatable unit was a student's enrollment, not a multi-stage production task with a different owner per stage. The full architecture was worth it at Client B and would have been overhead at Client A. It is the right answer for shops with fixed, repeatable production stages that each have owners, and unnecessary for shops without them. Plenty of real bases are unclear on exactly this question: what are tasks, what are statuses, how do they get assigned. It is not something you ship to everyone.

Second, my board looked confusing at first because I had modeled statuses as if they were tasks. That is not a flaw in the pattern. It is the pattern working. Once tasks were records, the confusion had a place to resolve to.

---

## Lesson 2 — A changelog is one record per status change

**The pattern in one sentence:** to know how long something spent in each stage, do not overwrite a status field; write a new record every time the status changes, so the history is the rows.

### Case study — 2025-11-25, Client B

The original ask was the changelog. The photographers wanted their own photo-shoot changelog. The designers wanted a design changelog. I had built a changelog before and found it slow, and I wanted to know whether there was a faster way. The answer follows directly from the tasks-as-records model. A changelog is just tasks-as-records taken one level more detailed.

If you only need "when did this task start and when did it finish," one record per task with a start date and a completion date is enough. If you need "how long did it sit in each stage," you write one record per status change. Each record holds the same task, the same project, a status, and the date it entered that status. Created and Pending on the 25th, In Progress on the 26th, Complete on the 30th. Link those in date order and the durations come out as data: this status lasted one day, the next lasted four. You are not calculating durations from an overwritten field that has lost its own history. You are reading them off the rows.

For the fully detailed version, you record that on a given date a specific task reached a specific status: task 1, same project, a different date for each change. Created and pending on the 25th, in progress on the 26th, complete by the 30th. Linking those records in order shows that the task started on the 25th, that this status lasted one day, and that it is now in progress. One record per status, or one record per status change, is essentially the same thing.

### Principle

An overwritten field remembers only the present. An event log remembers every transition. If a stakeholder will ever ask "how long did this spend in review," you need the transitions as rows, decided at design time, because you cannot reconstruct history you already wrote over.

### Where it broke or changed

The cost is real. If you write one record per status change, showing the current status of each task inside a project view becomes hard, because the "current" status is the latest of many rows, not a field on the task. To show the current status you would need either the status written into the record name so it appears, or a lookup on each task (a lookup pulls a value from a linked record). Either way the display gets awkward. So the detailed changelog gives you duration history and costs you display complexity. For the magazine client I did not always need per-status detail. One record per task with start and completion dates covered most of the reporting. The lesson is to pick the level of detail against the actual question, not to build the most detailed thing by reflex. Most changelogs people ask for are answered by start-and-finish. The full per-change log is for when someone genuinely needs stage durations.

---

## Lesson 3 — Assign tasks by role, with a roles library, and add a junction table only when a person's role changes by project

**The pattern in one sentence:** tag each template task with a role, give each staff member a role, assign the matching person when tasks are created, and reach for a junction table exactly when one person plays different roles on different projects.

### Case study — 2025-11-25, Client B

Once tasks are records, they still need owners, and typing an owner onto every generated task by hand defeats the automation. So I assign owners through roles rather than names. Add a Roles library (designer, PM, CEO, photographer). Tag each template task with the role that should own it. Give each staff member a role. Then in the task-creation automation, or a second automation right after it, find the staff member whose role matches the template task's role and assign them.

Add complexity one step at a time, on purpose, because that is the part worth copying. The simplest version assumes each role maps to one person across the whole company. Each template task is assigned to a role, say designer. Each staff member has a role. Once the tasks are created, you find the staff member whose role matches each task and assign them. The next version, for when only some staff work a given project, links staff to projects so you only assign from that project's team. The most complex version is when the same person is a designer on project A and the PM on project B. Only there do you add a junction table (a table that sits between two others to record which records connect to which). It records, per project, which role each person plays: on this project this person plays this role; on that project the same person plays a different role.

### Principle

Assignment is a lookup against a roles layer, not a hand-typed name. Add a junction table at exactly the moment the relationship becomes many-to-many, meaning a person's role depends on the project, and not one moment before. The junction table is not free. It is worth adding only when the cardinality (how many records on one side relate to how many on the other) requires it.

### Where it broke or changed

This is the clearest place in the whole module where the architecture is more than the client needed. Neither of my two clients had the "same person, different role by project" problem in production. Client B's people had stable roles. The photographer photographed, the designer designed. So I built the roles library and the role-based assignment, and I never built the junction table, because the third setup describes a company I did not have. I taught myself all three levels so I would recognize the moment the third one becomes necessary. Recognizing it and building it are different acts. Build the level your cardinality actually is. This connects straight back to Module 1's junction-table rule: a junction that turns out to be one-to-one is not a junction, it is a duplicate.

---

## Lesson 4 — A free native Airtable form can trigger the whole template-task cascade

**The pattern in one sentence:** let external people create a project through a free native Airtable interface form, and the created record fires the same "create tasks from template" automation, so you never pay for a collaborator seat just to let someone start a project.

### Case study — 2025-11-25, Client B

The client did not want to pay a monthly per-collaborator fee for every rep who needed to start a project. My instinct, from the earlier meetings, was to reach for Fillout (a third-party form builder). But a native Airtable interface form does the job here for free. Build a form for the Projects table, publish it, share the link, and anyone on the web can submit it. The submission creates a project record, and because the automation triggers on record-created, the template-task cascade runs exactly as it would from an internal create. The external submitter needs no seat and no login.

To restate the flow: an external user submits the published form, a record is created, the automation triggers, it finds the template tasks, and it creates the tasks. The whole cascade runs. And when you do want a hosted form with more range, Fillout's free plan covers a lot: creation, updates, and several integrations are all possible on the free plan.

Be clear about when to use which option. Native forms and Fillout's free tier are the low-cost path for external record creation and updates. Reserve paid collaborator seats for people who genuinely need to be inside the base.

### Principle

The trigger for your automation cascade does not care whether the record was created by a paid collaborator, a native form, or a Fillout submission. Choose the cheapest creation method that fits the submitter's technical comfort, and let the record-created event do the rest. Access design and automation design are the same decision here.

### Where it broke or changed

The native form's limit comes from the same thing that makes it free. It creates records and collects the fields you put on it, but it is not a full editing surface, and it gives the submitter no way to browse the base. For pure project-creation that is exactly right. The moment the external user needs to update existing records, or see related data, or move through pages, you are back to the Module 6 choice: a read-only collaborator share (full navigation, full backend visibility, free) or Fillout update forms (write without a seat, at the cost of showing the backend read-only). The free native form is the correct tool for one specific job, external creation that starts a cascade, and you should not push it past that.

---

## Lesson 5 — Running a build while the client edits the base underneath you

**The pattern in one sentence:** when the client co-owns the base, builds a third of it themselves, refuses to let you change their tables, and edits and deletes your work while you build, you stop treating the base as yours to control and start treating forward motion, not tidiness, as the goal.

The architecture in the first four lessons is one thing. This is the part the engagement itself taught me, and it is the one I most want you to carry.

### Case study — 2026-05-14, and the weeks of repair on 2026-06-08

By May of 2026 the Client B base was five months into a shared build and it showed. The client had built about a third of the tables themselves, and they would not let me change anything they had built. Then they went into the parts I had built and started deleting and changing the fields and the data. This went on for months, which is a large part of why the build took as long as it did. The 2025-11-25 architecture is the reference version. What I had by May of 2026 is what that architecture looks like after five months of two people editing the same base with different ideas of how it worked.

By May, for the first time in the whole engagement, I was the only one touching the base. I had also made a second base and rebuilt the model from scratch, and the client got upset that I had gone ahead and done it. My read at that point: I was going to hand this to them and they were going to break it within about a week, and I had stopped worrying about that.

Here is the move I reached for when nobody in the room could say what state the live base was in. I think better from a blank base. Rather than argue with the live base, I would open a blank base and start over. Here are the products, here are the relationships, rebuild the model with everything I now know. That does not have to be the final version, and it does not have to be what ships. It is a way to mock things up and get my own understanding back. The person who has put the time into the live base still leads and still decides what ships. The blank base is a thinking tool for getting clarity back.

What I actually did, and what worked:

**I made a second base and rebuilt the model from scratch, even though the client got upset about it.** The blank-base move is a thinking tool, not a shipping plan. When nobody in the room could say what state the live base was in, rebuilding the core products and relationships from scratch in a blank base was how I got my own understanding of the model back. I did not need the mock to become the deliverable. I needed it to know what the deliverable should be. The client read the second base as me going around them, which is a real client-management cost. That is why this is a Module 7 lesson and not a Module 1 one: the technical move was cheap, the relationship move was not.

**I let go of trying to keep the base tidy.** By the 2026-06-08 session I was not trying to keep the base pure. I was doing exactly the kind of after-the-fact repair that a co-edited base forces. I set up a "no contract" view to find the line items the client's edits had left with no linked contract, backfilled a contract for each, moved contact links up from the line-item level to the contract level where they belonged, and deleted the migration fields once the data had been copied down. That is the convert-lookup-to-static migration (create a lookup, paste the value, delete the lookup, delete the source link) run as damage control rather than as planned design. The base was never going to be architecturally pure. The job was to keep it correct enough to work while two people edited it.

**I accepted that I would hand it over and they would break it, and I stopped worrying about that.** I was going to hand this to them and they were going to break it within about a week, and I did not care. That is not giving up. It is scoping. My job was to deliver something correct and understandable at handover. What happens after handover, in a base the client insists on editing, is their responsibility, not mine. Saying that boundary out loud was what let me keep moving.

### The recording was the memory system

One thing made all of this possible, across the whole engagement and the whole course: every session was recorded. Eleven months of weekly calls is more than any consultant remembers. A co-edited base that changes every week is exactly the situation where "what did we decide about where start and end dates live" is a question you will ask three times. The recordings are why I can tell you that the start-and-end-date table location changed inside a single 2025-11-25 meeting, or that the pattern-matching-versus-AI parsing decision (regex is pattern matching on text) reversed across three meetings in the fall. Without a recording of every session, a solo consultant on a months-long co-edited build is reconstructing decisions from memory. That is the same failure as overwriting a status field: you keep only the present and lose the history. Record every session. The transcript is your changelog for the engagement itself.

### Principle

On a live, co-owned base you do not control, aim for forward motion and correctness, not for tidiness or ownership. Use a blank-base mock as a thinking tool. Expect after-the-fact repair as the normal cost of shared editing. Record every session so decisions are data you can search. Name the boundary of your responsibility at handover, so you stop spending effort defending a base someone else is going to edit anyway.

### Where it broke or changed

The second base is the hardest call. It got my clarity back and it upset the client, and I would weigh that trade differently now (see below). The honest read is that some of the five months of slowness was the client editing my work, and some of it was me not settling, early and in writing, which tables were mine to change and which were theirs. I treated it as a technical problem for a long time before I treated it as an agreement problem. The agreement problem is the one that was actually costing the months.

---

## What I'd do differently now

**Match the architecture to the client before I teach it back to them.** The full set is a complete and correct system: tasks as records, template cascade, changelog per status change, roles library, junction table, native form. But I came out of building it ready to deploy all of it, and only one of my two clients needed most of it. Now I would start by asking which level of the roles model the client's cardinality actually is, and whether they need per-status durations or just start-and-finish, and I would build exactly that. This is a lot to take in, and I should have read that as a sign to build less, faster.

**Settle table ownership in writing before the co-build starts, not five months in.** The single most expensive thing in the Client B engagement was not a schema decision. It was that the client and I edited the same base for five months without a written agreement about which tables were theirs to change and which were mine. The second base, the deletions, the repair sessions, the upset: most of it traces back to an ownership boundary that was never written down. I would now open a co-owned build with a one-page statement of which tables each side owns and what "done" looks like at handover.

**Use the blank-base mock earlier and more openly.** I reached for the from-scratch rebuild in month five, out of frustration, and the client experienced it as me going around them. If I had introduced "I'm going to mock the core model in a scratch base so we both understand it, and it is not the thing we ship" in month one as a normal working practice, it would have been a shared tool instead of a move that looked territorial.

**Keep the tasks-as-records pattern; drop the reflex to build the detailed changelog.** The records model is the keeper from this module. It changed how I build, and it is the one I now reach for by default whenever I catch myself modeling a checklist as fields. But I over-built changelogs early, one record per status change on things nobody needed durations for. Start-and-finish dates on one record per task answer most of what people call a changelog. Build the per-change log only when someone names a real question about stage duration.

---

## Exercises

**Exercise 1 — Convert a field-per-task board to records.** Take any base where you have modeled a checklist as checkbox fields or a workflow as single-select statuses. Build a Tasks table and a Template Tasks table. Write the record-created automation that loops the template tasks and creates one linked, pending task record per template. Then prove the payoff. Add one one-off task by hand and confirm your schema did not change to fit it. If you had to add a field, you did not finish the conversion.

**Exercise 2 — Build the changelog both ways and see the tradeoff.** On the same base, first build one record per task with a start date and a completion date. Then build one record per status change. For each, answer two questions: "what is this task's current status" and "how long did this task sit in the In Progress stage." Notice that the simple version answers the first question easily and cannot answer the second. The detailed version answers the second directly but makes the first one need a lookup or a status-in-the-name trick. Write down, for your actual client, which question they will really ask, and keep only the version that answers it.

**Exercise 3 — Draft the ownership agreement you wish you'd had.** For a real or imagined co-owned build, write the one page I did not write. List every table, mark each one as yours-to-change or theirs-to-change, state what "done" means at handover, and state plainly what happens to your responsibility after the client edits the base once it is handed over. This is a Module 8 (Client Communication) artifact as much as a Module 7 one, which is the point. The project-management cadence produces the documents the client actually sees, and the ownership boundary is the one that would have saved me five months.
