# Demo — Task 05

This is the key difference from Tasks 01-04: **nothing gets rejected here.** Both pods will be created. What differs is what shows up in the `PolicyReport`.

## Case 1 — Pod with NO labels (created anyway, but logged as a violation)

```bash
kubectl apply -f bad-pod.yaml
kubectl get pod bad-pod-no-labels
```

Expected: pod is created successfully — Audit mode does not block it.

## Case 2 — Pod WITH `app`/`env` labels (created, and passes)

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-labeled
```

## Check the PolicyReport — this is where Audit mode actually shows its result

```bash
kubectl get policyreport -A | grep -E "bad-pod-no-labels|good-pod-labeled"
```

Expected: `bad-pod-no-labels` shows `FAIL: 1`, `good-pod-labeled` shows `PASS: 1`.

For full detail on the failure:
```bash
kubectl describe policyreport -n default | grep -A 10 bad-pod-no-labels
```

## The takeaway

Compare this to Task 01-04's `Enforce` behavior: there, `bad-pod` never got created at all. Here, both pods exist — Audit mode is purely observational. This is how you'd stage a new policy before turning on hard enforcement.

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```
