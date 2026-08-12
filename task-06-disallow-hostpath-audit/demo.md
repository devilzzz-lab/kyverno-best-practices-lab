# Demo — Task 06

Both pods will be CREATED (Audit mode doesn't block). The difference shows up in the PolicyReport.

## Case 1 — Pod with hostPath volume

```bash
kubectl apply -f bad-pod.yaml
kubectl get pod bad-pod-hostpath
```

## Case 2 — Pod with no hostPath volume

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-no-hostpath
```

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep -E "bad-pod-hostpath|good-pod-no-hostpath"
```

Expected: `bad-pod-hostpath` → `FAIL: 1`, `good-pod-no-hostpath` → `PASS: 1`.

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```
