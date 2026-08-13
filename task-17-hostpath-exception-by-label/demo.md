# Demo — Task 17

## Case 1 — Pod WITHOUT the exception label, mounts hostPath (should be REJECTED)

```bash
kubectl apply -f blocked-pod.yaml
```

Expected: request denied, error referencing `hostpath-exception-by-label`.

## Case 2 — Pod WITH `hostpath-access: allowed` label, mounts hostPath (should SUCCEED)

```bash
kubectl apply -f allowed-pod.yaml
kubectl get pod allowed-pod-etc-access
```

Expected: pod created normally, despite mounting the same `/etc` hostPath.

## Confirm the exception is precisely scoped

```bash
kubectl get pods -l hostpath-access=allowed
```
Only `allowed-pod-etc-access` should show up — this is how you'd audit exactly which workloads have this elevated access in a real cluster.

## The takeaway — Deployment-level, not replica-level

If you scale a Deployment built from `allowed-pod.yaml`'s template to `replicas: 7`, all 7 replicas would be allowed (they all inherit the same label). There is no way to allow only 1 of 7 identical replicas — the exception is scoped to whichever *Deployment* carries the label, not to an individual pod within a replica set.

## Cleanup

```bash
kubectl delete -f allowed-pod.yaml --ignore-not-found
kubectl delete -f blocked-pod.yaml --ignore-not-found
```
