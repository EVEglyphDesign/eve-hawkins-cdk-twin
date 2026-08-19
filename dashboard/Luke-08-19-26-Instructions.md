# Luke 08-19-26 Instructions

**Where the money is, and where he expects to see it.**

Author · Luke Weatherbie ("Luke Skywalker" on the project team)
Recorded · 2026-08-19
Recorded by · Dany Thériault, EVEglyphDesign
For · Tim Hawkins · Peterbilt Atlantic
Companion to · [Customer Sphere Wireframe for Tim](https://eveglyphdesign.github.io/hawkins-twin-platform/customer-sphere/tim/) · [Customer Sphere v0.1 Review for Tobias](https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/dashboard/EVEglyphDesign_Customer_Sphere_v0.1_Review.pdf)

---

## The dedication

> On this day, August 19, 2026, Luke Weatherbie — otherwise known as Luke Skywalker on our project team — has provided us some very good guidance in how to show Tim the money.
>
> This is an important lifeline to the development team. Because what it tells them is: **this is where the money is, and this is where he expects to see it.** And that if we can frame the identification, the seeing, and the action in response, in a way that is enjoyable, we should have a lot of people wanting to work with it.
>
> For now, we only have to make one person happy. And that's Tim Hawkins. The rest of us serve at his pleasure.
>
> — Luke Weatherbie, 2026-08-19

Everything below is Luke's own signal, captured in his voice, grouped and preserved verbatim so the development team knows what to look for, what to ask, and where the dollars leak.

---

## 1. Parts

**Look for:** sales below matrix · obsolete / aged stock · high special-order ratio · uncredited core returns.

**Ask:**
- What % of invoices are below matrix, and who's overriding?
- What's our fill rate — stock vs. special order?
- What's the dollar value of parts with no movement in 12+ months?
- Are core credits being captured before the return window closes? **Flag when cores hit the system to be returned.**

## 2. Service

**Look for:** technician efficiency gaps · warranty under-billing or rejected claims · uncaptured shop supply / sublet · unexplained discounting by advisor.

**Ask:**
- What's our flag-hours vs. clock-hours efficiency by tech and by location?
- Is our warranty labor rate below what the manufacturer allows?
- What % of ROs carry a shop supply / sublet line, and is that consistent across advisors?
- Which advisor has the highest average discount per RO?

## 3. Warranty capture on units already in the shop

> Where can we capture more warranty work on units when they are in the shop? We could possibly upload warranty plans into the model for this.

The plan-upload path is the load-bearing idea: if the twin holds each unit's warranty coverage, the shop-visit trigger becomes automatic — every RO opened on an in-warranty unit checks against the coverage table before the customer pays out of pocket.

## 4. Customers who disappeared

> Customers who have disappeared — I think that is covered in what Tobias has already drafted.

Confirmed. That signal is [Screen 2 of the Customer Sphere Wireframe v0.1](https://eveglyphdesign.github.io/hawkins-twin-platform/customer-sphere/tim/) — the 228-day silence gap and the four "worth a phone call this week" tiles. **No duplication needed here.** The sphere already reports the absence.

## 5. Service retention — first visit → repeat visits

**Look for:** customers who service once and never return · gaps between recommended and actual next-visit intervals · no-shows on scheduled appointments.

**Ask:**
- What % of first-time service customers return within their next service interval?
- How many customers are overdue for scheduled maintenance with no follow-up contact logged?
- What's our appointment no-show rate, and is anyone rebooking those customers?

## 6. Declined / deferred work

**Look for:** recommended repairs that were declined and never revisited · safety-related items that lapse without a follow-up.

**Ask:**
- What's the dollar value of declined work sitting in the system right now?
- Is there a process to re-contact customers on declined items at the next visit, or does it just disappear from the RO?

## 7. Warranty and maintenance-contract expirations

**Look for:** extended warranties or maintenance plans expiring with no renewal outreach · customers who fall out of warranty and immediately stop coming in.

**Ask:**
- Who has a warranty or PM contract expiring in the next 60–90 days, and is anyone reaching out before it lapses?
- What % of customers renew vs. walk after expiration?

## 8. Fleet and commercial accounts — Peterbilt-specific

**Look for:** fleet accounts with declining unit counts serviced · accounts that haven't been touched by a rep in months · service-level slippage (turnaround time) on key accounts.

**Ask:**
- Which fleet accounts have reduced their visit frequency or spend year-over-year?
- Do our top accounts have a named contact checking in regularly, or is it purely reactive?
- Are we losing fleet work to a competitor because of turnaround time?

## 9. Customer experience and complaints

**Look for:** negative reviews or CSI scores with no documented resolution · repeat complaints from the same customer · complaints that never reach a manager.

**Ask:**
- What's our CSI trend by location, and are low scores tied to a specific advisor or process?
- Is there a closed-loop process for a customer complaint — logged, resolved, and followed up — or does it end at "we fixed the car"?

## 10. Service throughput — the sold-hour question

> How many hours in the service dept do we need to sell a day, week, month, year — per tech, per rooftop?

This is the daily control for the service floor. Twin surfaces it as a per-tech and per-rooftop panel with the target on one axis and the sold-hours on the other, in day / week / month / year windows.

## 11. Effective labor rate

> What are effective labor rates per tech, per rooftop?

Effective labor rate = (total labor revenue) ÷ (total flag hours sold). Twin surfaces the delta between the door rate and the effective rate — that gap is discounting, warranty write-downs, and uncaptured sublet compressed into one number.

## 12. Expense exceptions

> Exceptions in expenses, both fixed and semi — accounting exceptions.

The twin's job on the expense side is to flag the row that does not fit — a January utility bill that is triple December's, a rent posting to the wrong CMF, a supplier the dealership has never used before. Not a report. A list of rows that need eyes.

## 13. Floor-plan aging

> Flooring dates and when units will be coming off of those floor plans.

Every unit on the lot has an in-date and a curtailment schedule. Twin surfaces the coming-due window (30 / 60 / 90 days) so the unit is either sold, moved, or paid down before the interest step-up hits.

## 14. Collections

> Difficult collection customers flagged.

The customer sphere already sees the FINAL NOTICE / COLLECTIONS chain (Screen 2 of the Wireframe). This section names it as a first-class list rather than an incident on one customer card: **the collections worklist**, ranked by dollars aged, with the last three touch-points on each row and the desk that owns the next call.

## The struck line

> ~~What if I had a company-wide survey go out asking some simple stuff — what are your major time killers during the day, things like that — that we could then look at trying to fold into this and be able to disperse it out amongst staff in smaller pieces? Obviously, they don't know the scope of it.~~
>
> Strike that one from the record. That's something dumb-dumb I can do with HR to make them feel like they're involved. — Luke, 2026-08-19

Preserved crossed-out for the audit trail; the twin will not solicit staff input for the operator dashboard. If the survey happens later through HR, its output is a separate document that the twin can ingest, not drive.

---

## What this changes for the development team

Luke has given us the **cause-of-loss checklist** — the specific signals a working dealer principal expects the dashboard to surface without being asked. Every item in §§1–14 maps to an already-planned extract from CDK, plus one new source (PACCAR warranty plans, §3). This document is the plain-English brief that pairs with the ATD 60-COV extraction targets in [`EXTRACTION-STAGING.md`](https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin/blob/main/dashboard/EXTRACTION-STAGING.md).

Concretely, the extraction plan grows by seven exception surfaces that were not in v0.1:

1. **Below-matrix parts sales** — invoice-line override register (parts kind, override user, dollar delta vs. matrix).
2. **Aged parts inventory** — parts master × last-movement date × on-hand extended value, banded 12m / 18m / 24m+.
3. **Core-return watchdog** — cores accepted × return window × credit posting; alert when the window is 14 days from close.
4. **RO shop-supply consistency** — RO header × advisor × supply/sublet line presence rate; per-advisor deviation from the rooftop average.
5. **Declined-work register** — RO estimate lines with status=declined × dollar value × age × next-visit flag.
6. **Contract-expiration outreach** — warranty and PM contract expiration × 60/90-day window × last customer touch.
7. **Floor-plan curtailment** — unit inventory × floor-plan in-date × curtailment schedule × interest step-up date.

These are additive to the eight-stage extraction order already defined in the staging document, not a replacement. Each one becomes a `twin.doc(kind=…)` extension or a computed view on the existing `kind='invoice'` shape — the sphere absorbs them without a migration.

---

*Recorded verbatim from Luke Weatherbie's guidance to the project team, 2026-08-19. Preserved because the development team needs to hear it in his voice.*

*Pour le bien-être du peuple.*
