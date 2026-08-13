# Demo — Task 13

## Create a new namespace

```bash
kubectl create namespace quota-demo-ns
```

## Confirm the ResourceQuota was auto-created

```bash
kubectl get resourcequota -n quota-demo-ns
kubectl describe resourcequota default-quota -n quota-demo-ns
```

Expected: `default-quota` exists with the hard limits from the policy (`requests.cpu: 2`, `requests.memory: 2Gi`, `limits.cpu: 4`, `limits.memory: 4Gi`, `pods: 20`).

## Prove the quota is actually enforced

Try creating 21 tiny pods in this namespace (exceeding the `pods: 20` cap) — the 21st should be rejected by the ResourceQuota admission check, independent of Kyverno:

```bash
for i in $(seq 1 21); do
  kubectl run quota-test-$i --image=nginx:1.25 -n quota-demo-ns \
    --requests='cpu=10m,memory=16Mi' --limits='cpu=20m,memory=32Mi' 2>&1 | tail -1
done
```

(If your `kubectl` version doesn't support `--requests`/`--limits` flags, use a small pod manifest looped instead.)

Expected: the 21st pod creation fails with a quota-exceeded error.

## Cleanup

```bash
kubectl delete namespace quota-demo-ns
```
