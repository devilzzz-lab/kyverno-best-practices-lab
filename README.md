# Kyverno Best Practices Lab

Hands-on lab covering **10 real-world Kyverno policies**, built and tested on a local KIND cluster, with an optional GitOps (ArgoCD) auto-deployment flow.

## Why Kyverno

Kyverno is a Kubernetes-native policy engine. Unlike OPA/Gatekeeper (which requires learning Rego), Kyverno policies are plain YAML — the same format you already use for any Kubernetes manifest. It runs as a dynamic admission controller, intercepting requests to the API server to **validate**, **mutate**, or **generate** resources, and can also verify image signatures.

See [`docs/kyverno-architecture.md`](docs/kyverno-architecture.md) for the full architecture breakdown.

---

## Two ways to use this repo

### Path A — I want ALL policies live on my cluster (GitOps)

Use this if you just want every policy in `policies/` enforced on your cluster automatically, kept in sync with Git.

1. [`setup/01-cluster-setup.md`](setup/01-cluster-setup.md) — create the KIND cluster
2. [`setup/02-kyverno-install.md`](setup/02-kyverno-install.md) — install Kyverno
3. [`setup/03-argocd-install.md`](setup/03-argocd-install.md) — install ArgoCD and connect this repo
4. [`setup/04-argocd-testing.md`](setup/04-argocd-testing.md) — verify the Git → cluster sync actually works (valid push, deleted push, broken push)

From then on: edit/add a file in `policies/`, `git push`, and ArgoCD applies it — no manual `kubectl apply`. See [`policies/README.md`](policies/README.md) for how that folder works.

### Path B — I want to learn how EACH policy works (manual)

Use this to study one policy at a time — apply it yourself, break it yourself, see exactly what Kyverno does.

1. [`setup/01-cluster-setup.md`](setup/01-cluster-setup.md) — create the KIND cluster
2. [`setup/02-kyverno-install.md`](setup/02-kyverno-install.md) — install Kyverno
3. Skip ArgoCD entirely. Open any `task-NN-*/` folder from the [Task index](#task-index) below and work through its 3 files in order:
   - `README.md` — what the policy does and why it matters
   - `setup.md` — apply that one policy manually with `kubectl apply -f`
   - `demo.md` — apply `bad-pod.yaml` (should be rejected) and `good-pod.yaml` (should succeed) to prove it

Both paths can be used together — e.g. run Path A for a live cluster, and still read through `task-NN-*/README.md` files to actually understand each rule.

---

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

---

## Repo structure

```
kyverno-best-practices-lab/
├── docs/
│   └── kyverno-architecture.md      # How Kyverno works internally
├── setup/
│   ├── 01-cluster-setup.md          # Create the local KIND cluster
│   ├── 02-kyverno-install.md        # Install Kyverno via Helm
│   ├── 03-argocd-install.md         # Install ArgoCD + connect this repo
│   └── 04-argocd-testing.md         # Verify GitOps sync works
├── argocd/
│   └── kyverno-policies-app.yaml    # ArgoCD Application (watches policies/)
├── policies/                        # Single source of truth ArgoCD auto-syncs (Path A)
│   ├── README.md
│   ├── 01-require-resource-limits.yaml
│   ├── 02-disallow-latest-tag.yaml
│   └── ...
├── task-01-require-resource-limits/ # Manual learning folders (Path B)
│   ├── README.md
│   ├── setup.md
│   ├── demo.md
│   ├── policy.yaml
│   ├── bad-pod.yaml
│   └── good-pod.yaml
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
