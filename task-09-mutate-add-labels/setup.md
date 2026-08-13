# Setup — Task 09

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy mutate-add-default-labels
```

Expected: `READY: True`.
