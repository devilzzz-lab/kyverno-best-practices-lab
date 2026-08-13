# Task 13 — Auto-generate Default ResourceQuota (Generate)

## What this policy does

Whenever a new Namespace is created, Kyverno automatically generates a `ResourceQuota` capping that namespace's total CPU/memory requests and limits, and its max pod count. System namespaces and `default` are excluded.

## Why it matters

Without a `ResourceQuota`, a single namespace can consume unlimited cluster resources — even if every individual Pod has proper `requests`/`limits` (Task 01), there's nothing capping how *many* pods a namespace can run. One team's namespace going rogue (bad autoscaling config, runaway CronJob, etc.) can starve every other team sharing the cluster.

Auto-generating a sane default quota on namespace creation means every team gets multi-tenancy protection automatically — no one has to remember to write one, and no namespace exists unconstrained.

## Rule type

`generate` — creates a `ResourceQuota` whenever a `Namespace` is created. `synchronize: true` keeps it self-healing if deleted manually.

## Files

- `policy.yaml` — the ClusterPolicy
- `setup.md` — how to apply the policy
- `demo.md` — how to prove the ResourceQuota gets auto-created and enforced
