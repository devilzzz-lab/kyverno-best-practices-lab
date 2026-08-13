# Task 10 — Auto-inject Default Resource Limits (Mutate)

## What this policy does

Any container missing `resources.requests`/`resources.limits` gets sensible defaults injected automatically (`100m`/`128Mi` requests, `250m`/`256Mi` limits). Uses `+()` conditional anchors throughout, so it never overwrites values a developer already set — it only fills in what's missing.

## Why it matters

Compare this to **Task 01**, which *rejects* pods missing resource limits. This policy takes the opposite, complementary approach: instead of blocking the developer, it silently fixes the gap for them. Many teams actually run both together — mutate first to backfill sane defaults, then validate/enforce as a safety net for anything that still slips through (e.g. from a raw `kubectl run`).

This is a very common "pit of success" pattern: make the easy path also the compliant path.

## Rule type

`mutate` — patches missing fields only, using nested conditional anchors on `requests`/`limits`/`cpu`/`memory` individually.

## Files

- `policy.yaml` — the ClusterPolicy
- `no-resources-pod.yaml` — pod with zero resources set; Kyverno should inject full defaults
- `partial-resources-pod.yaml` — pod with only `cpu` request set; Kyverno should fill in the rest without touching the existing `cpu` value
- `setup.md` — how to apply the policy
- `demo.md` — how to prove the mutation happened correctly in both cases
