# Setup — Task 06

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy disallow-hostpath-audit
```

Expected: `READY: True`.
