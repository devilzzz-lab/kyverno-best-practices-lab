# Setup Step 1 — Create the KIND Cluster

We use [KIND](https://kind.sigs.k8s.io/) (Kubernetes in Docker) to run a real local Kubernetes cluster for testing every policy in this repo.

## Prerequisites

- Docker Desktop running
- `kind` CLI installed
- `kubectl` CLI installed

## Create the cluster

```bash
kind create cluster --name kyverno-lab
```

## Verify

```bash
kubectl cluster-info --context kind-kyverno-lab
kubectl get nodes
```

You should see one node in `Ready` status:

```
NAME                        STATUS   ROLES           AGE   VERSION
kyverno-lab-control-plane   Ready    control-plane   30s   v1.xx.x
```

## What just happened

`kind create cluster` pulled the `kindest/node` image and ran it as a Docker container — that container **is** your Kubernetes node (control plane + kubelet + containerd all inside one container). You can see it directly:

```bash
docker ps
```

## Tear down (when you're done with the whole repo)

```bash
kind delete cluster --name kyverno-lab
```
