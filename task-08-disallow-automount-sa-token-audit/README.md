# Task 08 — Disallow automountServiceAccountToken (Audit Mode)

## What this policy does

Checks that every Pod explicitly sets `spec.automountServiceAccountToken: false`. Runs in `Audit` mode.

## Why it matters

By default, every pod automatically gets its ServiceAccount's API token mounted at `/var/run/secrets/kubernetes.io/serviceaccount/token` — **even if the application never talks to the Kubernetes API.** This is one of the most common "silent" over-privilege issues in real clusters:

- If that pod is compromised, the attacker now has a live credential to the Kubernetes API server, scoped to whatever RBAC permissions that ServiceAccount has.
- Most application pods (web servers, databases, workers) never need to call the K8s API at all — the token is pure unnecessary attack surface.

Only pods that genuinely need API access (controllers, operators, CI/CD runners) should have this token mounted, and even then they should use a purpose-built ServiceAccount with least-privilege RBAC — not the default one.

## Rule type

`validate`, mode: `Audit`.

## Files

- `policy.yaml` — the ClusterPolicy
- `bad-pod.yaml` — no `automountServiceAccountToken` set (defaults to true; flagged as `fail`)
- `good-pod.yaml` — `automountServiceAccountToken: false` (flagged as `pass`)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove Audit mode behavior
