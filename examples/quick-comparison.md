# A quick comparison

This is an author-written illustration, not a model benchmark. It shows the behavior DissentKit is designed to add.

## Request

> Dissent this: I want to launch the migration Friday without a rollback rehearsal.

## Generic reply

Launching without a rollback rehearsal could be risky. Consider testing the rollback plan first and make sure the team is prepared in case something goes wrong.

## DissentKit Direct Review

**Verdict:** Do not launch Friday without a rollback rehearsal. The largest risk is discovering during an outage that the documented recovery path does not work under real conditions.

**Strongest version of your plan:** Shipping Friday may protect the schedule, and the migration itself may already have passed its functional tests.

**Counterargument:** `[certain]` Functional migration tests do not prove that rollback works. `[likely]` A failed rollback would extend the outage and force the team to diagnose two problems at once.

**Missing tradeoff:** Delaying the launch costs time. Launching without a rehearsed recovery path risks a longer interruption, damaged data, and a decision made under pressure.

**Corrected plan:** Run a time-boxed rollback rehearsal before the go or no-go decision. Record the trigger, owner, commands, expected recovery time, and data-integrity check. If the rehearsal fails or exceeds the recovery window, move the migration.

## What changed

The second answer makes a decision, names the failure mechanism, distinguishes certainty from inference, acknowledges the schedule cost, and replaces vague caution with a testable plan. That is the Direct Review contract. It does not prove that every model will follow the contract, which is why the repository also includes reproducible evaluation fixtures.
