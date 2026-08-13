# Demo — Task 16

Both pods will be CREATED (Audit mode doesn't block).

## Case 1 — Signed image

```bash
kubectl apply -f signed-pod.yaml
kubectl get pod signed-pod-audit
```

## Case 2 — Unsigned image

```bash
kubectl apply -f unsigned-pod.yaml
kubectl get pod unsigned-pod-audit
```

Expected: pod is created successfully despite lacking a valid signature — Audit mode only logs the violation.

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep -E "signed-pod-audit|unsigned-pod-audit"
```

Expected: `signed-pod-audit` → `PASS: 1`, `unsigned-pod-audit` → `FAIL: 1`.

## Cleanup

```bash
kubectl delete -f signed-pod.yaml --ignore-not-found
kubectl delete -f unsigned-pod.yaml --ignore-not-found
```
