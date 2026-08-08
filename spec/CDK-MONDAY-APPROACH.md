# The CDK Monday Runbook

---

## Before you start

Fill these three blanks and the day runs without further preparation.

- **[REP]** — CDK account rep's first name
- **[PACCAR]** — the dealership's PACCAR / Peterbilt dealer contact
- Confirm Luke signs **Weatherbie** or **Weatherby**

Eight locations, five provinces: Hanwell, Moncton, Dartmouth, Kentville, Charlottetown, Deer Lake,
Saint-Pascal, Saint-Louis-du-Ha! Ha!
Eight CDK accounts on invoice 10002236: A173552, A192555, A193706, A240448, A299578, A173553,
A173554, A258188.

| Time | Do this |
|------|---------|
| 07:30 | **Generate the PGP key pair.** Nothing else can start until this exists |
| 07:45 | **eStore** — start the Data Export Tool addendum and Dealer Data Exchange yourself |
| 08:05 | Send **Email A** to [REP], cc Tim |
| 08:10 | Send **Email B** to Tim |
| 09:30 | **Call 1** — [REP] |
| 11:00 | **Call 2** — CDK Heavy Truck inside sales, **847-230-5715** |
| 11:30 | Send **Email C** to whoever Call 2 named |
| 14:00 | Send **Email D** to [PACCAR] |
| 16:30 | Send **Email E** to [REP], cc Tim |
| Wednesday | Send **Email F** to [REP], cc Tim and the CFO |

---

## 07:30 — the key

The extract cannot be switched on without a public key to send. Generate it before anything else so
nothing waits on it later in the day.

```
gpg --batch --gen-key <<EOF
Key-Type: RSA
Key-Length: 4096
Name-Real: Peterbilt Atlantic
Name-Email: [Luke's work address]
Expire-Date: 0
%no-protection
EOF
gpg --armor --export "Peterbilt Atlantic" > peterbilt-atlantic-public.asc
```

Export the private key and put it somewhere the dealership controls and Luke is not the only holder
of — not a laptop, not a chat window. Attach `peterbilt-atlantic-public.asc` to Email A.

---

## 07:45 — eStore. Start the extract first.

The Data Export Tool and Dealer Data Exchange are dealer entitlements at no licence fee. They do not
depend on the PACCAR questions, on [REP], or on anything said in any call. Starting them at 07:45
means the clock on the only item that actually moves data begins before CDK knows the day has
started, and it never enters the rep's queue.

Open eStore and start the Data Export Tool addendum against the Master Service Agreement — for **all
eight accounts**, not a single store. Then Dealer Data Exchange for the same accounts.

- **Self-serves** → sign it, done. Note the timestamp. Item 8 is closed before the first email goes.
- **Needs counter-signature** → sign same day, and Email A asks who counter-signs and when.
- **Blocked or missing for these accounts** → screenshot it, write down the exact message. That
  message becomes item 8 in Email A, worded as a permissions question rather than a request:
  *"eStore doesn't show the Data Export Tool addendum against our accounts. Is that a permissions
  thing on our side, or does it need to be added centrally?"*

Everything after this is paperwork behind a clock that is already running.

---

## Email A — 08:05

**To:** [REP] **Cc:** Tim Hawkins
**Subject:** PACCAR integration review — our CDK Drive environment (A173552 and related accounts)

[REP],

Luke Weatherbie at Peterbilt Atlantic, writing with Tim Hawkins's authority — Tim is copied.

We're reviewing how our eight locations sit against PACCAR's dealer programs, and CDK Drive is the
system in the middle of most of it. Before I take anything to our PACCAR contacts I want to be sure
I'm describing our own environment accurately, and you'll know it better than we do.

What I need to establish: which PACCAR interfaces we're running today, which are available to us and
switched off, and where the gaps are that our people are covering by hand.

1. Which PACCAR integrations are included in our current subscription across the eight accounts
   billed under invoice 10002236 — A173552, A192555, A193706, A240448, A299578, A173553, A173554 and
   A258188 — and which are separately licensed? A list per account would be ideal; a list for the
   group is a fine start.
2. Do we have Managed Dealer Inventory running — the daily inventory and demand file, and the
   Stock / MKT / COF order types coming back? If it's available and we're not on it, what does
   turning it on involve?
3. Does CDK Drive produce the PACCAR month-end financial statement, and does it transmit to PACCAR
   automatically, or is our controller assembling and uploading it by hand?
4. Where do we stand on Parts Fleet Services — Service Gate invoice transmission and remittance
   retrieval — and on the FOCUS customer and parts sales feed?
5. The electronic shipper integration was described as coming soon. Is it generally available now?
6. CDK publishes 80+ Heavy Truck OEM-specific integrations. Could I get the PACCAR subset of that
   list? Not marketing material — the actual list, so I can plan against it.
7. For the interfaces we do have running: what's the transport, what's the schedule, and where does a
   failure surface so our staff can see it? Is there a transmission log and retry history our
   accounting team can look at directly?

Two housekeeping items I've already started this morning, both dealer entitlements at no licence fee:

**8.** I started the Data Export Tool addendum against our Master Service Agreement in eStore first
thing — across all of the accounts above rather than a single store. Our public key is attached. Tell
me where it goes, who counter-signs, and whether anything on the addendum needs to change to cover
all eight accounts. *[If eStore blocked it: "eStore doesn't show the Data Export Tool addendum against
our accounts — is that a permissions thing on our side, or does it need to be added centrally?"]*

**9.** Dealer Data Exchange for the same accounts. I'd like the file layout and field documentation
that comes with the data sets sent over alongside it.

I'll call you this morning to walk through it. On 8 and 9 I've done my side — I need yours today. On
1 through 7 I don't need answers today, I need a name and a date against each one by close of
business.

If any of this sits with the Heavy Truck team rather than with you, tell me who and I'll go to them
directly rather than have it queue behind you.

Thanks,
Luke Weatherbie
Peterbilt Atlantic

---

## Email B — 08:10, internal

**To:** Tim Hawkins
**Subject:** CDK — what's going out this morning

Tim — going out to CDK this morning under your authority. I'm asking them to lay out which PACCAR
integrations we're running across the group and which we're entitled to and not using, plus switching
on two things that are free to us. Nothing in it commits us to anything or costs anything. I'll come
back to you end of day with what they've owned. If anyone from CDK calls you directly, sending them
back to me is the right answer.

Luke

---

## Call 1 — 09:30, [REP]. Fifteen minutes.

**Get three things: a case number, item 9 switched on while you're on the phone, and a name and date
against 1–7.** Item 8 is already started — you're confirming his side of it, not asking for it.

> "[REP] — Luke at Peterbilt Atlantic. I sent you something at eight this morning about our PACCAR
> setup. Have you had a chance to look? No rush if not, I can walk you through it."

If asked why:

> "We're getting ourselves organised before we go back to PACCAR. I don't want to walk in there
> describing our own systems wrong. You'd know better than I would what we've actually got running."

Get the case number:

> "Can you raise this as a case so it has a number I can refer back to?"

Close out 8 and 9 now, not queued:

> "I started the export addendum in eStore this morning and sent you our public key. Both of those
> are free to us and I don't think they need anyone above you. Can you finish them off while we're on
> the phone?"

Get owners:

> "I'm not asking you to answer these today. I'm asking who owns each one and when I'll hear. If it's
> you for all seven, that's a fine answer."

If he deflects to the Heavy Truck team — take it:

> "Perfect, who's the right person there? Can you introduce me by email today, or should I call the
> inside sales line?"

If he asks what you're building:

> "Nothing. Honestly it started because our controller is doing a month-end job by hand that I
> suspect the system does on its own, and I couldn't get a straight answer internally about what
> we're paying for."

**Never say:** extract · writeback · integration partner · third party · data warehouse · Azure ·
migration · alternative · benchmark · Karmak · Procede · portability · ownership.

---


## Call 2 — 11:00, CDK Heavy Truck inside sales, **847-230-5715**

This desk knows what the PACCAR interfaces do. The account team does not.

> "Hi — Luke Weatherbie, Peterbilt Atlantic, eight locations across Atlantic Canada and eastern
> Quebec, we're on CDK Drive. I'm trying to work out where we stand on the PACCAR integrations and I
> don't think our account rep is the right person. Is this the right desk?"

Lead with this one:

> "The one I most want to understand — does Drive produce the PACCAR month-end financial statement
> and send it up automatically? Our controller's doing something by hand every month and I don't
> know whether she needs to be."

Then, in order: Managed Dealer Inventory and the daily file · Service Gate and remittance · FOCUS ·
the PACCAR subset of the 80+ list.

On anything they say no to:

> "Is that on the roadmap at all?"

Close:

> "Who owns PACCAR integrations on your side? Can I email you directly if something comes up?"

Write the answers down during the call. They go into Email C.

---

## Email C — 11:30

**To:** [name from Call 2] **Cc:** Tim Hawkins
**Subject:** Following our call — PACCAR interfaces on our CDK Drive environment

[Name],

Thanks for the time this morning. Writing down what I think I heard so I don't misquote you
internally, and adding the couple of things we didn't get to.

My understanding from our call:

- [financial statement — what they said]
- [Managed Dealer Inventory — what they said]
- [Service Gate / FOCUS — what they said]

If I've got any of that wrong, correct me — I'd rather be corrected now than repeat it to our PACCAR
contacts.

Two to follow up:

1. The PACCAR subset of the Heavy Truck OEM integration list, as it applies to our accounts.
2. For anything we're entitled to and not currently using — what does switching it on involve, and is
   there a cost?

No urgency on either. I'd just like to know who to come back to.

Thanks again,
Luke Weatherbie
Peterbilt Atlantic

---

## Email D — 14:00

**To:** [PACCAR] **Cc:** Tim Hawkins
**Subject:** Our integration standing — where do we sit?

[Name],

Luke Weatherbie at Peterbilt Atlantic. We're taking a proper look at how well our systems are feeding
PACCAR from our eight locations, and I'd rather measure ourselves against your yardstick than invent
one.

Three questions:

1. I understand there's an OEM integration scorecard for dealers. What does it measure, and where
   does Peterbilt Atlantic currently sit on it?
2. Are there PACCAR programs we're eligible for that our current DMS setup isn't enabling?
3. Is there an interface specification available to dealers, as distinct from the one you'd give a
   DMS vendor? Our people would find it useful to see what good looks like.

Nothing behind this beyond wanting to be a better-run dealer group.

Thanks,
Luke Weatherbie

---

## Email E — 16:30. This is the one that makes Monday stick.

**To:** [REP] **Cc:** Tim Hawkins
**Subject:** Re: PACCAR integration review — where we landed today

[REP],

Writing down what we agreed this morning so we're both working from the same list.

| Item | Owner | Expected |
|------|-------|----------|
| 1. PACCAR integrations by account | | |
| 2. Managed Dealer Inventory status | | |
| 3. Month-end financial statement | | |
| 4. Service Gate / FOCUS | | |
| 5. Electronic shipper availability | | |
| 6. PACCAR subset of the integration list | | |
| 7. Transport, schedule, failure visibility | | |
| 8. Data Export Tool addendum | | |
| 9. Dealer Data Exchange | | |

Case number: [xxxx]. If I've recorded any of that wrong, correct me and I'll update it.

Thanks for getting 8 and 9 moving today.

Luke

**Leave blank rows blank.** Do not fill them in charitably and do not comment on them.

---

## Email F — Wednesday. Separate thread.

**To:** [REP] **Cc:** Tim Hawkins, [CFO]
**Subject:** Account paperwork — our file copies

[REP],

Separate from the integration questions — I'm getting our own files in order and I'm missing some
things I should have on hand. Nothing urgent.

1. Our current Master Agreement with CDK, including all schedules and amendments, for each of the
   accounts billed under invoice 10002236.
2. A written statement of the data-access entitlements currently active on each of those accounts.
   Our March invoice shows no variable charges and I'd like that confirmed in writing.
3. An itemised billing export from the CDK Billing Center covering the last twelve months, per
   account. Our mailed invoices are summarised and no longer show what we're paying for.
4. Please confirm which physical location each of the eight accounts corresponds to — A173552,
   A192555, A193706, A240448, A299578, A173553, A173554 and A258188 — against our eight locations at
   Hanwell, Moncton, Dartmouth, Kentville, Charlottetown, Deer Lake, Saint-Pascal and
   Saint-Louis-du-Ha! Ha! Where an account covers more than one location, or covers none, please say
   so.
5. A173553 is labelled as the Moncton branch and carries $21.50 in monthly recurring charges, against
   $1,600 to $2,000 on our other operating accounts. Is Moncton's DMS billed through another account,
   and if so which one?

Take until the end of next week if that's easier — I'd rather have it complete than fast. If any of
it sits with someone else, tell me who.

Thanks,
Luke

---

## If close of business passes with nothing owned

- **Tuesday 09:00** — same thread: *"Following up — I don't have owners against items 1 to 7 yet.
  Even a name without a date is progress."* Nothing more.
- **Tuesday 14:00** — *"If these sit better with the Heavy Truck team, say so and I'll take them
  there — I don't want them sitting in your queue on my account."*
- **Wednesday** — work the Call 2 contact instead. [REP] becomes a copy line.
- **Thursday** — Tim, one line to the rep's manager: *"Luke's been asking since Monday and hasn't got
  owners against a straightforward list. Who should he be talking to?"*

---

## When the answers come back

Do not compare, do not name another DMS, do not express disappointment. One question per gap:

> "Understood. Is that on the roadmap at all, or is it something dealers usually handle another way?"

If asked whether the dealership is looking at alternatives, the answer is no.
