# Setup — Task 01

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

## Apply the policy

```bash
kubectl apply -f policy.yaml
```

## Verify it's registered

```bash
kubectl get clusterpolicy require-resource-limits
```

Expected output:
```
NAME                       BACKGROUND   VALIDATE ACTION   READY
require-resource-limits    true         Enforce           true
```

`READY: true` means Kyverno has successfully loaded the policy and it's actively enforcing.
