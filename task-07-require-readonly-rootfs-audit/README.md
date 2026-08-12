# Task 07 — Require readOnlyRootFilesystem (Audit Mode)

## What this policy does

Checks that every container sets `securityContext.readOnlyRootFilesystem: true`. Runs in `Audit` mode.

## Why it matters

By default, a container's root filesystem is writable. If an attacker gets code execution inside the container, a writable filesystem lets them drop tools, modify binaries, or persist malware inside the running container. Setting the root filesystem to read-only removes that entire class of tampering — the app can still write to explicitly mounted volumes (e.g. `/tmp` via an `emptyDir`), but can't modify anything else.

This is a widely recommended hardening step (CIS Benchmark, Pod Security Standards "Restricted" profile) but it **does** require some application awareness — apps that write logs or temp files to arbitrary paths will break unless you mount an `emptyDir` for those paths. That's exactly why this is a good `Audit` candidate: you want to see which workloads would break before flipping to `Enforce`.

## Rule type

`validate`, mode: `Audit`.

## Files

- `policy.yaml` — the ClusterPolicy
- `bad-pod.yaml` — writable root filesystem (default; flagged as `fail`)
- `good-pod.yaml` — `readOnlyRootFilesystem: true` set (flagged as `pass`)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove Audit mode behavior
