# Luke 08-19-26 Warranty-Bot Recap

**A little warranty bot.** Off-the-record recap of a call between Dany Thériault and Luke Weatherbie, 2026-08-19, recorded because *we don't have the meeting on record and I want to recap it.* The idea started as §3 of Luke's Instructions the same day (*where can we capture more warranty work on units when they are in the shop*), and grew — on the call — into a warranty bot the service advisor talks to before the customer walks in.

Author of the artifact · Dany Thériault, EVEglyphDesign
Participants · Luke Weatherbie · Dany Thériault
Date · 2026-08-19
For · Tim Hawkins · Peterbilt Atlantic
Companion to · [Luke 08-19-26 Instructions](https://eveglyphdesign.github.io/hawkins-twin-platform/customer-sphere/Luke-08-19-26-Instructions/) · [Customer Sphere Wireframe for Tim](https://eveglyphdesign.github.io/hawkins-twin-platform/customer-sphere/tim/)

---

## 1. The idea in one line

**When a truck comes in, the twin already knows what warranty it holds — OEM and aftermarket — and the service advisor gets a "warranty bot" to hit before the customer is in the door. The bot answers *what can we check right now that will be an easy win for a warranty claim*.**

## 2. The recap, in the order it came out

### Luke — the setup

> Essentially we take the warranty information that's assigned to each unit. Because we can pull that when we run an exam, so we feed that in. So anytime that truck comes in, it's automatically picked up, scanned — what warranty is still covered — and it can allow the service advisor to easily hit a button and talk to it to see: *what can we check at this moment? Is it going to be an easy win for a warranty claim?*
>
> It can be simple stuff. It can be, on the torque side, within 500 kilometres we check brakes. Within the Peterbilt side, you know, where's your first inspection? Is it a crucial point to get that done?
>
> It would be a simple warranty upload that would be able to track what's applicable to each unit based on year, extended package — and it could even then also be folded into when warranties are nearing the end.

### Dany — where does the warranty live today?

> How do you collect the warranty information? Like, where do you validate the warranty today?

### Luke — the source, and the join key

> That would be through either the OEM system, or an aftermarket warranty that they would have. And it's all tracked through the VIN.

### Dany — so we can do it before the customer arrives

> The vehicle identification number. Right. So you'll check the third-party on that before doing the repair.

### Luke — proactive rather than reactive

> When a unit comes in for any type of service, the VIN is collected — and it's usually already picked up. Unless they're a new customer, we already have their VIN. So this could be a proactive thing as well. If somebody books in, we have their VIN. We can already start to run warranty checks on it.
>
> And when they walk in the door, we can say, *hey, we're also going to check this for warranty, this for warranty, this for warranty too. Would you like us to do that?*

### Dany — why not for everyone

> Why would you not do that? We can give you minimal charge. Why not do that for everyone?

### Luke — because it's the bonus, not the base

> Well, we can — absolutely. But this isn't just a technical thing. This is a customer-service bonus too. *Hey, we knew you were coming. You're under warranty. We see there's things that are covered. Would you like us to check this for a warranty-coverage surcharge?*

### Dany — the name that stuck

> So we'll have — why don't we make you, like, a little warranty bot? A little warranty bot. And then you'd provide it to the service advisors.

### Luke — Tim's line

> Warranty bot. And that could be — that's the possibilities of the entire business.
>
> [Tim: **I like that. I like that. I like that.**]

### Dany — the plumbing question

> These OEM sites will probably want some samples of a few of those, because probably we can connect to some of them with our APIs.

### Luke — where the easy wins live

> Aftermarket warranty, especially on the powersport side, would be really vulnerable to this — the OEM side third-parties it out, so that could be a window as well.
>
> I'm not 100% sure on the Peterbilt side how warranty flows and works yet. I know it's much more complicated because of the dollar volume. But it's the easy wins that we'd want to look for that can turn a three-hour RO into a six-hour RO — because of extra warranty work we can complete while we're draining an oil tank.

### Dany — the targeting system

> So that will be the targeting system for this. We can upload warranty coverages and start to specify them, maybe even through a code, when they're entered into CDK or Lightspeed.

### Luke — LLM caveat

> Warranty's pretty good, because the terms and conditions can be loaded as context. Even if they're all right in the same session, we can get pretty close on it. It's just that with a commercial LLM like that, it's always going to be reasoning over and over again — it's never going to be exactly the same.

### Dany — drift, and how to bound it

> But it can be a trigger to look, because quite often it's something that can pop up and make you jump out. It's always going to have a little bit of drift. But you can manage the drift over time — like I showed you with the boot contract and the canon and the SIN registry. As long as you have some kind of boundary. That's just an example of how to set up a boundary. You couldn't do it with less than three points in order to set up a boundary — that's the minimum. But it can be done in other ways.

### Luke — the close

> You know what, that makes sense. It can be done a number of different ways. And really, this could be a further-down-the-road long-term thing. **But like — that's big-money-off-the-table stuff. That's what we go with — the information that's the easiest to consolidate.**

---

## 3. What this actually is, once the recap is set aside

**The Warranty Bot is a per-unit warranty context object, keyed on VIN, exposed to the service advisor as a natural-language button, evaluated at booking time not at repair time.**

Six moving parts:

1. **The unit register.** Every VIN the dealership has ever touched, with year, model, factory package, extended-warranty package, in-service date, and every OEM / aftermarket warranty rider tied to it. This is a `twin.doc(kind='warranty_coverage')` extension of the sphere.

2. **The coverage rules.** OEM warranty terms (Peterbilt / PACCAR base + extended), aftermarket warranty terms (Torque, powersport-style third-party programs), and dealership-added service contracts. Loaded as context. Structured where possible (year + component + km/mile threshold + coverage window + labor rate), narrative where it has to be.

3. **The check catalogue.** *What can we check at this moment that will be an easy win?* Curated list of high-yield inspections, indexed by coverage rule and by the ROs the truck is already in for. Brakes at 500 km on Torque. First-inspection point on Peterbilt. Oil-drain windows where the tech is under the truck anyway.

4. **The advisor UI.** One button on the service-advisor screen — *"Warranty check this VIN"* — plus a talk-to-it mode where the advisor asks in plain language and the bot answers what is in coverage and what is worth checking, right now, on this unit. **Proactive, not reactive**: fires when the booking is made, not when the truck rolls in.

5. **The customer-facing script.** The bot output becomes an offer, not an invoice line: *"We saw you were coming in. Your unit is still under warranty for A, B and C. Would you like us to include those in today's visit?"* — the customer-service bonus Luke insisted on.

6. **The boundary.** Because a commercial LLM will drift, the bot output is a trigger-to-look, not an authoritative claim. The advisor still confirms. The dealership still submits. Drift is managed the same way it is managed in the boot contract and the SIN registry — with an explicit three-point boundary (source rule · unit context · check catalogue). Anything the bot suggests outside those three points is out of bounds.

---

## 4. Where it plugs into the sphere and the extraction plan

- **VIN is the join key.** VIN already lives on `twin.customer` and on every service RO in CDK. The new `kind='warranty_coverage'` document joins on VIN, not on customer id, so a warranty rider that transfers with a truck to a second owner still resolves.
- **Booking is the trigger event.** When a booking lands in CDK, the twin fires the warranty check. If the OEM side is API-reachable (per Luke's "we can connect to some of them with our APIs"), the check is live. If the OEM side is a third-party (Peterbilt / PACCAR going through their own third party, aftermarket programs via their own portals), the check is a scheduled fetch off a stored credential — the same shape as the existing CDK export-route pattern.
- **Adds to the extraction plan.** This is a new stage in the eight-stage extraction order that lives in [`EXTRACTION-STAGING.md`](https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin/blob/main/dashboard/EXTRACTION-STAGING.md). Concretely:
  - Stage 3b — Warranty coverage per unit (OEM base, OEM extended, aftermarket, dealership-added service contract).
  - Stage 3c — Warranty terms as context (structured where the rule is a threshold, narrative where the terms are prose).
  - Stage 3d — Check catalogue (high-yield inspections indexed by rule × current-RO).
  - Stage 3e — Booking-time trigger (event handler on CDK booking-created; scoring output persisted so it survives the LLM being reasoned again).

## 5. The Peterbilt caveat, quoted honestly

Luke: *I'm not 100% sure on the Peterbilt side how warranty flows and works yet. I know it's much more complicated because of the dollar volume.* The Peterbilt claim path is complicated, and the twin does not pretend to hold it end-to-end today. **What the twin can do first, safely:**

- The dealership-side lens (which coverages the unit holds, which checks are worth doing at this visit) is fully inside the twin's remit.
- Submitting the claim to Peterbilt / PACCAR stays where it is today — in the manufacturer's system — until the walkthrough with Craig Allen and the operator lands (that ask is already open in [`EXTERNAL-REFERENCES.md`](https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin/blob/main/dashboard/EXTERNAL-REFERENCES.md)).
- Aftermarket / powersport is where the twin can be end-to-end first, because as Luke put it, that side "would be really vulnerable to this."

## 6. Why this is on Tim's list, in Luke's own words

> Like — that's big-money-off-the-table stuff. That's what we go with — the information that's the easiest to consolidate.

The RO that was a three-hour job becomes a six-hour job because the warranty coverage was checked before the tech opened the drain plug. **The revenue that this surfaces is revenue the dealership was already entitled to but was not going to bill.** That is precisely the profile of every other signal in the Instructions doc — leakage, not new work.

---

## 7. Amendment to §3 of the Instructions

The stub that reads *"Where can we capture more warranty work on units when they are in the shop? We could possibly upload warranty plans into the model for this"* is superseded by this document. §3 of the Instructions now links here rather than trying to hold the idea in a single blockquote.

---

*Recorded 2026-08-19 by Dany Thériault from a live conversation with Luke Weatherbie, off-the-record. Preserved because the meeting was not on record and the idea is load-bearing for the dashboard.*

*Pour le bien-être du peuple.*
