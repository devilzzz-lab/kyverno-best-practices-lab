# Kyverno Best Practices Lab

Hands-on lab covering **10 real-world Kyverno policies**, built and tested on a local KIND cluster. Each task is self-contained: what the policy does, why it matters, how to set it up, and how to prove it works.

## Why Kyverno

Kyverno is a Kubernetes-native policy engine. Unlike OPA/Gatekeeper (which requires learning Rego), Kyverno policies are plain YAML — the same format you already use for any Kubernetes manifest. It runs as a dynamic admission controller, intercepting requests to the API server to **validate**, **mutate**, or **generate** resources, and can also verify image signatures.

See [`docs/kyverno-architecture.md`](docs/kyverno-architecture.md) for the full architecture breakdown.

## Repo structure

```
kyverno-best-practices-lab/
├── docs/
│   └── kyverno-architecture.md      # How Kyverno works internally
├── setup/
│   ├── 01-cluster-setup.md          # Create the local KIND cluster
│   ├── 02-kyverno-install.md        # Install Kyverno via Helm
│   └── 03-argocd-install.md         # Install ArgoCD + connect this repo
├── argocd/
│   └── kyverno-policies-app.yaml    # ArgoCD Application (watches policies/)
├── policies/                        # Single source of truth ArgoCD auto-syncs
│   ├── 01-require-resource-limits.yaml
│   ├── 02-disallow-latest-tag.yaml
│   └── ...
├── task-01-require-resource-limits/
├── task-02-disallow-latest-tag/
├── task-03-require-run-as-non-root/
├── task-04-disallow-privileged-containers/
├── task-05-require-labels/
├── task-06-auto-add-labels-mutate/
├── task-07-restrict-image-registries/
├── task-08-generate-default-networkpolicy/
├── task-09-require-probes/
└── task-10-image-signature-verification/
```

## GitOps flow (ArgoCD)

Every policy in `policies/` is auto-applied to the cluster by ArgoCD whenever you `git push`:

```
edit policy in policies/  →  git push  →  ArgoCD detects change  →  auto-applies to cluster
```

See [`policies/README.md`](policies/README.md) for how the folder is organized, and [`setup/03-argocd-install.md`](setup/03-argocd-install.md) to set it up.

Each `task-NN-*` folder contains:
- `README.md` — what the policy does and why it matters
- `setup.md` — commands to apply the policy
- `demo.md` — commands to prove it works (pass/fail cases)
- `policy.yaml` — the actual Kyverno policy

## Getting started

1. Follow [`setup/01-cluster-setup.md`](setup/01-cluster-setup.md) to create the KIND cluster.
2. Follow [`setup/02-kyverno-install.md`](setup/02-kyverno-install.md) to install Kyverno.
3. Follow [`setup/03-argocd-install.md`](setup/03-argocd-install.md) to install ArgoCD and connect this repo — from this point on, anything you push into `policies/` is auto-applied.
4. Work through `task-01` → `task-10` in order — they go from simple validation rules up to advanced image signature verification. Each task's `demo.md` walks you through manual testing; once you're happy with a policy, copy it into `policies/` so ArgoCD picks it up.

## Task index

| # | Task | Rule Type | Category |
|---|------|-----------|----------|
| 01 | [Require resource requests/limits](task-01-require-resource-limits/README.md) | validate | Reliability |
| 02 | [Disallow `:latest` image tag](task-02-disallow-latest-tag/README.md) | validate | Supply chain hygiene |
| 03 | [Require `runAsNonRoot`](task-03-require-run-as-non-root/README.md) | validate | Pod security |
| 04 | [Disallow privileged containers](task-04-disallow-privileged-containers/README.md) | validate | Pod security |
| 05 | [Require standard labels](task-05-require-labels/README.md) | validate | Governance |
| 06 | [Auto-inject default labels](task-06-auto-add-labels-mutate/README.md) | mutate | Automation |
| 07 | [Restrict allowed image registries](task-07-restrict-image-registries/README.md) | validate | Supply chain security |
| 08 | [Auto-generate default-deny NetworkPolicy](task-08-generate-default-networkpolicy/README.md) | generate | Network security |
| 09 | [Require liveness/readiness probes](task-09-require-probes/README.md) | validate | Reliability |
| 10 | [Verify image signatures (cosign)](task-10-image-signature-verification/README.md) | verifyImages | Supply chain security (advanced) |
