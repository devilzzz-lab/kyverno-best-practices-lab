# Demo — Task 04

## Case 1 — Pod with `privileged: true` (should be REJECTED)

```bash
kubectl apply -f bad-pod.yaml
```

Expected: request denied, error referencing `disallow-privileged-containers`.

## Case 2 — Pod without `privileged` set (should SUCCEED)

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-unprivileged
```

Expected: pod created normally.

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep disallow-privileged-containers
```

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```
