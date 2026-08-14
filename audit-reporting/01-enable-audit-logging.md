# Setup — Enable Audit Logging on KIND

Your current KIND cluster was created without audit logging. We need to **recreate it** using a config that mounts an audit policy and turns on the API server's audit log — this is what lets us capture "who did what, when, and was it blocked."

This will wipe your current cluster (policies, test pods, ArgoCD — all of it). You'll need to re-run the setup steps afterward.

## Step 1 — Create the local audit log directory

Run this from the repo root (`kyverno-best-practices-lab/`):

```bash
mkdir -p audit-reporting/audit-logs
```

## Step 2 — Delete the existing cluster

```bash
kind delete cluster --name kyverno-lab
```

## Step 3 — Recreate the cluster WITH audit logging enabled

Run this from the repo root, so the relative paths in `kind-config-with-audit.yaml` resolve correctly:

```bash
kind create cluster --config audit-reporting/kind-config-with-audit.yaml
```

## Step 4 — Verify audit logging is actually working

```bash
kubectl get nodes
docker exec kyverno-lab-control-plane ls -la /var/log/kubernetes/audit/
```

You should see `audit.log` growing in size. To confirm it's capturing real events:

```bash
docker exec kyverno-lab-control-plane tail -5 /var/log/kubernetes/audit/audit.log
```

You should see JSON lines with fields like `"user"`, `"verb"`, `"objectRef"`, `"responseStatus"`.

## Step 5 — Reinstall everything else

Follow, in order:
1. [`setup/02-kyverno-install.md`](../setup/02-kyverno-install.md)
2. [`setup/03-argocd-install.md`](../setup/03-argocd-install.md)
3. Push/re-sync your `policies/` folder as before

Once Kyverno + ArgoCD + all 17 policies are back up, move on to [`README.md`](README.md) in this folder to run the report generator.
