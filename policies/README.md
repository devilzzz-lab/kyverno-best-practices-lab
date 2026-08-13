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

## All policies

| File | ClusterPolicy name | Rule Type | Mode | Task |
|---|---|---|---|---|
| `01-require-resource-limits.yaml` | `require-resource-limits` | validate | Enforce | [Task 01](../task-01-require-resource-limits/README.md) |
| `02-disallow-latest-tag.yaml` | `disallow-latest-tag` | validate | Enforce | [Task 02](../task-02-disallow-latest-tag/README.md) |
| `03-require-run-as-non-root.yaml` | `require-run-as-non-root` | validate | Enforce | [Task 03](../task-03-require-run-as-non-root/README.md) |
| `04-disallow-privileged-containers.yaml` | `disallow-privileged-containers` | validate | Enforce | [Task 04](../task-04-disallow-privileged-containers/README.md) |
| `05-require-labels-audit.yaml` | `require-labels-audit` | validate | Audit | [Task 05](../task-05-require-labels-audit/README.md) |
| `06-disallow-hostpath-audit.yaml` | `disallow-hostpath-audit` | validate | Audit | [Task 06](../task-06-disallow-hostpath-audit/README.md) |
| `07-require-readonly-rootfs-audit.yaml` | `require-readonly-rootfs-audit` | validate | Audit | [Task 07](../task-07-require-readonly-rootfs-audit/README.md) |
| `08-disallow-automount-sa-token-audit.yaml` | `disallow-automount-sa-token-audit` | validate | Audit | [Task 08](../task-08-disallow-automount-sa-token-audit/README.md) |
| `09-mutate-add-labels.yaml` | `mutate-add-default-labels` | mutate | — | [Task 09](../task-09-mutate-add-labels/README.md) |
| `10-mutate-default-resources.yaml` | `mutate-default-resources` | mutate | — | [Task 10](../task-10-mutate-default-resources/README.md) |
| `11-mutate-image-pull-policy.yaml` | `mutate-image-pull-policy` | mutate | — | [Task 11](../task-11-mutate-image-pull-policy/README.md) |
| `12-generate-networkpolicy.yaml` | `generate-default-deny-netpol` | generate | — | [Task 12](../task-12-generate-networkpolicy/README.md) |
| `13-generate-resourcequota.yaml` | `generate-default-resourcequota` | generate | — | [Task 13](../task-13-generate-resourcequota/README.md) |
| `14-generate-configmap.yaml` | `generate-default-configmap` | generate | — | [Task 14](../task-14-generate-configmap/README.md) |
| `15-verify-images-enforce.yaml` | `verify-image-signatures-enforce` | verifyImages | Enforce | [Task 15](../task-15-verify-images-enforce/README.md) |
| `16-verify-images-audit.yaml` | `verify-image-signatures-audit` | verifyImages | Audit | [Task 16](../task-16-verify-images-audit/README.md) |
| `17-hostpath-exception-by-label.yaml` | `hostpath-exception-by-label` | validate | Enforce | [Task 17](../task-17-hostpath-exception-by-label/README.md) |

## Note on running all 17 together

Some policies overlap in scope (e.g. Task 06's blanket hostPath Audit and Task 17's Enforce-with-exception both target hostPath). If you sync all 17 via ArgoCD at once, every Pod is evaluated against all of them simultaneously — see `setup/change.md` for how to pause ArgoCD and isolate individual policies for clean testing.
