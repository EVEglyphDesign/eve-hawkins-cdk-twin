# The CDK Monday Approach

---

## 1. The shape of it

Five messages and two calls, all inside one working day, none of them dependent on any of the
others. No single person at CDK can see the whole shape, and no single person can stall it. Every
message is answerable by the person receiving it, and every one of them asks only for something
Peterbilt Atlantic is already entitled to.

The organising principle is that **Monday does not ask for answers. Monday asks for owners.** A
document takes a week to produce and can be delayed forever without anyone being at fault. A name
and a date takes ninety seconds, is almost impossible to refuse in writing, and once given it
converts a vague request into an accountable one. Everything below is built to extract owners on
Monday and documents afterwards.

| Time | Route | Message | Asks for |
|------|-------|---------|----------|
| 08:05 | Account rep | **Email A** — PACCAR integration review | Interface register + two free entitlements |
| 08:10 | Internal | **Email C** — Tim, one paragraph | Authority on the record before anything lands |
| 09:30 | Account rep | **Call 1** — follow the email | Case number, owner name, date per item |
| 10:00 | eStore | Self-serve | Data Export Tool addendum, no rep required |
| 11:00 | CDK Heavy Truck | **Call 2** — 847-230-5715 | The truck-side contact who can actually answer |
| 11:30 | Heavy Truck desk | **Email B** — sent to whoever Call 2 names | The same register, from the side that knows it |
| 14:00 | PACCAR OEM contact | **Email D** — scorecard enquiry | The acceptance criteria, independent of CDK |
| 16:30 | Account rep | **Email E** — the confirmation | Writes down what was agreed. This is the enforcement |

Email F — the paperwork request — goes Wednesday, deliberately, and is covered in §8.

---

## 2. Email A — the account rep, 08:05

> **To:** [rep first name]
> **Cc:** Tim Hawkins
> **Subject:** PACCAR integration review — our CDK Drive environment (A173552 and related accounts)
>
> [First name],
>
> Luke Weatherbie at Peterbilt Atlantic, writing with Tim Hawkins's authority — Tim is copied.
>
> We're reviewing how our nine rooftops sit against PACCAR's dealer programs, and CDK Drive is the
> system in the middle of most of it. Before I take anything to our PACCAR contacts I want to be sure
> I'm describing our own environment accurately, and you'll know it better than we do.
>
> What I'm trying to establish is simple: which PACCAR interfaces we're actually running today, which
> ones are available to us and switched off, and where the gaps are that our people are currently
> covering by hand.
>
> 1. Which PACCAR integrations are included in our current subscription across the eight accounts
>    billed under invoice 10002236 — A173552, A192555, A193706, A240448, A299578, A173553, A173554
>    and A258188 — and which are separately licensed? A list per account would be ideal; a list for
>    the group is a fine start.
> 2. Do we have Managed Dealer Inventory running — the daily inventory and demand file, and the
>    Stock / MKT / COF order types coming back? If it's available and we're not on it, I'd like to
>    understand what turning it on involves.
> 3. Does CDK Drive produce the PACCAR month-end financial statement, and does it transmit to PACCAR
>    automatically, or is our controller still assembling and uploading it by hand? I'd like to stop
>    that being a manual job if it doesn't have to be.
> 4. Where do we stand on Parts Fleet Services — Service Gate invoice transmission and remittance
>    retrieval — and on the FOCUS customer and parts sales feed?
> 5. The electronic shipper integration was described as coming soon. Is it generally available now?
> 6. CDK publishes 80+ Heavy Truck OEM-specific integrations. Could I get the PACCAR subset of that
>    list? Not marketing material — the actual list, so I can plan against it.
> 7. For the interfaces we do have running: what's the transport, what's the schedule, and where does
>    a failure surface so our staff can see it? Is there a transmission log and retry history our
>    accounting team can look at directly?
>
> Two housekeeping items alongside it, both of which I believe are dealer entitlements at no licence
> fee, so they shouldn't need anything beyond your side:
>
> **8.** The Data Export Tool added to our Master Service Agreement across all of the accounts above
> rather than a single store. We'll generate the PGP key pair here — tell me where to send the public
> key.
>
> **9.** Dealer Data Exchange switched on for the same accounts, with the file layout and field
> documentation that comes with the data sets.
>
> I'll call you this morning to walk through it. On 8 and 9 I'd like those moving today. On 1 through
> 7 I don't need the answers today — I need a name and a date against each one by close of business,
> so I know each is owned.
>
> If any of this sits with the Heavy Truck team rather than with you, tell me who and I'll go to them
> directly rather than have it queue behind you.
>
> Thanks,
> Luke Weatherbie
> Peterbilt Atlantic

**Why 08:05.** It is the first thing in the inbox, before the day's escalations arrive, and it gives
the rep ninety minutes to read it before the call lands. A rep who has read the email and been called
about it is a rep who has already started working the problem. A rep who is called cold defers.

---

## 3. Email C — internal to Tim, 08:10

One paragraph. It exists so that Luke's authority is documented independently of the cc line, before
anyone at CDK or inside the dealership has a reason to question it.

> **To:** Tim Hawkins
> **Subject:** CDK — what's going out this morning
>
> Tim — going out to CDK this morning, under your authority as we discussed. I'm asking them to lay
> out which PACCAR integrations we're actually running across the group and which we're entitled to
> and not using, plus switching on two things that are free to us. Nothing in it commits us to
> anything or costs anything. I'll come back to you end of day with what they've owned. If anyone
> from CDK calls you directly, sending them back to me is the right answer.
>
> Luke

**Why it matters.** If the request is ever questioned internally, this paragraph — sent before the
fact, not after — is the record that it was authorised rather than freelanced. It costs one minute
and it removes the only structural vulnerability in the whole approach.

---

## 4. Call 1 — the account rep, 09:30

Fifteen minutes, maximum. The call has one job: convert nine written items into nine named owners.

**Open.** *"[First name] — Luke at Peterbilt Atlantic. I sent you something at eight this morning
about our PACCAR setup. Have you had a chance to look? No rush if not, I can walk you through it."*

**The frame, if asked why.** *"We're getting ourselves organised before we go back to PACCAR. I don't
want to walk in there describing our own systems wrong. You'd know better than I would what we've
actually got running."* — This is true, it is flattering, and it is the entire cover story. It needs
nothing else behind it.

**The three things to get, in order:**

1. **A case or ticket number.** Ask for it explicitly: *"can you raise this as a case so it has a
   number I can refer back to?"* An unnumbered request does not exist inside a vendor.
2. **Items 8 and 9 moving today.** *"Those two are free to us and I don't think they need anyone
   above you. Can you start those while we're on the phone?"* Ask him to do it during the call. It
   converts a queued task into a completed one, and it makes him feel useful early, which buys
   goodwill for the harder items.
3. **A name and a date against 1 through 7.** *"I'm not asking you to answer these today. I'm asking
   who owns each one and when I'll hear. If it's you for all seven, that's a fine answer."*

**If he deflects to the Heavy Truck team** — that is a win, not a setback. *"Perfect, who's the right
person there? Can you introduce me by email today, or should I call the inside sales line?"* Get a
name. That name is worth more than any of the seven answers.

**If he asks what you're building** — nothing is being built. *"Nothing yet. Honestly it started
because our controller is doing a month-end job by hand that I suspect the system does on its own,
and I couldn't get a straight answer internally about what we're paying for."* True, ordinary, and
it closes the topic.

**Do not say, on this call or ever:** extract, writeback, integration partner, third party, data
warehouse, Azure, migration, alternative, benchmark, Karmak, Procede, portability, ownership.

---

## 5. eStore, 10:00 — the route that needs nobody

The Data Export Tool is contracted through eStore as an addendum to the dealership's own Master
Service Agreement, licensed to the dealer at no licence fee. Luke opens eStore himself, immediately
after Call 1, and starts that addendum directly.

Three possible outcomes, and all three are useful:

- **It self-serves.** The rep's queue is now irrelevant to the ingestion date. Data starts moving this
  week regardless of what CDK's account team does.
- **It requires a signature.** Sign it same day. Note the counter-signature turnaround; that number is
  a useful measure of how CDK actually performs.
- **It is blocked or absent for these accounts.** Whatever blocks it names the gate — and that gate
  becomes item 10 on Wednesday's paperwork email, asked innocently: *"eStore doesn't show the Data
  Export Tool addendum for our accounts. Is that a permissions thing on our side?"*

---

## 6. Call 2 — CDK Heavy Truck inside sales, 11:00 — **847-230-5715**

This is the number [PACCAR Solutions' own integration guidance](https://support.paccar.decisiv.net/hc/en-us/articles/360034411713-What-is-Integration-and-How-Can-It-Make-My-Job-Easier)
tells dealers to call. A Peterbilt dealer phoning the truck-specific desk about PACCAR integration is
the most ordinary call in the industry.

This is the most valuable fifteen minutes of the day and the least likely to be recognised as such.
The general account team sells CDK Drive. The Heavy Truck desk knows what the PACCAR interfaces
actually do, which ones exist, and which ones CDK has never built. They will tell you, cheerfully,
because to them it is product knowledge rather than a disclosure.

**Open.** *"Hi — Luke Weatherbie, Peterbilt Atlantic, nine rooftops in Atlantic Canada, we're on CDK
Drive. I'm trying to work out where we stand on the PACCAR integrations and I don't think our account
rep is the right person. Is this the right desk?"*

**Lead with the financial statement question, not the inventory one.** *"The one I most want to
understand — does Drive produce the PACCAR month-end financial statement and send it up
automatically? Our controller's doing something by hand every month and I don't know whether she
needs to be."*

That question is operational, sympathetic, specific, and it is the exact interface Karmak names and
CDK's public record does not. The answer to it — whatever it is — is the single most valuable thing
obtainable on Monday, and it is obtainable for the price of a phone call by a dealer asking about its
own controller's workload.

**Then, in order:** Managed Dealer Inventory and the daily file. Service Gate and remittance. FOCUS.
The PACCAR subset of the 80+ list. Ask *"is that on the roadmap?"* about anything they say no to —
roadmap answers are freely given and tell you what CDK knows it lacks.

**Close with the name.** *"Who owns PACCAR integrations on your side? Can I email you directly if
something comes up?"*

---

## 7. Email B — the Heavy Truck desk, 11:30

Sent within thirty minutes of Call 2, to whoever it named, while the conversation is still warm.

> **To:** [name from Call 2]
> **Cc:** Tim Hawkins
> **Subject:** Following our call — PACCAR interfaces on our CDK Drive environment
>
> [Name],
>
> Thanks for the time this morning — genuinely more useful than I expected. Writing down what I
> think I heard so I don't misquote you internally, and adding the couple of things we didn't get to.
>
> My understanding from our call:
>
> - [what they said about the financial statement]
> - [what they said about MDI]
> - [what they said about Service Gate / FOCUS]
>
> If I've got any of that wrong, correct me — I'd rather be corrected now than repeat it to our
> PACCAR contacts.
>
> Two things to follow up:
>
> 1. The PACCAR subset of the Heavy Truck OEM integration list, as it applies to our accounts.
> 2. For anything we're entitled to and not currently using — what does switching it on involve, and
>    is there a cost?
>
> No urgency on either. I'd just like to know who to come back to.
>
> Thanks again,
> Luke Weatherbie
> Peterbilt Atlantic

**Why this email is the important one.** Writing back what they said, and inviting correction, does
three things at once. It creates a written record of verbal statements a vendor would never put in
writing unprompted. It makes correction feel helpful rather than adversarial, so corrections actually
arrive. And it establishes Luke as the sort of customer who listens and takes notes, which is the
customer vendors volunteer things to.

---

## 8. Email D — PACCAR, through the dealership's own OEM contact, 14:00

Entirely independent of CDK. It produces the acceptance criteria that CDK will eventually be measured
against, and it costs nothing to ask.

> **To:** [dealership's PACCAR / Peterbilt dealer contact]
> **Cc:** Tim Hawkins
> **Subject:** Our integration standing — where do we sit?
>
> [Name],
>
> Luke Weatherbie at Peterbilt Atlantic. We're taking a proper look at how well our systems are
> feeding PACCAR from our nine rooftops, and I'd rather measure ourselves against your yardstick than
> invent one.
>
> Three questions:
>
> 1. I understand there's an OEM integration scorecard for dealers. What does it measure, and where
>    does Peterbilt Atlantic currently sit on it?
> 2. Are there PACCAR programs we're eligible for that our current DMS setup isn't enabling? I'd
>    rather find out from you than discover it later.
> 3. Is there an interface specification available to dealers, as distinct from the one you'd give a
>    DMS vendor? Our people would find it useful to see what good looks like.
>
> Nothing behind this beyond wanting to be a better-run dealer group.
>
> Thanks,
> Luke Weatherbie

**Why it belongs on Monday and not later.** The scorecard is the acceptance test for everything
downstream. Knowing PACCAR's own measure of the dealership makes every subsequent CDK conversation
concrete — it stops being *"could you do more?"* and becomes *"here is our score, here is what moves
it."* A vendor argues with an opinion. A vendor does not argue with the OEM's scorecard.

---

## 9. Email E — the confirmation, 16:30. This is the enforcement.

Everything before this is conversation. This is what makes Monday binding. Sent to the rep, copying
Tim, on the original thread.

> **To:** [rep first name]
> **Cc:** Tim Hawkins
> **Subject:** Re: PACCAR integration review — where we landed today
>
> [First name],
>
> Writing down what we agreed this morning so we're both working from the same list.
>
> | Item | Owner | Expected |
> |------|-------|----------|
> | 1. PACCAR integrations by account | [name] | [date] |
> | 2. Managed Dealer Inventory status | [name] | [date] |
> | 3. Month-end financial statement | [name] | [date] |
> | 4. Service Gate / FOCUS | [name] | [date] |
> | 5. Electronic shipper availability | [name] | [date] |
> | 6. PACCAR subset of the integration list | [name] | [date] |
> | 7. Transport, schedule, failure visibility | [name] | [date] |
> | 8. Data Export Tool addendum | [name] | [status] |
> | 9. Dealer Data Exchange | [name] | [status] |
>
> Case number: [xxxx]. If I've recorded any of that wrong, correct me and I'll update it.
>
> Thanks for getting 8 and 9 moving today.
>
> Luke

**Why this is the whole approach in one message.** A table of owners and dates, sent to the person
who gave them and copied to the dealer principal, converts a helpful conversation into a commitment
that a named individual now has to either meet or explain. Nothing in it is aggressive. It reads as
diligence. It is the entire mechanism.

Leave blanks where nothing was committed — a blank row is more eloquent than a complaint, and it
invites the rep to fill it in himself.

---

## 10. Wednesday — Email F, the paperwork, deliberately dull

Separate thread. Copied to Tim **and** to the CFO. Different register entirely: no urgency, no
deadline pressure, extra time offered as a courtesy.

> **Subject:** Account paperwork — our file copies
>
> [First name],
>
> Separate from the integration questions — I'm getting our own files in order and I'm missing some
> things I should have on hand. Nothing urgent.
>
> 1. Our current Master Agreement with CDK, including all schedules and amendments, for each of the
>    accounts billed under invoice 10002236.
> 2. A written statement of the data-access entitlements currently active on each of those accounts.
>    Our March invoice shows no variable charges and I'd like that confirmed in writing.
> 3. An itemised billing export from the CDK Billing Center covering the last twelve months, per
>    account. Our mailed invoices are summarised now and no longer show what we're paying for.
>
> Take until the end of next week if that's easier — I'd rather have it complete than fast. If any of
> it sits with someone else, tell me who.
>
> Thanks,
> Luke

**Why Wednesday and why separate.** These are the items that read as an audit. Mixed into Monday's
integration email they would have poisoned its tone, routed the whole thread to the account team and
to legal, and made the CFO the natural owner of a conversation that should belong to Luke. Sent
alone, two days later, in a bored voice, they read as filing.

The offer of extra time is not politeness. It is what makes a thin or incorrect answer his to own —
accuracy was asked for over speed, and room was given to deliver it.

**Not asked, on Monday or Wednesday:** the fee schedule for extract and writeback access, and CDK's
process for authorising a dealer-designated integration partner. Those two questions, in one
sentence, tell a competent rep exactly what is being scoped. They are also premature — nothing can be
priced until the register is known. They wait until the register comes back, and depending on what it
says, they may be better put to PACCAR than to CDK.

---

## 11. If Monday close passes with nothing owned

Escalate on structure, never on tone. Each step is a reasonable thing for a customer to do, and each
one raises the cost of continued silence without a single word of complaint.

1. **Tuesday 09:00.** Reply on the same thread: *"Following up — I don't have owners against items 1
   to 7 yet. Even a name without a date is progress."* Nothing more.
2. **Tuesday 14:00.** *"If these sit better with the Heavy Truck team, say so and I'll take them
   there — I don't want them sitting in your queue on my account."* This offers him a graceful exit
   and simultaneously removes his monopoly on the request.
3. **Wednesday.** Work Email B instead. The Heavy Truck contact from Call 2 is now the primary route,
   and the account rep becomes a copy line rather than a gate.
4. **Thursday.** Tim sends one line to the rep's manager: *"Luke's been asking since Monday and
   hasn't got owners against a straightforward list. Who should he be talking to?"* Dealer principal
   to vendor management, no accusation, impossible to ignore.
5. **Any time.** PACCAR's answer to Email D arrives on its own clock and is unaffected by any of this.

The escalation never needs to become adversarial, because none of the asks were ever unreasonable.
That is the point of having made them reasonable.

---

## 12. Handling the answers without showing a card

**If the register comes back full** — CDK names MDI, financial statement transmission, Service Gate,
FOCUS and the rest, and shows them active — then the dealership is better integrated than the public
record suggested, §3 of the standard becomes a validated inventory, and the correct next move is to
use them properly rather than to build anything. Say so plainly and be pleased. That reaction is
genuine and it costs nothing.

**If the register comes back thin** — the likelier outcome, given CDK names four PACCAR items across
all of its public properties — do not point that out. Do not compare, do not mention another DMS, do
not express disappointment. The correct response is a single sympathetic question per gap:

> *"Understood. Is that on the roadmap at all, or is it something dealers usually handle another way?"*

That question is friendly, it invites CDK to describe its own gap in its own words, and the answer —
*"dealers usually handle that manually"* or *"that's not something we've built"* — is the finding.
Written by CDK, in CDK's voice, in reply to a dealer asking an innocent question. It is worth more
than any assertion made from outside, and it was obtained without a card being shown.

**If they ask, at any point, whether the dealership is looking at alternatives** — the answer is no,
and it is true. Nothing in this week's approach is a procurement exercise. It is a dealer group
establishing what it already owns before speaking to its OEM. Every question survives being
forwarded, quoted, or read aloud in a meeting Luke is not in.

---

## 13. Provenance

Question set and interface register from
[the PACCAR Feedback Standard, EgD-HAW-CDK-PLUG-001](https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/spec/).
Sequencing rationale from
[the outreach reframe, EgD-HAW-CDK-OUT-002](https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/outreach/).
Account numbers and the invoice reference from CDK invoice summary 10002236, dated 2026-03-31,
header account A173552 — eight accounts, CAD $19,842.75 current against a CAD $42,070.52 grand total.
The Heavy Truck inside-sales number is published in
[PACCAR Solutions' dealer integration guidance](https://support.paccar.decisiv.net/hc/en-us/articles/360034411713-What-is-Integration-and-How-Can-It-Make-My-Job-Easier).
The export route is documented in `docs/export-route.md` in this repository.

Two blanks remain and both are inside the dealership: the account rep's first name, and confirmation
of whether Luke signs Weatherbie or Weatherby.
