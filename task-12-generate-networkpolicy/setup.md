# Setup — Task 12

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy generate-default-deny-netpol
```

Expected: `READY: True`.
