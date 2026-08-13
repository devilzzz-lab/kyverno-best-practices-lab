# Demo — Task 10

## Case 1 — Pod with NO resources set at all

```bash
kubectl apply -f no-resources-pod.yaml
kubectl get pod no-resources-pod -o jsonpath='{.spec.containers[0].resources}'; echo
```

Expected: shows the full injected block — `requests: {cpu: 100m, memory: 128Mi}`, `limits: {cpu: 250m, memory: 256Mi}` — even though you never wrote it.

## Case 2 — Pod with a PARTIAL resources block (only `cpu` request set)

```bash
kubectl apply -f partial-resources-pod.yaml
kubectl get pod partial-resources-pod -o jsonpath='{.spec.containers[0].resources}'; echo
```

Expected: `requests.cpu` stays `500m` (your value, untouched), but `requests.memory`, `limits.cpu`, `limits.memory` all get the defaults filled in around it.

## Check the PolicyReport (mutate rules also log a pass/mutation record)

```bash
kubectl get policyreport -A | grep -E "no-resources-pod|partial-resources-pod"
```

## Cleanup

```bash
kubectl delete -f no-resources-pod.yaml --ignore-not-found
kubectl delete -f partial-resources-pod.yaml --ignore-not-found
```
