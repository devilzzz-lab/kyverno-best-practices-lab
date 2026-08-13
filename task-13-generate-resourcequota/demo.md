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
cat <<EOF | kubectl apply -n quota-demo-ns -f -
apiVersion: v1
kind: Pod
metadata:
  name: quota-test-$i
spec:
  containers:
  - name: nginx
    image: nginx:1.25
    resources:
      requests:
        cpu: 10m
        memory: 16Mi
      limits:
        cpu: 20m
        memory: 32Mi
EOF
done
```

Expected: the 21st pod creation fails with a quota-exceeded error.

## Cleanup

```bash
kubectl delete namespace quota-demo-ns --grace-period 0 --force
```


