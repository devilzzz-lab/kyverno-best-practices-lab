# Demo — Task 14

## Create a new namespace

```bash
kubectl create namespace config-demo-ns
```

## Confirm the ConfigMap was auto-created

```bash
kubectl get configmap -n config-demo-ns
kubectl get configmap namespace-defaults -n config-demo-ns -o yaml
```

Expected: `namespace-defaults` ConfigMap exists with `LOG_LEVEL: info`, `ENVIRONMENT: dev`, `CREATED_BY_POLICY: generate-default-configmap` — none of which you wrote yourself.

## Confirm self-healing

```bash
kubectl delete configmap namespace-defaults -n config-demo-ns
kubectl get configmap -n config-demo-ns
```

Wait a few seconds, check again — it should reappear automatically.

## Cleanup

```bash
kubectl delete namespace config-demo-ns
```
