# Task 03 — Require `runAsNonRoot`

## What this policy does

Blocks any Pod unless it explicitly sets `securityContext.runAsNonRoot: true` — either at the pod level or on every container. Accepts either location via `anyPattern`.

## Why it matters

By default, containers run as `root` (UID 0) unless the image or manifest says otherwise. Running as root inside a container is dangerous because:
- A container breakout (kernel/runtime vulnerability) gives the attacker **root on the host**, not just a low-privilege user.
- Many container security benchmarks (CIS Kubernetes Benchmark, NSA/CISA hardening guide) list this as a top recommendation.
- It's cheap to enforce and forces teams to build images that don't assume root.

This is a foundational **Pod Security Standard** control (maps to the "Restricted" profile).

## Rule type

`validate`, mode: `Enforce`, using `anyPattern` (matches if either sub-pattern is satisfied).

## Files

- `policy.yaml` — the ClusterPolicy
- `bad-pod.yaml` — no `runAsNonRoot` set (should be rejected)
- `good-pod.yaml` — sets `runAsNonRoot: true` (should succeed)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove it works
