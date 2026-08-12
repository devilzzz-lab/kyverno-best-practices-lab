# Setup Step 2 — Install Kyverno

## Add the Helm repo

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update
```

## Install

```bash
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
```

## Verify

```bash
kubectl get pods -n kyverno -w
```

Wait until you see **4 pods** in `Running` state, then `Ctrl+C`:

```
kyverno-admission-controller-xxxxx     1/1   Running
kyverno-background-controller-xxxxx    1/1   Running
kyverno-cleanup-controller-xxxxx       1/1   Running
kyverno-reports-controller-xxxxx       1/1   Running
```

## Confirm the webhooks are registered

```bash
kubectl get validatingwebhookconfigurations | grep kyverno
kubectl get mutatingwebhookconfigurations | grep kyverno
```

If both return results, Kyverno is actively intercepting admission requests and you're ready to start on `task-01`.

## Uninstall (if you ever need to reset just Kyverno, not the whole cluster)

```bash
helm uninstall kyverno -n kyverno
kubectl delete ns kyverno
```
