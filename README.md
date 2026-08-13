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
5. [`gitops-final-test/README.md`](gitops-final-test/README.md) — the final test: one pod that satisfies all 17 policies at once, one that violates them, run against the full policy stack together

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

| # | Task | Rule Type | Mode |
|---|------|-----------|------|
| 01 | [Require resource requests/limits](task-01-require-resource-limits/README.md) | validate | Enforce |
| 02 | [Disallow `:latest` image tag](task-02-disallow-latest-tag/README.md) | validate | Enforce |
| 03 | [Require `runAsNonRoot`](task-03-require-run-as-non-root/README.md) | validate | Enforce |
| 04 | [Disallow privileged containers](task-04-disallow-privileged-containers/README.md) | validate | Enforce |
| 05 | [Require standard labels](task-05-require-labels-audit/README.md) | validate | Audit |
| 06 | [Disallow hostPath volumes](task-06-disallow-hostpath-audit/README.md) | validate | Audit |
| 07 | [Require readOnlyRootFilesystem](task-07-require-readonly-rootfs-audit/README.md) | validate | Audit |
| 08 | [Disallow automountServiceAccountToken](task-08-disallow-automount-sa-token-audit/README.md) | validate | Audit |
| 09 | [Auto-inject default labels](task-09-mutate-add-labels/README.md) | mutate | — |
| 10 | [Auto-inject default resource limits](task-10-mutate-default-resources/README.md) | mutate | — |
| 11 | [Auto-set imagePullPolicy](task-11-mutate-image-pull-policy/README.md) | mutate | — |
| 12 | [Auto-generate default-deny NetworkPolicy](task-12-generate-networkpolicy/README.md) | generate | — |
| 13 | [Auto-generate default ResourceQuota](task-13-generate-resourcequota/README.md) | generate | — |
| 14 | [Auto-generate default ConfigMap](task-14-generate-configmap/README.md) | generate | — |
| 15 | [Verify image signatures (cosign)](task-15-verify-images-enforce/README.md) | verifyImages | Enforce |
| 16 | [Verify image signatures (cosign)](task-16-verify-images-audit/README.md) | verifyImages | Audit |
| 17 | [hostPath exception by label](task-17-hostpath-exception-by-label/README.md) | validate | Enforce |

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
