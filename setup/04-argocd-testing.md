# Testing ArgoCD Sync — GitOps Flow Verification

This doc is only about proving **ArgoCD** correctly syncs policies from Git to the cluster. It does **not** cover testing individual policies — that's done manually per task (see `task-NN-*/demo.md` files), using `kubectl apply` on `good-pod.yaml` / `bad-pod.yaml`. Keep these two concerns separate:

- **ArgoCD test (this doc)** → proves Git → cluster sync works for policy YAMLs
- **Task demo test (`task-NN-*/demo.md`)** → proves a specific policy blocks/allows pods correctly, applied manually by you

---

## Test 1 — Confirm ArgoCD is synced and healthy right now

```bash
kubectl get application -n argocd
```

Expected:
```
NAME                SYNC STATUS   HEALTH STATUS
kyverno-policies    Synced        Healthy
```

```bash
kubectl get clusterpolicy
```

You should see all 4 policies currently in `policies/` listed here, all `READY: True` — proving ArgoCD deployed them, not a manual `kubectl apply` from you.

---

## Test 2 — Push a valid new policy and watch ArgoCD auto-apply it

1. Add a new (correct) policy file to `policies/`, e.g. copy `policies/01-require-resource-limits.yaml` to `policies/99-test-policy.yaml` and rename the `metadata.name` to `test-policy`.
2. Commit and push:
   ```bash
   git add policies/99-test-policy.yaml
   git commit -m "test: add test policy to verify argocd sync"
   git push
   ```
3. Watch ArgoCD pick it up (default poll interval ~3 min, or force it):
   ```bash
   kubectl get application -n argocd -w
   ```
4. Confirm it landed on the cluster:
   ```bash
   kubectl get clusterpolicy test-policy
   ```
   It should exist — **without you ever running `kubectl apply` yourself.**

5. Clean up: delete `policies/99-test-policy.yaml`, commit, push. ArgoCD's `prune: true` should automatically remove it from the cluster too:
   ```bash
   kubectl get clusterpolicy test-policy
   ```
   Expected: `Error from server (NotFound)` — proof that deleting from Git deletes from the cluster.

---

## Test 3 — Push a BROKEN policy and watch ArgoCD flag it

1. Add a deliberately broken policy, e.g. `policies/99-broken-policy.yaml`:
   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: broken-policy
   spec:
     validationFailureAction: Enforce
     rules:
       - name: broken-rule
         match:
           any:
           - resources:
               kinds:
                 - Pod
         validate:
           # intentionally missing "message" and "pattern" — invalid rule body
   ```
2. Commit and push:
   ```bash
   git add policies/99-broken-policy.yaml
   git commit -m "test: push intentionally broken policy"
   git push
   ```
3. Check ArgoCD's sync status:
   ```bash
   kubectl get application -n argocd
   ```
   Expected: `SYNC STATUS` or `HEALTH STATUS` shows an error state (e.g. `Degraded` or sync failure), instead of silently applying garbage.

4. Get the actual error:
   ```bash
   kubectl describe application kyverno-policies -n argocd
   ```
   Look at the `Conditions` / `Status` section — it will show the rejection reason (either a YAML parse error or Kyverno's own API validation error).

5. Also check via the ArgoCD UI (`https://localhost:8080`) — the `kyverno-policies` app tile will show a red/error state with the same detail.

6. Clean up: delete `policies/99-broken-policy.yaml`, commit, push.

---

## What each test proves

| Test | Proves |
|---|---|
| Test 1 | Baseline sync is healthy |
| Test 2 | Git push → cluster apply (and prune on delete) works automatically |
| Test 3 | ArgoCD surfaces broken policies instead of silently failing |

Once all 3 pass, your GitOps loop for Kyverno policies is confirmed working end-to-end.
