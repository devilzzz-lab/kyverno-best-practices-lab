# Task 09 — Auto-inject Default Labels (Mutate)

## What this policy does

Every Pod that doesn't already have `team` and `managed-by` labels gets them **automatically added** at admission time — before the pod is ever persisted. The `+()` conditional anchor means "add this field only if it doesn't already exist," so it won't clobber a label someone explicitly set.

## Why it matters

There's no `Enforce`/`Audit` split for `mutate` — the rule either applies its patch on match, or it doesn't. Mutation is proactive automation, not gatekeeping: instead of rejecting a pod for missing a label, Kyverno just fixes it for you. Teams commonly use this to guarantee every workload is traceable (cost allocation, ownership, alert routing) without pushing that burden onto every developer.

## Rule type

`mutate` — no enforce/audit modes. `+(team)` and `+(managed-by)` are conditional anchors meaning "only add if absent."

## Files

- `policy.yaml` — the ClusterPolicy
- `test-pod.yaml` — a plain pod with no labels; apply it and inspect the result to see the injected labels
- `setup.md` — how to apply the policy
- `demo.md` — how to prove the mutation happened
