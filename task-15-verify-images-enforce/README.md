# Task 15 — Verify Image Signatures with Cosign (Enforce)

## What this policy does

Only allows Pods to run if their container image (matching `ghcr.io/kyverno/test-verify-image:*`) is **cryptographically signed** by a trusted key, verified via [cosign](https://github.com/sigstore/cosign). Unsigned or tampered images are rejected outright (`Enforce`).

This uses Kyverno's official test image and public key from the [Kyverno image verification docs](https://kyverno.io/docs/writing-policies/verify-images/) — safe to test against without needing to sign your own images first.

## Why it matters

Anyone can push an image to a registry, including a compromised CI pipeline, a leaked credential, or a malicious insider. Without image signature verification, Kubernetes has no way to know whether the image it's about to run is the exact, untampered artifact your build pipeline produced. This is the core of **software supply chain security** — the same class of concern behind incidents like SolarWinds and the broader push toward SLSA/sigstore adoption industry-wide.

`verifyImages` moves trust from "the registry says this tag exists" to "cryptographic proof this exact image was signed by a key we trust."

## Rule type

`verifyImages`, mode: `Enforce` — behaves like `validationFailureAction` on a validate rule; non-conforming images are blocked at admission.

## Files

- `policy.yaml` — the ClusterPolicy
- `signed-pod.yaml` — uses Kyverno's official pre-signed test image (should SUCCEED)
- `unsigned-pod.yaml` — uses a normal, unsigned public image (should be REJECTED)
- `setup.md` — how to apply the policy
- `demo.md` — how to prove signature verification works
