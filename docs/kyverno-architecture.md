# Kyverno Architecture

## What Kyverno is

Kyverno is a **policy engine designed specifically for Kubernetes**. It runs as a set of controllers inside your cluster and enforces rules on resources as they're created, updated, or deleted — written entirely in YAML, with no separate policy language to learn.

## Why Kyverno over alternatives (e.g. OPA/Gatekeeper)

- **No new DSL** — OPA/Gatekeeper uses Rego, a purpose-built query language. Kyverno policies are Kubernetes-native YAML, so anyone who can write a manifest can write a policy.
- **Built-in mutation and generation** — not just validation. Kyverno can rewrite incoming resources (mutate) or spawn new resources in response to events (generate), which Gatekeeper doesn't do natively.
- **Image verification built in** — native cosign integration for supply-chain security (`verifyImages` rules).
- Faster ramp-up for teams already comfortable with Kubernetes manifests.

## Where it sits in the request flow

```
kubectl apply
      │
      ▼
API Server ── AuthN ── AuthZ ──▶ Admission Webhooks
                                        │
                                        ▼
                             Kyverno Admission Controller
                          (validate / mutate / verifyImages)
                                        │
                              allow / deny / mutate
                                        │
                                        ▼
                                     etcd
```

Kyverno registers itself as a `ValidatingWebhookConfiguration` and `MutatingWebhookConfiguration`. Every matching resource request passes through Kyverno **before** it's persisted.

## Core components

| Component | Responsibility |
|---|---|
| `kyverno-admission-controller` | The webhook itself — intercepts live requests, enforces validate/mutate/verifyImages rules in real time |
| `kyverno-background-controller` | Runs `generate` rules and reconciles them in the background (e.g. keeps a generated NetworkPolicy in sync with its source policy) |
| `kyverno-cleanup-controller` | Executes `CleanupPolicy` resources — TTL-style automatic deletion of matching resources |
| `kyverno-reports-controller` | Continuously scans the cluster in `audit` mode and produces `PolicyReport` / `ClusterPolicyReport` CRDs |

## Policy resource types

- `ClusterPolicy` — applies cluster-wide
- `Policy` — applies to a single namespace

## Rule types

- **validate** — allow or deny a resource based on a pattern or CEL/JSON expression. Can run in `Enforce` (block) or `Audit` (log only) mode.
- **mutate** — rewrite incoming resources (e.g. inject labels, defaults, sidecars) before they're persisted.
- **generate** — create new resources in response to another resource's lifecycle (e.g. auto-create a NetworkPolicy when a Namespace is created).
- **verifyImages** — verify container image signatures (cosign) and/or attestations before allowing a Pod to run.

## Enforce vs Audit

- `validationFailureAction: Enforce` — non-compliant resources are **rejected** at admission time.
- `validationFailureAction: Audit` — non-compliant resources are **allowed**, but logged as a violation in a `PolicyReport`.

Most teams roll out new policies in `Audit` mode first to see what would break, then switch to `Enforce` once they're confident.

## Observability: PolicyReports

Kyverno continuously reports policy pass/fail status per resource via:
- `PolicyReport` — namespaced
- `ClusterPolicyReport` — cluster-scoped

These are standard Kubernetes CRDs, so they're queryable with `kubectl get policyreport -A` and can be scraped by dashboards or compliance tooling.
