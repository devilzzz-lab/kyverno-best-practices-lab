# Setup — Task 07

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy require-readonly-rootfs-audit
```

Expected: `READY: True`.
