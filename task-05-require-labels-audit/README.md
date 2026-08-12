# Task 05 — Require Standard Labels (Audit Mode)

## What this policy does

Checks that every Pod has `app` and `env` labels set. Unlike Tasks 01-04, this runs in **`Audit`** mode — non-compliant pods are **NOT blocked**. They're created normally, but Kyverno logs a `fail` result in a `PolicyReport`.

## Why Audit mode matters

`Enforce` mode is risky to turn on blind — if you don't know how many existing workloads would violate a new rule, you could break production the moment you apply it. The standard practice is:

1. Roll out a new policy in `Audit` mode first.
2. Let it run for a while, watch `PolicyReport` results accumulate.
3. See how many resources are actually non-compliant and who owns them.
4. Once violations are fixed (or accepted), flip `validationFailureAction` to `Enforce`.

This is exactly how real platform teams introduce new governance rules without breaking existing workloads overnight.

## Why labeling matters specifically

Labels like `app` and `env` are what most tooling (cost allocation, alerting routing, ownership tracing, `kubectl` filtering) depends on. Missing labels quietly break dashboards and automation elsewhere, even though the pod itself runs fine — which is exactly the kind of "soft" violation that's a good fit for `Audit` mode rather than an outright block.

## Rule type

`validate`, mode: `Audit` — allows non-compliant pods through, but records the violation.

## Files

- `policy.yaml` — the ClusterPolicy
- `bad-pod.yaml` — missing labels (will be CREATED, but shows as `fail` in PolicyReport)
- `good-pod.yaml` — has `app` and `env` labels (shows as `pass`)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove Audit mode behavior
