# Demo — Task 07

Both pods will be CREATED (Audit mode doesn't block).

## Case 1 — Pod with default (writable) root filesystem

```bash
kubectl apply -f bad-pod.yaml
kubectl get pod bad-pod-writable-rootfs
```

## Case 2 — Pod with `readOnlyRootFilesystem: true`

```bash
kubectl apply -f good-pod.yaml
kubectl get pod good-pod-readonly-rootfs
```

Note this manifest also mounts `emptyDir` volumes for the paths nginx needs to write to (`/tmp`, `/var/cache/nginx`, `/var/run`) — this is the real-world pattern: read-only root + specific writable mounts.

## Bonus — prove the filesystem is actually read-only

```bash
kubectl exec good-pod-readonly-rootfs -- touch /test-file
```
Expected: `touch: /test-file: Read-only file system`

```bash
kubectl exec bad-pod-writable-rootfs -- touch /test-file
```
Expected: succeeds silently — proving the contrast.

## Check the PolicyReport

```bash
kubectl get policyreport -A | grep -E "bad-pod-writable-rootfs|good-pod-readonly-rootfs"
```

## Cleanup

```bash
kubectl delete -f good-pod.yaml --ignore-not-found
kubectl delete -f bad-pod.yaml --ignore-not-found
```
