# Setup — Task 11

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

This policy assumes `:latest` is not blocked cluster-wide. If Task 02's `disallow-latest-tag` (Enforce) is still applied, the `:latest` test pod below will be rejected before this mutate rule ever sees it — temporarily remove or Audit Task 02's policy if you want to test both mutation paths, or see `setup/change.md` for how to isolate testing.

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy mutate-image-pull-policy
```

Expected: `READY: True`.
