# Task 12 — Auto-generate Default-Deny NetworkPolicy (Generate)

## What this policy does

Whenever a new Namespace is created, Kyverno automatically creates a `NetworkPolicy` inside it that denies all Ingress and Egress traffic by default. System namespaces (`kube-system`, `kyverno`, `argocd`, etc.) and `default` are excluded so the cluster itself doesn't break.

## Why it matters

By default, Kubernetes networking is **fully open** — any pod can talk to any other pod across the entire cluster, in any namespace, with zero restrictions. This is a huge blast radius if any single pod is compromised. The "default-deny, then explicitly allow what's needed" model is a foundational zero-trust networking practice.

Rather than relying on every team to remember to write a NetworkPolicy when they create a namespace, this policy makes secure-by-default automatic — new namespaces start locked down, and teams must explicitly add `NetworkPolicy` rules to allow the traffic their app actually needs.

`synchronize: true` means if someone deletes the generated NetworkPolicy manually, Kyverno's background controller will recreate it to match the policy's intent.

## Rule type

`generate` — creates a new resource (`NetworkPolicy`) whenever the trigger resource (`Namespace`) is created. No enforce/audit split.

## Files

- `policy.yaml` — the ClusterPolicy
- `setup.md` — how to apply the policy
- `demo.md` — how to prove the NetworkPolicy gets auto-created
