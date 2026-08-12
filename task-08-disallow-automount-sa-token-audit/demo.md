# Demo — Task 08

Both pods will be CREATED (Audit mode doesn't block).

## Case 1 — Pod with default token mounting (no field set)

```bash
kubectl apply -f bad-pod.yaml
kubectl get pod bad-pod-default-token
```

## Case 2 — Pod with `automountServiceAccountToken: false`

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-no-automount
```

## Bonus — prove the difference in what's actually mounted

```bash
kubectl exec bad-pod-default-token -- ls /var/run/secrets/kubernetes.io/serviceaccount/
```
Expected: shows `token`, `ca.crt`, `namespace` — the token IS mounted.

```bash
kubectl exec good-pod-no-automount -- ls /var/run/secrets/kubernetes.io/serviceaccount/
```
Expected: `ls: /var/run/secrets/kubernetes.io/serviceaccount/: No such file or directory` — no token mounted at all.

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep -E "bad-pod-default-token|good-pod-no-automount"
```

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```
