# policies/

This is the **single folder ArgoCD watches**. Every Kyverno `ClusterPolicy` that should be live on the cluster lives here, flat, numbered to match its task.

## How it works (GitOps flow)

```
edit/add a policy.yaml here
        │
        ▼
   git commit + push
        │
        ▼
ArgoCD polls this repo's `policies/` path
        │
        ▼
ArgoCD auto-applies (or removes, if deleted) the ClusterPolicy on the cluster
```

No manual `kubectl apply` needed once ArgoCD is set up (see `setup/03-argocd-install.md`).

## Relationship to `task-NN-*` folders

Each `task-NN-*` folder keeps its own copy of `policy.yaml` alongside its `README.md`, `setup.md`, and `demo.md` — that's for **learning and manual walkthroughs**, where you apply one policy at a time and see how it behaves.

The copy in `policies/` is the **source of truth for the live cluster** via ArgoCD. If you tune a policy after testing it manually in its task folder, copy the final version here too.

## Current policies

| File | ClusterPolicy name | Task |
|---|---|---|
| `01-require-resource-limits.yaml` | `require-resource-limits` | [Task 01](../task-01-require-resource-limits/README.md) |
| `02-disallow-latest-tag.yaml` | `disallow-latest-tag` | [Task 02](../task-02-disallow-latest-tag/README.md) |
| `03-require-run-as-non-root.yaml` | `require-run-as-non-root` | [Task 03](../task-03-require-run-as-non-root/README.md) |
| `04-disallow-privileged-containers.yaml` | `disallow-privileged-containers` | [Task 04](../task-04-disallow-privileged-containers/README.md) |
