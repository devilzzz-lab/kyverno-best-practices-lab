# Demo — Task 10

## Case 1 — Pod with NO resources set at all

```bash
kubectl apply -f no-resources-pod.yaml
kubectl get pod no-resources-pod -o jsonpath='{.spec.containers[0].resources}'; echo
```

Expected: shows the full injected block — `requests: {cpu: 100m, memory: 128Mi}`, `limits: {cpu: 250m, memory: 256Mi}` — even though you never wrote it.

## Case 2 — Pod with a PARTIAL resources block (`requests` set, `limits` missing)

```bash
kubectl apply -f partial-resources-pod.yaml
kubectl get pod partial-resources-pod -o jsonpath='{.spec.containers[0].resources}'; echo
```

Expected: `requests.cpu` stays `100m` and `requests.memory` stays `200Mi` (your values, untouched), while `limits.cpu: 250m` and `limits.memory: 256Mi` get filled in automatically since `limits` was missing entirely.

**Important constraint to understand:** Kubernetes requires `requests <= limits` for every resource. If your partial pod's `requests` value is *higher* than the default limit this policy injects (`250m` CPU / `256Mi` memory), the pod will be rejected — not by Kyverno, but by the Kubernetes API server's own validation, since the mutated result would violate that constraint. That's why `partial-resources-pod.yaml` uses modest values (`100m`/`200Mi`) that stay comfortably under the injected defaults.

## Check the PolicyReport (mutate rules also log a pass/mutation record)

```bash
kubectl get policyreport -A | grep -E "no-resources-pod|partial-resources-pod"
```

## Cleanup

```bash
kubectl delete -f no-resources-pod.yaml --ignore-not-found
kubectl delete -f partial-resources-pod.yaml --ignore-not-found
```
