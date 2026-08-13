# Demo — Task 12

## Create a new namespace

```bash
kubectl create namespace demo-app-ns
```

## Confirm the NetworkPolicy was auto-created — you never wrote this yourself

```bash
kubectl get networkpolicy -n demo-app-ns
kubectl get networkpolicy default-deny-all -n demo-app-ns -o yaml
```

Expected: a `default-deny-all` NetworkPolicy exists, with empty `podSelector: {}` (applies to all pods) and both `Ingress`/`Egress` denied.

## Confirm self-healing (synchronize: true)

```bash
kubectl delete networkpolicy default-deny-all -n demo-app-ns
kubectl get networkpolicy -n demo-app-ns
```

Wait a few seconds and check again — it should reappear automatically, recreated by Kyverno's background controller.

## Confirm system namespaces were correctly excluded

```bash
kubectl get networkpolicy -n kube-system
```

Expected: no `default-deny-all` here — the exclude list in the policy prevented it.

## Cleanup

```bash
kubectl delete namespace demo-app-ns
```
