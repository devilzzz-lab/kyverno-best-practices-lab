# Setup — Task 16

Assumes your KIND cluster + Kyverno are already running (see `/setup`). Requires cluster egress to `ghcr.io` and the sigstore/rekor transparency log.

```bash
kubectl apply -f policy.yaml
kubectl get clusterpolicy verify-image-signatures-audit
```

Expected: `READY: True`.

**Note:** `verifyImages` rules require `mutateDigest: false` explicitly set when using `Audit` mode — Kyverno's admission webhook rejects `mutateDigest: true` (the default) under Audit, since digest-pinning is an enforcement-time action. This is already set correctly in `policy.yaml`.
