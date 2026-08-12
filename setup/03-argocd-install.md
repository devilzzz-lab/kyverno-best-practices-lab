# Setup Step 3 — Install ArgoCD

ArgoCD watches the `policies/` folder in this repo on GitHub, and auto-applies every Kyverno policy it finds there — so `git push` becomes your deployment mechanism.

## Install ArgoCD into the cluster

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Wait for it to come up

```bash
kubectl get pods -n argocd -w
```

Wait until all pods are `Running`, then `Ctrl+C`.

## Access the ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open [https://localhost:8080](https://localhost:8080) (accept the self-signed cert warning).

## Get the initial admin password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo
```

Login as `admin` with that password.

## Connect this GitHub repo

Push this repo to GitHub first, then either:

**Via UI:** Settings → Repositories → Connect Repo → paste your repo's HTTPS URL.

**Via CLI** (if you have `argocd` CLI installed):
```bash
argocd login localhost:8080
argocd repo add https://github.com/<your-username>/kyverno-best-practices-lab.git
```

## Create the Application

```bash
kubectl apply -f ../argocd/kyverno-policies-app.yaml
```

(See `argocd/kyverno-policies-app.yaml` in the repo root — it points ArgoCD at the `policies/` folder and enables auto-sync.)

## Verify

```bash
kubectl get application -n argocd
```

You should see `kyverno-policies` with `SYNC STATUS: Synced` and `HEALTH STATUS: Healthy`.

From now on: any `policy.yaml` you add or edit inside `policies/` and push to GitHub is automatically applied to the cluster by ArgoCD — no manual `kubectl apply` needed.
