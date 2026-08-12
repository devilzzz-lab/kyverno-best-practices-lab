# Task 04 — Disallow Privileged Containers

## What this policy does

Blocks any Pod where a container sets `securityContext.privileged: true`. The pattern uses `=()` conditional anchors, so pods that don't set `privileged` at all (defaults to `false`) are still allowed — only explicit `true` is blocked.

## Why it matters

A privileged container has almost unrestricted access to the host — it can access all host devices, bypass most kernel security mechanisms (cgroups, namespaces, seccomp/AppArmor restrictions), and effectively gives root-equivalent control of the node itself.

This is one of the most dangerous settings in Kubernetes:
- It's the #1 escape hatch used in real container-breakout attacks.
- CIS Kubernetes Benchmark and Pod Security Standards ("Restricted" and "Baseline" profiles) both explicitly forbid it.
- There's almost never a legitimate reason for an application workload to need it (some infra/CNI/storage daemonsets are the rare exception, and those should be explicitly excluded from this policy via namespace/label exclusions in production).

## Rule type

`validate`, mode: `Enforce`, using conditional anchors (`=()`) so unset fields don't fail the pattern.

## Files

- `policy.yaml` — the ClusterPolicy
- `bad-pod.yaml` — sets `privileged: true` (should be rejected)
- `good-pod.yaml` — no `privileged` set (should succeed)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove it works
