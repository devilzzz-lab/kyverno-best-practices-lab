# Task 17 — hostPath Exception by Label (One Workload Allowed, Rest Blocked)

## The real-world scenario

You have several Deployments in your cluster. One of them is a legitimate infrastructure workload that genuinely needs to read `/etc` (or any other node path) via a `hostPath` volume — e.g. a log-collector agent, a node-monitoring exporter. Every other Deployment is a normal application and should **never** be allowed to mount `hostPath` at all.

## Important clarification first — what this policy CANNOT do

If you have **1 Deployment with `replicas: 7`**, all 7 pods are generated from the exact same PodTemplate. There is no way to have "1 of the 7 replicas" behave differently from the other 6 — they are identical clones by definition. Kyverno validates each pod's manifest, and since all 7 replicas submit the same manifest, they either all pass or all fail together.

**What this policy actually demonstrates:** 7 *separate* Deployments. One of them (the legitimate infra workload) is labeled `hostpath-access: allowed` and is permitted to mount hostPath. The other 6 are not labeled, and are blocked from using hostPath at all.

## What this policy does

Blocks any Pod from using a `hostPath` volume — **except** pods carrying the label `hostpath-access: allowed`. Uses Kyverno's `match` + `exclude` combination: `match` selects all Pods for validation, `exclude` carves out an exception for the labeled ones.

## Why it matters

This is the standard real-world pattern for "mostly forbidden, narrowly permitted." Blanket-blocking hostPath (Task 06) is a good start, but real clusters almost always have 1-2 legitimate system/infra workloads that genuinely need it. Rather than disabling the policy cluster-wide, you carve out a precise, auditable exception — anyone can `kubectl get pods -l hostpath-access=allowed` and see exactly which workloads have this elevated access, and why.

## Rule type

`validate`, mode: `Enforce`, using `match` + `exclude` with a label selector.

## Files

- `policy.yaml` — the ClusterPolicy
- `allowed-pod.yaml` — labeled `hostpath-access: allowed`, mounts hostPath (should SUCCEED)
- `blocked-pod.yaml` — no label, mounts hostPath (should be REJECTED)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove the exception works correctly
