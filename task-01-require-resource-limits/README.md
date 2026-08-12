# Task 01 — Require Resource Requests & Limits

## What this policy does

Blocks any Pod from being created if its containers don't specify **both** `resources.requests` and `resources.limits` for `cpu` and `memory`.

## Why it matters

Without resource requests/limits:
- The Kubernetes scheduler can't make good placement decisions (no idea how much CPU/memory a pod needs).
- A single misbehaving pod can consume all node resources and starve everything else (noisy neighbor problem).
- Autoscaling (HPA/VPA/Cluster Autoscaler) doesn't work reliably without requests defined.

This is usually the **first** policy any team adopts — it's low-risk, catches a very common oversight, and directly improves cluster stability.

## Rule type

`validate`, mode: `Enforce` (blocks non-compliant pods outright — no grace period).

## Files

- `policy.yaml` — the ClusterPolicy
- `setup.md` — how to apply it
- `demo.md` — how to prove it blocks bad pods and allows good ones
