# Task 11 — Auto-set imagePullPolicy (Mutate)

## What this policy does

Automatically sets `imagePullPolicy` based on the image tag:
- Image uses `:latest` → forced to `imagePullPolicy: Always` (since `:latest` can change, you must always re-pull to get the current version)
- Image uses a specific version tag (e.g. `nginx:1.25`) → set to `IfNotPresent` if not already specified (versioned tags are immutable, so there's no need to re-pull every time — saves time and registry bandwidth)

## Why it matters

This is a subtle but common production bug: if you use `:latest` with the default/incorrect pull policy, Kubernetes may reuse a stale cached image on the node instead of pulling the actual latest version — completely defeating the purpose of `:latest` and causing "why is it running the old code" confusion. This policy makes the pull behavior automatically match the tag's semantics, without relying on every developer remembering to set it correctly by hand.

(Note: Task 02 in this repo blocks `:latest` outright in Enforce mode — this task assumes a cluster where `:latest` is still permitted, e.g. a dev/sandbox namespace, and just makes its behavior correct when it does show up.)

## Rule type

`mutate`, with a `preconditions` block on the first rule (only apply "Always" logic when a `:latest` image is actually present) and a conditional anchor `+()` on the second rule (don't overwrite an explicitly set pull policy).

## Files

- `policy.yaml` — the ClusterPolicy
- `latest-tag-pod.yaml` — uses `nginx:latest`; should get `imagePullPolicy: Always`
- `versioned-tag-pod.yaml` — uses `nginx:1.25` with no pull policy set; should get `IfNotPresent`
- `setup.md` — how to apply the policy
- `demo.md` — how to prove both mutation paths work
