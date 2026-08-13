# Switching Between GitOps (ArgoCD) and Manual Policy Testing

When ArgoCD's auto-sync is ON, it will keep re-creating/reverting any `ClusterPolicy` you manually delete or edit (self-heal). Use this guide to temporarily pause that so you can test policies in isolation, then switch back.

---

## Step 1 — Turn OFF auto-sync

```bash
kubectl patch application kyverno-policies -n argocd --type merge -p '{"spec":{"syncPolicy":{"automated":null}}}'
```

ArgoCD now only watches — it won't auto-apply or revert anything. Existing policies stay on the cluster untouched.

---

## Step 2 — Delete all policies for a clean slate

```bash
kubectl delete clusterpolicy --all
kubectl get clusterpolicy
```

Expected: `No resources found` — clean cluster, ready for isolated manual testing.

---

## Step 3 — Manually test whatever you want

Apply individual `policy.yaml` files from any `task-NN-*/` folder, test with `bad-pod.yaml` / `good-pod.yaml`, delete, repeat — without ArgoCD interfering.

```bash
kubectl apply -f task-05-require-labels-audit/policy.yaml
# ...test...
kubectl delete -f task-05-require-labels-audit/policy.yaml
```

---

## Step 4 — Turn auto-sync back ON

```bash
kubectl patch application kyverno-policies -n argocd --type merge -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
```

## Step 5 — Force an immediate re-sync (don't wait for ArgoCD's poll interval)

```bash
kubectl patch application kyverno-policies -n argocd --type merge -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'
```

## Step 6 — Verify everything came back

```bash
kubectl get clusterpolicy
```

All policies from `policies/` in Git should reappear, `READY: True`. You don't need a fresh `git push` for this — ArgoCD just re-syncs to whatever's already in the repo. You'd only need to `git push` if you also edited something in `policies/` since the last sync.
