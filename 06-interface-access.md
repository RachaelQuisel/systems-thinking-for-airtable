# Module 6 — Interface & Access Design

*Systems Thinking for Airtable · Rachael Quisel*

---

## Frame

Every build I do ends the same way. Real people need to open a screen and see only the records that belong to them. And I need to hand that screen out without giving anyone the whole base.

That is what this module is about. Not the schema, not the automation. The layer where a caseworker in Texas, a sales manager at AY Media, or an account executive logs in and does their job. This is the layer clients actually touch. It is also the layer where a build that looked finished in the demo breaks the moment 148 people are pointed at it.

The hard part is that Airtable's sharing model is a set of fixed limits with a few known ways around them. Every workaround trades one thing for another. A public share is free and safe, but it strips out linked-record data and disables interface buttons. A read-only collaborator gets full navigation for free, but can see every record in the base. Per-user data isolation, where each person sees only their own rows, is possible in Airtable itself, but it costs a paid seat for every single user. And the moment the requirement is a dashboard behind a login on a custom domain, you have gone past what Airtable interfaces do at all. Now you are choosing between Airtable's own Site and Canvas features (Airtable's tools for publishing a web page or dashboard straight from a base) and a fully custom-coded front end that the client cannot maintain after you leave.

One tension runs through the whole module. As builds get complicated, the tendency is toward code you can control directly. The opposite pressure is toward whatever the client can still own after you are gone. Both are real. Neither wins by default.

So the point of this module is not "use Site" or "use interfaces." The point is that interface and access design is a set of tradeoffs you name out loud and commit to. The wrong default is the one you reach for without checking the constraint that actually decides it. For Coding Clarified that constraint was HIPAA. For AY Media it was whether the client could own the thing after I was gone.

## Prerequisites

This module depends on Modules 1 and 2, and not loosely. Interface fields are references into the schema. A page does not hold data. It filters, displays, and links to data that lives in tables. So every capability in this module sits downstream of a schema decision you already made.

A per-user filtered page can only filter on a field that exists at the right level. To show a caseworker only their own students, the caseworker's email has to live somewhere the page can compare against the logged-in user. In the Coding Clarified build we kept the caseworker as a plain single-line-text field (free-typed text, not a link to another table) rather than a linked Caseworkers table (a field that points to rows in a separate table). Converting it to a lookup would have broken the WooCommerce Zap (an automation in Zapier) that wrote the value as free text (Module 4). That was a defensible, lean choice. It is also the kind of choice that constrains the interface layer later. A free-text caseworker is harder to drive a login filter off of than a linked record with a real email field. When you read "filter the page by the logged-in user's chip" below, remember the chip is only there if the schema put it there.

Same with the dashboard totals. A manager review page that shows "proposed total" next to "resulting total" is reading a rollup (a field that combines or totals values from linked records) and an override formula. Those only make sense after the Contract to Contract Line Item model settled, and after the resulting-total field was defined as "use the custom value if it is not blank, otherwise use the line-item rollup" (Module 1). The interface only shows what the schema holds. If it shows the wrong number, the bug is usually one table down.

So: schema before interface, always. What follows assumes the model underneath is already correct.

---

## Lesson 1 — The 148-caseworker interface wall

**Pattern: Airtable caps interfaces at 50 pages per interface and 50 interfaces per base. You cannot give each of N users their own page. When N is large, the native answer is ONE page that filters dynamically on the logged-in user, which costs a paid seat per user. Below that budget you either use one public page with a manual filter, which leaks, or you leave Airtable for an external portal.**

### Case study

Coding Clarified is a medical-coding school. Students enroll, and each student is assigned to a caseworker. The caseworker is supposed to see that student's progress: which tracker they are on, what they have submitted, their attendance. My first instinct was the obvious one. Give each caseworker their own interface page, filtered to their students, and send each one their own link.

On 2025-08-26 I hit the limit. There were 148 caseworkers, and Airtable does not let you build 148 pages. The cap is 50 pages per interface, and 50 interfaces per base. You can work within that ceiling, but you have to know it is there before you design against it. It silently caps the "one page per person" idea before you even write it down.

Even if the math had worked, maintaining 148 near-identical pages by hand is a job nobody should sign up for. The native way to do this is one page with a dynamic filter. The filter compares a field on the record against the email of whoever is logged in: show records where the caseworker's email equals the logged-in user's email. One page serves any caseworker. The catch is that every caseworker then needs their own authenticated Airtable account, paid for by the workspace owner.

That last clause is the whole cost. One page serves all 148 caseworkers, but only if all 148 are authenticated Airtable users with paid seats bought by the workspace owner. The filter works because Airtable knows who is logged in. No login, no per-user filter.

I had already hit the deciding constraint two weeks earlier, on 2025-08-12, when the roster was quoted at 133 rather than 148. The caseworker list was not fixed month to month, which is worth noting on its own. The count I was designing against moved by fifteen people across two sessions, and a number that moves is a number you build slack around. The mechanics were the same either way. Per-user isolation in Airtable is easy as long as each person has their own account, because you set the filter to ask "is the logged-in user's email this?" and show only the matching records. What actually ended the plan was HIPAA. The other caseworkers cannot have access to the other students' records.

That is the sentence that decides the architecture. The tempting free workaround is one public interface with a dropdown filter, where each caseworker picks their own name. It is disqualified outright. A dropdown filter does not enforce anything. Any caseworker could pick any other caseworker's name and see students who are not theirs. For a school handling protected student health information, cross-visibility is not a minor problem. It is a violation. So the choice narrows to two real options: pay for 148 authenticated seats, or stand up an external portal that enforces per-user access itself.

### Principle

Per-user data isolation in Airtable is a paid feature, not a filter you can fake. One dynamically filtered page beats 148 hand-built pages, but the filter only holds when every viewer is authenticated, which means a paid seat each. Below that budget, a public page with a manual filter does not isolate data. It only hides it politely, and "politely hidden" fails the moment the data is confidential or regulated. Find the constraint that actually governs, HIPAA here, and let it disqualify the cheap-but-leaky option before you commit to it.

### Where it broke or changed

The natural next move, once native per-user isolation is priced out, is a front-end portal. My standing position is to avoid portals when I can. A portal is one more integration, one more thing that needs to be maintained, one more thing that breaks. I have paid for ignoring that. But once HIPAA rules out the shared public filter and the client will not buy 148 seats, a portal is what is left, and the next question is which one.

Here is where I want to be honest about a recommendation that is easy to get wrong. The conventional advice, when you need a lightweight front end over Airtable, is to reach for Softr and stay away from Bubble (two tools for building a web front end over Airtable). The reasoning: Bubble asks a lot of you to stand up, and Softr you can get running without much extra effort. That advice is sound in general, and it was wrong for me, because it rested on a fact about me that was not true. I had spent the previous two years learning Bubble. I am basically Bubble certified.

The lesson I keep is not that the advice was careless. It is that "which tool is easier" is never a fact about the tool alone. It is a fact about the tool and the person holding it together. Generic advice that recommends against your actual strongest skill is a reminder to state your own capabilities out loud before you accept a recommendation built on a guess about them.

---

## Lesson 2 — Public share versus read-only base access

**Pattern: To hand out an interface, you pick between two free options. Publicly sharing a single page exposes no backend, but it strips linked-record data and disables interface buttons. Inviting the viewer as a read-only collaborator gives full multi-page navigation, but exposes every record in the base. Choose by matching the navigation you need against the data exposure you can tolerate, and reach for the specific workarounds when neither fits.**

### Case study

By 2025-10-03 the Coding Clarified build had a multi-page interface with a dashboard. I wanted to publicly share the whole thing so caseworkers and the client could see it without any account. That does not work the way I hoped. It is worth walking through exactly why, because the two failure points are the ones people get wrong most.

First hard limit: public sharing is per single page, and it excludes the dashboard. Airtable does not let you publicly share an interface that contains multiple pages. You can publicly share a single page on its own, but not overview pages, and the dashboard is an overview page. So the one screen the client most wanted to see is the one screen a public share cannot deliver.

Second hard limit: a public share hides linked-record data. If a record shows fields that are links to other tables, those linked values do not render on the public page. When you publicly share, the linked records simply do not show up.

So the free, no-account, zero-backend-exposure path costs you the dashboard and your relational data. The alternative is a read-only collaborator, which is the opposite set of tradeoffs. It is still free. It gives the full navigable experience, including the dashboard. But the viewer can see the entire base behind it. If you do not mind the user having access to the data layer, you share full read-only access, you do not pay for it, and if you send them straight to the interface URL they get the full read-only experience: the green navigation tab on the left, every page including the dashboard, the whole thing to move through.

The caveat is the same one from Lesson 1, stated plainly. A read-only collaborator can see all the data on the back end. So if you have data that is not ready to be seen, or confidential data, this is not good. For a HIPAA base that caveat is fatal again, which is exactly why Lesson 1 pushed us toward a portal for the caseworkers. But for a client stakeholder who is allowed to see everything, read-only collaborator is the better free path, because it keeps the dashboard.

The workarounds for when you commit to a public page anyway are worth memorizing. Each one restores one of the things the public page took:

- **Password the link.** In Manage Link Settings you can set a password on a public share. That gives you a thin layer of access control the public page otherwise lacks.
- **Use lookups or rollups to surface relational data.** A lookup (a field that pulls a value in from a linked record) or a rollup renders as a flat value. Public shares hide linked records, so put the value you need into a lookup or rollup field and it survives the public share.
- **Use a button FIELD, not an interface button, for actions.** Interface buttons frequently do not fire on public shares. An actual button field with an open-URL or mailto action works even for read-only and external viewers. Read-only or external users on a public share can click it and it will work, where an interface button sometimes will not.
- **Let read-only users write via embedded Fillout forms.** A read-only collaborator cannot edit records. But you can put a Fillout (a form builder that writes to Airtable) create form or a prefilled update form on the view as a button, and the external user submits through it. That is a workaround to Airtable's paid-editor limit. You get around the pricing constraint on editors, at the same cost: the user has access to the full data layer as read-only.

### Principle

There is no single "share the interface" button that does what you want. There are two free modes with opposite tradeoffs, public page (safe, limited, no dashboard, no links) and read-only collaborator (full navigation, full exposure). And there is a small set of workarounds, password, lookup/rollup, button field, embedded Fillout form, that each restore exactly one lost capability at a known cost. Design the share mode by writing down two things: the navigation the user needs, and the data they are allowed to see. The intersection picks the mode.

### Where it broke or changed

The button-field-over-interface-button rule is the one I would have gotten wrong on my own. In the builder the interface button looks like it works. It works for me, the authenticated builder, and silently does nothing for the external viewer. That gap between "works in my session" and "works for the person I shipped it to" is the recurring failure of this whole module, and the button field is the concrete fix for it.

---

## Lesson 3 — Per-user filtered pages: one page, the logged-in user's own records

**Pattern: When your viewers are authenticated, build ONE interface page filtered on the logged-in user, not a page per person. Filter a caseworker's page where caseworker email equals the logged-in user's email. Filter a manager's review page on the status flag that means "this needs you." One page absorbs any number of users and stays maintainable, because there is one page to maintain.**

### Case study

This is the same mechanism from Lesson 1, seen from the other side. In Lesson 1 the per-user filter was priced out for 148 unauthenticated, HIPAA-scoped caseworkers. But when the viewers are a small set of authenticated internal staff, the per-user filtered page is exactly right. The AY Media build is where I actually shipped it.

By 2026-06-08, AY Media had a discount-approval workflow. A sales rep, an account executive, proposes a price on a contract. If it needs sign-off, the account executive flags it, and it has to land in front of a manager. I did not build a page per manager or a page per account executive. I built one manager interface. The review page is filtered on the review flag, so a contract appears there precisely when it has been flagged as needing manager review. The sales rep proposes the value, and it shows up on the manager's interface because of the "needs manager review" toggle. The account executive checked that box, so the contract surfaces on the manager's page, and the manager comes in and looks at how much it costs.

The action on that page is a button, and this ties directly back to Lesson 2. Rather than send the manager a Fillout email with an opaque edit URL, I turned the update into a button placed on the manager's own interface. I strip the routing out of the form. Instead of the form going to the manager, I turn it into a button and put it on the manager's interface.

The filter key differs by role. The manager review page filters on a status field, the "needs manager review" toggle, so it collects flagged contracts from every account executive. A per-account-executive workspace filters on identity instead, the logged-in user's own records. That is the caseworker mechanic from Coding Clarified: set the filter to ask whether the logged-in user's email matches, and if so, show only that. Both are the same discipline. One page, a filter that resolves per viewer, no duplication.

### Principle

A page that changes what it shows based on who is looking, or based on a status that routes work to a role, is one page. Do not build N pages for N people. Filter on identity (the logged-in user's email or chip) when each person should see only their own records. Filter on a status flag when work should route to whoever holds a role. The count of users stops mattering to your maintenance burden, which is the entire point.

### Where it broke or changed

The manager review page only works because I decided, in the same conversation, not to keep a negotiation history. The approval loop is bounded to a single revision. The base stores only the proposed value and the final value, not the back-and-forth. If the manager accepts, they submit the form through. If not, they reject. That is the only back-and-forth. If it needs to be more than that, it escalates to a phone call or an email. The form is no longer where the negotiation takes place. It is one revision. The base only ever writes and overwrites the proposed amount. There is no need to keep track of historic negotiations.

That is a schema decision, store current state and overwrite the proposed field, and it makes the interface simple. If I had chosen to keep every revision, the review page would have needed a child table and a history view, and the one-page filter would not have been enough. The interface stayed simple because the data model stayed bounded. Module 1 deciding Module 6, again.

---

## Lesson 4 — When Airtable interfaces stop being enough

**Pattern: Fillout and Airtable interfaces cover a large amount of ground. But complex requirements hit their limits: a real dashboard, a custom domain, filtering out already-sold inventory, large sortable record lists. The fallback options, in rough order of client-maintainability, are Airtable Site, Airtable Canvas, and a fully custom-coded front end (a Next.js app on Vercel, with Airtable as the backend). The more capable the front end, the less the client can own it after you leave. Choose for where the build is going, but weigh handoff as a first-class constraint.**

### Case study

Across all four of the mature AY Media sessions, the pressure went the same direction: move off Fillout toward something you can control with code, because the workarounds kept accumulating. Fillout has no "does not contain" filter. Its generated PDFs are static. Its edit URLs are opaque. Its record fetches are hard to sort and paginate. Every one of those cost time in a build meeting. The argument for code is that its up-front cost pays for itself the moment requirements get complicated, which they always do. Even when it seems like heavier building to start with, as soon as things get complicated, and they always do, having the ability to control code is usually easier from that point on.

The most capable fallback option is a fully custom build. Airtable stays the backend, and the front end is custom code. On the AY-adjacent work this is the shape I moved toward for the first genuinely custom delivery, where the database is still Airtable but the front end is bespoke. The design came out of Claude, and the front-end code came out of Claude as well. That is the far end of the range. It is powerful, and it is also the end a client cannot maintain.

I keep to the general direction. Where I pushed back, and where the pushback stands, is on two specifics.

First, Site would not have saved us on this particular AY Media build. The requirement was not only "stop me from selling sold inventory." It was also a dashboard. Site could have solved the first. It could not deliver the second, so switching to it would not have avoided the work I did. On 2026-05-14 that is exactly where it landed: using Site would not have helped avoid any of this, given that they also wanted a dashboard. If they had not wanted a dashboard, and only wanted the "do not allow me to select something that has already been sold" behavior, that part could have been done with Site. The dashboard is the part that Site does not reach.

The honest reframe is that Site is the better bet for future flexibility, not for this build. You could argue that developing in Site rather than Fillout leaves you better prepared for whatever comes next, because Fillout carries certain limitations. That is a fair claim, and it is a different claim from "Site would have saved us here." It would not have. Both things are true at once. Site is a stronger foundation for the next requirement, and Site would not have removed the work this requirement demanded.

Second, and this is the constraint that actually governs the whole choice for AY-type clients: a custom Vercel front end is powerful, and the client cannot maintain it after I am gone. On 2026-05-14 the open questions were still unresolved. I needed a clear protocol for how a custom front end gets built, where it gets deployed (Vercel or a cloud store), how access is shared with the client, how a custom domain gets connected, how it gets maintained, and how the customer can really own it, so that when I am not around anymore they can still work on it. That is my problem with Vercel. I build things for myself on Vercel, but my clients cannot maintain that.

That is the deciding question. Not "which front end is more capable," which is Vercel and custom code, hands down. The question is "who owns and maintains this in a year." For a magazine sales team the honest answer is that they can maintain an Airtable interface and they cannot maintain a Next.js app on Vercel.

By 2026-06-08 I did come around for the next client. When the build is one where the extra capability is required from the start, code is the right call, and I said so: I am convinced. But the concession is scoped. It is a yes for builds that need what code gives you, not a blanket "always start in Site." The AY dashboard case stands as the counterexample, where switching frameworks would not have removed the work.

### Principle

The front end is a handoff decision, not only a capability decision. Rank the options by how much the specific client can own after you leave. Airtable interfaces, Site, and Canvas sit on the maintainable end. A custom-coded Vercel front end sits on the powerful end. Pick for where the requirements are actually going. When a more powerful front end is genuinely needed, make client ownership, access, custom domain, and maintenance an explicit part of the plan, not a problem you discover at handoff. And do not switch frameworks to solve one requirement if the framework you would switch to cannot cover the other requirements in the same brief.

### Where it broke or changed

Over the AY Media arc the front-end plan moved several times, and PDF generation left Fillout entirely. That is a sign that "which front end" was genuinely unsettled, not a solved default. Earlier in the same build, on 2026-02-12, I had repeatedly kept Fillout for the MVP (minimum viable product) specifically because the client had chosen it: I kind of had to go with what they were telling me at that point. Advocating Site across four calls and holding Fillout for the MVP was not stubbornness. It was the maintainability constraint and the client's own tool choice pulling against the capability constraint, and the resolution was per-build, not once-and-for-all.

---

## Lesson 5 — A live availability view is not a form, it is a dashboard

**Pattern: When the user needs to SEE what is still available before they act, a form is not enough. A form collects input. It does not show state. Inventory that can be sold once, premium ad positions, issue slots, needs a live view of what remains. That is a dashboard requirement, and dashboards are exactly the thing that pushes you past a simple Fillout form.**

### Case study

This is the requirement hiding inside Lesson 4's dashboard argument. It deserves its own naming, because it is the thing that decided the AY front-end question.

AY Media sells premium print positions, inside front cover, page 4, and each is sellable once per issue. On 2026-05-14 I worked out that the account executive does not just need to submit a sale. Before they submit, they need to see which positions for a given issue are still open, because selling a position that is already sold is the failure the whole feature exists to prevent. There are two ways to model that inventory. The fullest way is one record per sellable slot, one ad position per month per year, which is how you usually handle stock: when you sell it, it is no longer in your inventory. The leanest way is a lookup that finds the month and year of things already sold, and then a filter inside Fillout that hides those from the picker.

The leanest version, the Fillout filter, hides sold slots from the picker. That is genuinely useful, and it is a form behavior. But the client also wanted to look at the issue and see all the slots, sold and open, at a glance. That is not a filtered picker. That is a dashboard. It is the exact requirement I pointed at when I said Site would not have covered us: using Site would not have helped avoid any of this, given that they also wanted a dashboard.

So the availability requirement split into two: a form that prevents you from selecting a sold slot (which Fillout, or Site, can do), and a live view that shows you the state of all slots (which needs a dashboard). The presence of the second is what made the front-end decision hard.

### Principle

Ask whether the user needs to act or needs to see, because they call for different things. A form prevents a bad input. A dashboard shows current state. Inventory that is sellable once needs both, and the "needs to see" half is a dashboard requirement that a form cannot satisfy no matter how cleverly you filter it. Naming that split early tells you whether a simple form is enough or whether you are committed to a dashboard, and the dashboard is what changes the whole front-end conversation.

### Where it broke or changed

I nearly lost a full session to this by arguing front-end tools before I had named the two-part requirement. Once the availability need was split into the picker filter and the state view, the front-end question got answerable. Fillout covers the picker, and whether the state view lives in an Airtable interface, Site, or custom code becomes the Lesson 4 tradeoff. The lesson is that the interface question was unanswerable until the requirement was stated precisely, which is the recurring point of this entire module.

---

## What I'd do differently now

**I would name the deciding constraint before I open the interface builder.** For Coding Clarified it was HIPAA, which disqualified every free public-filter workaround before I spent a minute on them. For AY Media it was client ownership after handoff, which disqualified the most capable front end. Both times the constraint was knowable up front, and both times I started building before I said it out loud. Now the first question is "what is the one requirement that rules options out," and I answer it before I compare tools.

**I would test every share as the recipient, not as myself.** The interface-button-versus-button-field trap only shows up when someone who is not the authenticated builder clicks it. Everything works in my session. I now open a share in a separate context, or hand it to the actual user, before I call it done, because "works for me" and "works for them" are different claims, and only the second one ships.

**I would separate "needs to act" from "needs to see" on day one.** The AY availability feature stayed muddled for a long call because a picker filter and a state dashboard were being discussed as one thing. They are two things with two different front-end implications. Splitting them early would have made the front-end decision answerable a lot sooner.

**I would state my own capabilities before accepting a tool recommendation.** The Softr-over-Bubble reasoning was reasonable and built on a wrong guess about what I could do. A recommendation about which tool is "easier" is always about the tool and the person together, and I am the person, so I say what I already know how to build before I let a general rule of thumb recommend around it.

**I would treat the per-user filter as a paid feature, not a free trick.** The single-page logged-in-user filter is the correct native pattern, and it is only free of extra tooling if the client is already paying for a seat per user. When they are not, that is the signal to price the portal honestly, rather than reach for a public dropdown that does not actually isolate anything.

## Exercises

**1. Price the wall.** Take a base where you want N people to each see only their own records. Write down N, then write down the three native options and their real costs. (a) One filtered page per person: confirm whether N exceeds 50 pages per interface or 50 interfaces per base. (b) One dynamically filtered page: multiply N by the per-seat Airtable price the workspace owner would pay. (c) One public page with a manual filter: write one sentence describing exactly what a user could see that is not theirs. Then name the constraint (confidentiality, regulation, budget) that picks between them. If option (c) leaks regulated data, cross it out before you consider it.

**2. Match the share mode to the exposure.** Take a multi-page interface with a dashboard. For each intended viewer group, fill in two columns: the navigation they need (single page, or full multi-page including the dashboard) and the data they are allowed to see (their rows only, or the whole base). Use the two columns to pick public page versus read-only collaborator for each group. For any group that lands on "public page" but needs relational data or a working action button, list the specific workaround (lookup/rollup, button field, embedded Fillout form, password) that restores it, and the cost of that workaround.

**3. Split act from see.** Take a feature where a user chooses from limited inventory that can be consumed once (a room, a time slot, a print position, an appointment). Write two requirements as separate sentences: the form behavior that prevents selecting something already taken, and the view behavior that shows current availability at a glance. Decide whether each is satisfiable in a form or requires a dashboard. Then state whether the presence of a dashboard requirement changes your front-end choice, and how it weighs against who has to maintain the result after you leave.
