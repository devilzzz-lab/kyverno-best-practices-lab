# Demo — Task 03

## Case 1 — Pod with no `runAsNonRoot` set (should be REJECTED)

```bash
kubectl apply -f bad-pod.yaml
```

Expected: request denied, error referencing `require-run-as-non-root`.

## Case 2 — Pod with `runAsNonRoot: true` (should SUCCEED)

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-nonroot
```

Expected: pod created normally.

## Bonus — confirm it's actually running as non-root

```bash
kubectl exec good-pod-nonroot -- id
```

Should show `uid=1000` (not `uid=0`).

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep require-run-as-non-root
```

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```
