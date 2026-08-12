# Demo — Task 02

## Case 1 — Pod using `:latest` (should be REJECTED)

```bash
kubectl apply -f bad-pod.yaml
```

Expected: request denied, error referencing `disallow-latest-tag`.

## Case 2 — Pod using an explicit version tag (should SUCCEED)

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-versioned
```

Expected: pod created normally.

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep disallow-latest-tag
```

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```
