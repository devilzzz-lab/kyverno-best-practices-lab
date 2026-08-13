# GitOps Final Test — All 17 Policies at Once

This is the final validation step: prove that when **all 17 policies from `policies/` are synced by ArgoCD simultaneously**, a properly-hardened pod sails through cleanly, and a badly-configured pod gets caught.

This is different from every `task-NN-*/demo.md` you've run so far — those test one policy in isolation. This tests the **full policy stack together**, exactly as it behaves on a real production cluster where every rule applies to every pod at once.

## Prerequisites

Make sure ArgoCD auto-sync is ON and all 17 policies are `READY: True`:

```bash
kubectl get clusterpolicy
```

You should see 17 policies, all `READY: True`.

## Test 1 — `good-pod.yaml` (should pass ALL policies)

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-all-policies
```

Expected: pod created successfully. Here's how it satisfies every relevant policy:

| Policy | How `good-pod.yaml` satisfies it |
|---|---|
| `require-resource-limits` | Full `requests`/`limits` set for cpu and memory |
| `disallow-latest-tag` | Uses `nginx:1.25`, not `:latest` |
| `require-run-as-non-root` | `securityContext.runAsNonRoot: true` |
| `disallow-privileged-containers` | `privileged: false` explicitly |
| `require-labels-audit` | Has `app` and `env` labels |
| `disallow-hostpath-audit` | No `hostPath` volumes used at all |
| `require-readonly-rootfs-audit` | `readOnlyRootFilesystem: true`, with `emptyDir` mounts for the paths nginx needs to write to |
| `disallow-automount-sa-token-audit` | `automountServiceAccountToken: false` |
| `mutate-add-default-labels` | Doesn't block anything — just adds `team`/`managed-by` labels on top |
| `mutate-default-resources` | Doesn't block — resources already fully specified, so nothing gets overwritten |
| `mutate-image-pull-policy` | Doesn't block — sets `imagePullPolicy: IfNotPresent` since tag is versioned |
| `hostpath-exception-by-label` | No hostPath used, so the block/exception logic never triggers |
| `verify-image-signatures-*` | Doesn't apply — these only match `ghcr.io/kyverno/test-verify-image*`, not `nginx` |
| `generate-*` (NetworkPolicy/ResourceQuota/ConfigMap) | Not pod-triggered — these fire on Namespace creation, not Pod creation |

## Check what got mutated automatically

```bash
kubectl get pod good-pod-all-policies -o yaml | grep -A 3 labels:
kubectl get pod good-pod-all-policies -o jsonpath='{.spec.containers[0].imagePullPolicy}'; echo
```

You should see `team=devops` and `managed-by=kyverno` added on top of your own `app`/`env` labels, and `imagePullPolicy: IfNotPresent` set automatically.

## Test 2 — `bad-pod.yaml` (should be REJECTED)

```bash
kubectl apply -f bad-pod.yaml
```

Expected: **rejected**. This pod deliberately violates almost every Enforce policy at once — `:latest` tag, `privileged: true`, missing resources, missing `runAsNonRoot`, and a `hostPath` mount. Kyverno's admission webhook evaluates all matching policies and blocks on the very first Enforce violation it hits — you'll see one specific policy named in the rejection message, even though the pod actually violates several simultaneously. This is expected: Kubernetes admission stops at the first denial rather than aggregating every possible failure.

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```

## What this proves

If both tests behave as expected, your entire GitOps pipeline is validated end-to-end: **Git → ArgoCD → Kyverno → real enforcement on real pods**, with all 17 policies active together, matching how this would actually run in production.
