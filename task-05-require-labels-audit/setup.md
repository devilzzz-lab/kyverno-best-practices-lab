# Setup — Task 05

Assumes your KIND cluster + Kyverno are already running (see `/setup`).

## Apply the policy

```bash
kubectl apply -f policy.yaml
```

## Verify it's registered

```bash
kubectl get clusterpolicy require-labels-audit
```

Expected: `READY: True`. Note the policy shows `Audit` mode, not `Enforce` — check with:

```bash
kubectl get clusterpolicy require-labels-audit -o jsonpath='{.spec.validationFailureAction}'
```
Should print `Audit`.
