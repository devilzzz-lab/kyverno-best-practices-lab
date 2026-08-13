# Setup — Task 10

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy mutate-default-resources
```

Expected: `READY: True`.

Note: this policy is normally used together with Task 01's `require-resource-limits` Enforce policy — if both are on the cluster at once, this mutate rule runs first (backfills defaults), so Task 01's validate check should always pass afterward.
