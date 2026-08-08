# The CDK Outreach, Reframed

---

## 1. Why it needed reframing

The version on the record — v5, seven numbered items, sent under Luke Weatherbie's name with Tim
Hawkins and the CFO copied — is a good email. It is specific, it is entitled, it is enforceable,
and it correctly separates the three free items from the four that require CDK to produce paperwork.
Nothing in it is wrong.

What has changed is not the email. It is what is now known behind it.

At the time v5 was written, the dealership's PACCAR integration surface was an unknown. It is no
longer. The register in
[the PACCAR Feedback Standard](https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/spec/)
reconstructs fourteen PACCAR interfaces from Karmak's and Procede's own public documentation, isolates
the seven that carry dealer data *back up* to the OEM, and measures CDK's published record against
them. CDK names four PACCAR items across all of its public properties. Karmak names thirteen.
Missing from CDK's public record entirely: Managed Dealer Inventory, financial statement transmission,
FOCUS, Service Gate, PacLease RPS, and the loyalty card feed.

That changes the strongest available posture from **"send me my paperwork"** to **"help us understand
where we stand with PACCAR."** The second one is warmer, harder to refuse, routes to a different and
more useful part of CDK, and — this is the part that matters — obtains the same information as the
first, because the answers to fourteen integration questions *are* an entitlement statement.

### The structural fault in v5

v5 does two jobs with opposite emotional registers in a single email.

- **Items 4, 5, 6** are operational and warm. A dealer asking to switch on a free entitlement.
- **Items 1, 2, 3, 7** are procurement and cold. A dealer asking for its Master Agreement, an
  itemised twelve-month billing export, and a fee schedule.

A rep reading items 1–3 hears an audit. An audit gets routed to the account team and to legal, it
gets a considered rather than a helpful reply, and it makes the CFO the natural owner of the thread —
which is the one outcome the cc structure was designed to avoid. The warm items then wait behind the
cold ones.

**The reframe separates them.** The integration conversation goes to the truck side of CDK and stays
technical and enthusiastic. The paperwork request goes separately, later, and boring.

---

## 2. v5 — as sent, for comparison

> **To:** [rep first name]
> **Cc:** Tim Hawkins, Peter [CFO]
> **From:** Luke Weatherbie, Peterbilt Atlantic
> **Subject:** Data access and documentation request — Peterbilt Atlantic group (A173552 and related accounts)
>
> [First name],
>
> I'm writing on behalf of Peterbilt Atlantic, with Tim Hawkins's authority, regarding our CDK Drive
> environment across the group's rooftops. Tim is copied here.
>
> We're improving how our service and parts teams see a customer across all of our locations, which
> means combining our CDK business data with our other operating systems. The goal is that a customer
> gets an answer the first time they ask, whichever rooftop they call. Today that information is
> fragmented and our people are working around it.
>
> Seven items. I've kept them separate deliberately so nothing gets missed.
>
> 1. Our current Master Agreement with CDK, including all schedules and amendments, for each of the
>    accounts billed under invoice 10002236 — A173552, A192555, A193706, A240448, A299578, A173553,
>    A173554 and A258188.
> 2. A written statement of the data-access entitlements currently active on each of those accounts —
>    any extract feeds, writeback packages or API subscriptions.
> 3. An itemised billing export from the CDK Billing Center covering the last twelve months, per account.
> 4. The Data Export Tool added to our Master Service Agreement.
> 5. Dealer Data Exchange switched on for the same accounts.
> 6. The file layout and field documentation that comes with the export data sets.
> 7. Your current fee schedule for extract and writeback access, and your documented process for
>    authorising a dealer-designated integration partner.
>
> [closing — call this afternoon, items 4/5/6 moving today or Monday, owner name and date against
> each documentation item by close of business Monday 10 August]

**What it gets right:** Luke's authority in the first line. Real account numbers. Free items sitting
among paid ones so the rep can look responsive immediately. A close that asks only for a name and a
date, which is nearly impossible to refuse.

**What it costs:** item 7 names "extract," "writeback," and "integration partner" in one sentence.
That is the closest thing in the email to a card. A competent rep reads item 7 and understands that
Peterbilt Atlantic is scoping a third party against the CDK data layer, and that understanding
arrives before any relationship has been built on the truck side.

---

## 3. v6 — the reframe

> **To:** [rep first name]
> **Cc:** Tim Hawkins
> **From:** Luke Weatherbie, Peterbilt Atlantic
> **Subject:** PACCAR integration review — our CDK Drive environment (A173552 and related accounts)
>
> [First name],
>
> Luke Weatherbie at Peterbilt Atlantic, writing with Tim Hawkins's authority — Tim is copied.
>
> We're doing a review of how our nine rooftops sit against PACCAR's dealer programs, and CDK Drive is
> the system in the middle of most of it. Before I take anything to our PACCAR contacts I want to be
> sure I'm describing our own environment accurately, and you'll know it better than we do.
>
> What I'm trying to establish is straightforward: which PACCAR interfaces we're actually running
> today, which ones are available to us and switched off, and where the gaps are that our people are
> currently covering by hand.
>
> Specifically:
>
> 1. Which PACCAR integrations are included in our current subscription across the eight accounts
>    billed under invoice 10002236 — A173552, A192555, A193706, A240448, A299578, A173553, A173554
>    and A258188 — and which are separately licensed? A list per account would be ideal; a list for
>    the group is a fine start.
> 2. Do we have Managed Dealer Inventory running — the daily inventory and demand file, and the
>    Stock / MKT / COF order types coming back? If it's available and we're not on it, I'd like to
>    understand what turning it on involves.
> 3. Does CDK Drive produce the PACCAR month-end financial statement, and does it transmit to PACCAR
>    automatically, or is our controller still assembling and uploading that by hand? I'd like to stop
>    that being a manual job if it doesn't have to be.
> 4. Where do we stand on Parts Fleet Services — Service Gate invoice transmission and remittance
>    retrieval — and on the FOCUS customer and parts sales feed?
> 5. The electronic shipper integration was described as coming soon. Is it generally available now?
> 6. CDK publishes 80+ Heavy Truck OEM-specific integrations. Could I get the PACCAR subset of that
>    list? Not marketing material — the actual list, so I can plan against it.
> 7. For the interfaces we do have running: what's the transport, what's the schedule, and where does
>    a failure surface so our staff can see it? Is there a transmission log and a retry history our
>    accounting team can look at directly?
>
> Two housekeeping items alongside it, both of which I believe are dealer entitlements at no licence
> fee, so they shouldn't need anything beyond your side:
>
> **8.** The Data Export Tool added to our Master Service Agreement across all of the accounts above
>    rather than a single store. We'll generate the PGP key pair here — tell me where to send the
>    public key.
>
> **9.** Dealer Data Exchange switched on for the same accounts, with the file layout and field
>    documentation that comes with the data sets.
>
> I'll call you this afternoon to walk through it. On 8 and 9 I'd like those moving today or Monday
> morning. On 1 through 7, I don't need the answers by Monday — I need a name and a date against each
> one by close of business Monday 10 August, so I know it's owned.
>
> If any of this sits with the Heavy Truck team rather than with you, tell me who and I'll go to them
> directly rather than have it queue behind you.
>
> Thanks,
> Luke Weatherbie
> Peterbilt Atlantic

---

## 4. What moved, and why

| # | Change | Reason |
|---|--------|--------|
| 1 | Subject line: "Data access and documentation request" → "PACCAR integration review" | The first is a demand notice; the second is a customer doing diligence on its own operation. The second gets opened by someone who wants to help. |
| 2 | The CFO comes off the cc | v5 copied Peter so the Master Agreement request would be visible internally. v6 does not ask for the Master Agreement, so there is no reason to hand him the thread. Tim's cc alone still carries the authority. |
| 3 | Master Agreement, billing export, entitlement statement — all removed | These are the audit-register items. They go in a separate, later, deliberately dull email. Keeping them here poisons the tone of everything above them. |
| 4 | Item 7 of v5 — fee schedule and integration-partner process — **removed entirely** | This was the only sentence in v5 that showed a card. It asks CDK to price third-party access to its data layer, which tells a competent rep exactly what is being scoped. It is also not needed yet: nothing can be priced until the register in §1–7 is known. |
| 5 | Seven new questions, all about PACCAR interfaces | Sourced from the register. Each names a specific interface Karmak publishes and CDK does not, so a thin answer is self-evidently thin without any accusation being made. |
| 6 | The free entitlements demoted to items 8 and 9, under "housekeeping" | In v5 they were the operational core. In v6 they are a footnote to a bigger conversation — which lowers their salience, makes them trivially easy to approve, and removes the impression that the export tool is the point of the email. |
| 7 | "Combining our CDK business data with our other operating systems" — removed | True, but it is the sentence that plants *integration project* in the reader's mind. v6 gives a reason that is equally true and entirely internal: getting our own environment described accurately before we talk to PACCAR. |
| 8 | Closing adds an explicit route to the Heavy Truck team | v5 invited redirection generally. v6 names the destination, because the truck side is where the useful answers live and where the relationship is worth building. |
| 9 | The 24-hour posture is preserved intact | Call the same afternoon. Free items today or Monday morning. Name and date per item by Monday close. Unchanged from v5, because it was right. |

---

## 5. Where the removed items go

Nothing is abandoned. It is sequenced.

**Email B — the dull one.** Sent separately, on its own thread, ideally a day or two later, copied to
Tim and to the CFO. Master Agreement with all schedules and amendments per account. Written statement
of active data-access entitlements. Itemised twelve-month billing export from the Billing Center.
Framed as annual file-hygiene: *"I need our own paperwork on file properly."* No urgency, no
deadline drama, extra days offered as a courtesy. It reads as a GM tidying a filing cabinet — which
is exactly how the Lightspeed equivalent was already framed, and for the same reason.

**The fee schedule and the partner-authorisation process — later, and possibly never from CDK.**
Ask this only once the register is known. If CDK's answers to v6 items 1–7 come back strong, the
register becomes a validated inventory and the pricing question has a real shape. If they come back
thin, the register becomes the gap analysis and the question is better put to PACCAR through the
dealer's own OEM contact, where it costs nothing and reveals nothing.

**Three questions belong to PACCAR, not CDK.** The scorecard dimensions and Peterbilt Atlantic's
current standing; which PACCAR programs the dealership is eligible for that its DMS configuration
does not enable; and whether a dealer-facing interface specification exists as distinct from a
vendor-facing one. Karmak's own FAQ confirms a PACCAR OEM integration scorecard exists. That
scorecard is the acceptance test for everything downstream, and it is obtainable from PACCAR by a
dealer simply asking about its own score.

---

## 6. The 24-hour sequence

The email is one of four routes opened the same afternoon, none of which depends on the others.

1. **The rep.** v6 goes out, Luke calls within the hour. Get a case number, an owner name and a date
   per item. Same-day one-paragraph email back recording what was agreed. That written record is what
   makes Monday enforceable.
2. **eStore, directly.** The Data Export Tool is contracted through eStore as an addendum to the
   dealership's own Master Service Agreement. Luke opens it himself the same afternoon. If it
   self-serves, the rep's queue is irrelevant to the ingestion date. If it blocks, whatever blocks it
   names the gate.
3. **CDK Heavy Truck inside sales — 847-230-5715.** The number
   [PACCAR Solutions' own integration guidance](https://support.paccar.decisiv.net/hc/en-us/articles/360034411713-What-is-Integration-and-How-Can-It-Make-My-Job-Easier)
   tells dealers to call. A Peterbilt dealer calling the truck-specific desk about PACCAR integration
   is the most ordinary call in the industry, and it reaches people who can actually answer items 2,
   3 and 4.
4. **PACCAR, through the dealership's own OEM contact.** The three scorecard questions. Independent
   of CDK entirely, and it produces the acceptance criteria CDK will eventually be measured against.

By Monday morning: a case number, an eStore answer, a truck-side contact, and a PACCAR scorecard
enquiry in flight — instead of one email sitting in one queue.

---

## 7. What is deliberately absent from v6

No mention of sovereignty, data rights, ownership, portability, or the litigation history. No mention
of a third party, an integration partner, a platform, a warehouse, or Azure. No comparison to Karmak
or Procede, and no indication that a comparison has been run. No suggestion that CDK might be
replaced, supplemented, or bypassed. No pricing question. No fee schedule.

Every question in v6 is one a Peterbilt dealer would ask if it had never heard of any of that, and
every answer improves the dealership's operation whether or not anything else is ever built. That is
a true statement, and it is what makes this posture sustainable rather than a tactic — it survives
being forwarded, quoted, or read aloud in a meeting Luke is not in.

Written on the assumption that every word is read by the CFO, by the rep's manager, and eventually
by CDK's legal team. It holds up under all three readings.

---

## 8. Open blanks before sending

- The rep's first name.
- **Surname spelling.** The record holds both "Weatherbie" and "Weatherby." Confirm which he signs.
- Rooftop count. The group is described as nine rooftops; invoice 10002236 covers eight accounts and
  seven rooftops. v6 says "nine rooftops" in the opening and "eight accounts" in item 1 — confirm
  both are correct as written, or reconcile before sending.
- Whether v5 has already gone. If it has, v6 is not a replacement — it is the second contact, sent to
  the Heavy Truck desk rather than the account rep, and the opening line becomes *"separately from
  the account paperwork I asked [rep] for, I'm working on something on the PACCAR side."*

---

## 9. Provenance

Reframed against
[the PACCAR Feedback Standard, EgD-HAW-CDK-PLUG-001](https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/spec/),
whose §3 register and §9 question set supply items 1 through 7. v5 is reproduced from the drafting
session of 2026-08-07. CDK's published PACCAR record was read from
[the CDK Heavy Truck OEM integrations page](https://www.cdkglobalheavytruck.com/oem-integrations)
and [the Heavy Truck OEM newsletter](https://www2.cdkglobal.com/ht-oem). The incumbent register
derives from [Karmak's PACCAR integrations page](https://www.karmak.com/integrations/paccar) and
[the Fusion 3.59 cumulative release notes](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf).

No confidential CDK material was used in constructing v6. Every question in it is answerable from
CDK's own account records and asks about the dealership's own environment.
