# Setup — Task 15

Assumes your KIND cluster + Kyverno are already running (see `/setup`). Requires cluster egress to `ghcr.io` and the sigstore/rekor transparency log to fetch signature data — this will not work in a fully air-gapped environment.

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy verify-image-signatures-enforce
```

Expected: `READY: True`.
