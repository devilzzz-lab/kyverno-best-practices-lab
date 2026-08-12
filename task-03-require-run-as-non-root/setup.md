# Setup — Task 03

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

## Apply the policy

```bash
kubectl apply -f policy.yaml
```

## Verify it's registered

```bash
kubectl get clusterpolicy require-run-as-non-root
```

Expected: `READY: True`.
