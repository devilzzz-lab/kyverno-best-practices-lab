# Task 02 — Disallow `:latest` Image Tag

## What this policy does

Blocks any Pod whose container image uses the `:latest` tag (or has no tag at all — which Docker/Kubernetes silently resolves to `latest`).

## Why it matters

`:latest` is a moving target — the same tag can point to a completely different image tomorrow. This causes:
- **Non-reproducible deployments** — you can't reliably redeploy the exact same version.
- **Silent breakage** — a pod restart can pull a newer, untested image without anyone changing anything.
- **Debugging nightmares** — "it worked yesterday" because `:latest` quietly changed underneath you.

This is one of the most universally recommended Kubernetes best practices, and one of the easiest wins for a policy engine to enforce.

## Rule type

`validate`, mode: `Enforce`.

## Files

- `policy.yaml` — the ClusterPolicy
- `bad-pod.yaml` — uses `nginx:latest` (should be rejected)
- `good-pod.yaml` — uses `nginx:1.25` (should succeed)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove it works
