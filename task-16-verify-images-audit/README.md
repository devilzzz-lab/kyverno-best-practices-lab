# Task 16 — Verify Image Signatures with Cosign (Audit)

## What this policy does

Same signature check as Task 15, but in `Audit` mode — unsigned images are **not blocked**, just logged as a violation in `PolicyReport`.

## Why it matters

Image signature verification is one of the riskiest checks to turn on in `Enforce` mode blind — if your team hasn't fully adopted image signing yet, flipping this straight to `Enforce` could block every single deployment cluster-wide. This is the textbook case for staging a policy: run in `Audit` for a while, see exactly how many workloads currently run unsigned images, get teams to adopt signing, and only then flip to `Enforce` (Task 15).

## Rule type

`verifyImages`, mode: `Audit`.

## Files

- `policy.yaml` — the ClusterPolicy
- `signed-pod.yaml` — signed test image (passes)
- `unsigned-pod.yaml` — unsigned test image (created anyway, but flagged `fail`)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove Audit mode behavior for image verification
