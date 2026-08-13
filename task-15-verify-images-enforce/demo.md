# Demo — Task 15

## Case 1 — Pod using the SIGNED test image (should SUCCEED)

```bash
kubectl apply -f signed-pod.yaml
kubectl get pod signed-pod
```

Expected: pod created — Kyverno verified the cosign signature against the trusted public key in the policy.

## Case 2 — Pod using the UNSIGNED test image (should be REJECTED)

```bash
kubectl apply -f unsigned-pod.yaml
```

Expected: request denied — no valid signature found matching the trusted key.

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep verify-image-signatures-enforce
```

## Cleanup

```bash
kubectl delete -f signed-pod.yaml --ignore-not-found
kubectl delete -f unsigned-pod.yaml --ignore-not-found
```
