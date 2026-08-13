# Demo — Task 09

## Apply a pod with NO labels

```bash
kubectl apply -f test-pod.yaml
```

## Inspect what Kyverno injected

```bash
kubectl get pod test-pod-no-labels --show-labels
```

Expected: `team=devops,managed-by=kyverno` — labels you never wrote yourself, added automatically at admission time.

```bash
kubectl get pod test-pod-no-labels -o yaml | grep -A 3 labels:
```

## Prove it doesn't override an explicit value

Edit `test-pod.yaml`, add `labels: {team: platform}` under `metadata`, reapply as a new pod name, and confirm `team` stays `platform` (not overwritten to `devops`) while `managed-by` still gets added.

## Cleanup

```bash
kubectl delete -f test-pod.yaml --ignore-not-found
```
