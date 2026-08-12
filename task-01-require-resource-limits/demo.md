# Demo — Task 01

## Case 1 — Pod with NO resource limits (should be REJECTED)

```bash
kubectl run bad-pod --image=nginx
```

Expected: the request is denied at admission time, with an error referencing `require-resource-limits`:

```
Error from server: admission webhook "validate.kyverno.svc-fail" denied the request:
...
CPU and memory resource requests/limits are required on every container.
```

## Case 2 — Pod WITH resource limits (should SUCCEED)


```bash
kubectl apply -f good-pod.yaml
```

Expected: pod is created normally.

```bash
kubectl get pod good-pod
```

## Check the PolicyReport

```bash
kubectl get policyreport -A
```

You should see a `pass` entry for `good-pod` against `require-resource-limits`. (Rejected pods never get created, so they won't show as `fail` entries here — `Enforce` mode blocks at admission, it doesn't just log.)

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
```
