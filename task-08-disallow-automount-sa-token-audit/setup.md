# Setup — Task 08

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy disallow-automount-sa-token-audit
```

Expected: `READY: True`.
