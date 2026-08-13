# Setup — Task 16

Assumes your KIND cluster + Kyverno are already running (see `/setup`). Requires cluster egress to `ghcr.io` and the sigstore/rekor transparency log.

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy verify-image-signatures-audit
```

Expected: `READY: True`.
