# Demo — Task 11

## Case 1 — Pod using `:latest`

```bash
kubectl apply -f latest-tag-pod.yaml
kubectl get pod latest-tag-pod -o jsonpath='{.spec.containers[0].imagePullPolicy}'; echo
```

Expected: `Always` — injected automatically because the image tag is `:latest`.

## Case 2 — Pod using a versioned tag, no pull policy set

```bash
kubectl apply -f versioned-tag-pod.yaml
kubectl get pod versioned-tag-pod -o jsonpath='{.spec.containers[0].imagePullPolicy}'; echo
```

Expected: `IfNotPresent` — injected automatically because the tag is immutable.

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep -E "latest-tag-pod|versioned-tag-pod"
```

## Cleanup

```bash
kubectl delete -f latest-tag-pod.yaml --ignore-not-found
kubectl delete -f versioned-tag-pod.yaml --ignore-not-found
```
