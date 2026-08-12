# Kyverno Best Practices Lab

Hands-on lab covering **10 real-world Kyverno policies**, built and tested on a local KIND cluster. Each task is self-contained: what the policy does, why it matters, how to set it up, and how to prove it works.

## Why Kyverno

Kyverno is a Kubernetes-native policy engine. Unlike OPA/Gatekeeper (which requires learning Rego), Kyverno policies are plain YAML — the same format you already use for any Kubernetes manifest. It runs as a dynamic admission controller, intercepting requests to the API server to **validate**, **mutate**, or **generate** resources, and can also verify image signatures.

See [`docs/kyverno-architecture.md`](docs/kyverno-architecture.md) for the full architecture breakdown.

## Repo structure

```
kyverno-best-practices-lab/
├── docs/
│   └── kyverno-architecture.md      # How Kyverno works internally
├── setup/
│   ├── 01-cluster-setup.md          # Create the local KIND cluster
│   └── 02-kyverno-install.md        # Install Kyverno via Helm
├── task-01-require-resource-limits/
├── task-02-disallow-latest-tag/
├── task-03-require-run-as-non-root/
├── task-04-disallow-privileged-containers/
├── task-05-require-labels/
├── task-06-auto-add-labels-mutate/
├── task-07-restrict-image-registries/
├── task-08-generate-default-networkpolicy/
├── task-09-require-probes/
└── task-10-image-signature-verification/
```

Each `task-NN-*` folder contains:
- `README.md` — what the policy does and why it matters
- `setup.md` — commands to apply the policy
- `demo.md` — commands to prove it works (pass/fail cases)
- `policy.yaml` — the actual Kyverno policy

## Getting started

1. Follow [`setup/01-cluster-setup.md`](setup/01-cluster-setup.md) to create the KIND cluster.
2. Follow [`setup/02-kyverno-install.md`](setup/02-kyverno-install.md) to install Kyverno.
3. Work through `task-01` → `task-10` in order — they go from simple validation rules up to advanced image signature verification.

## Task index

| # | Task | Rule Type | Category |
|---|------|-----------|----------|
| 01 | Require resource requests/limits | validate | Reliability |
| 02 | Disallow `:latest` image tag | validate | Supply chain hygiene |
| 03 | Require `runAsNonRoot` | validate | Pod security |
| 04 | Disallow privileged containers | validate | Pod security |
| 05 | Require standard labels | validate | Governance |
| 06 | Auto-inject default labels | mutate | Automation |
| 07 | Restrict allowed image registries | validate | Supply chain security |
| 08 | Auto-generate default-deny NetworkPolicy | generate | Network security |
| 09 | Require liveness/readiness probes | validate | Reliability |
| 10 | Verify image signatures (cosign) | verifyImages | Supply chain security (advanced) |
