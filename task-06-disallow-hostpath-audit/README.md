# Task 06 — Disallow hostPath Volumes (Audit Mode)

## What this policy does

Flags any Pod that mounts a `hostPath` volume. Runs in `Audit` mode — the pod is still created, but logged as a violation.

## Why it matters

A `hostPath` volume mounts a path from the **node's own filesystem** into the pod. This means:
- A compromised container can read/write files on the underlying node — potentially including secrets, other workloads' data, or the container runtime socket.
- It ties a pod to a specific node's local disk contents, breaking portability and rescheduling.
- It's a common technique used in real container-escape attack chains (e.g. mounting `/` or the Docker socket).

CIS Kubernetes Benchmark flags unrestricted `hostPath` usage as a security risk. It's not always avoidable (some legitimate infra daemonsets need it), which is exactly why this is a good `Audit`-first candidate — you want visibility into who's using it before you block it outright.

## Rule type

`validate`, mode: `Audit`.

## Files

- `policy.yaml` — the ClusterPolicy
- `bad-pod.yaml` — mounts a hostPath volume (created, but flagged as `fail`)
- `good-pod.yaml` — no volumes (flagged as `pass`)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove Audit mode behavior
