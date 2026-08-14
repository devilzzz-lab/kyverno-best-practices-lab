# Audit Reporting — Who Triggered Which Policy, and What Happened

This folder answers: **"someone applied a pod/deployment — which namespace, what time, which service account, was it blocked (Enforce) or just flagged (Audit), and which policy fired?"**

## Two data sources, because the answer needs both

| Question | Source | Script |
|---|---|---|
| Who applied it, when, from where, was it **blocked**? | Kubernetes API server **audit log** | `parse_audit_log.py` |
| Which **Audit**-mode policy flagged a resource that was still **allowed**? | Kyverno **PolicyReport** CRDs | `fetch_policy_reports.py` |

This split exists because of how Kyverno actually works:
- **Enforce mode** — Kyverno's admission webhook rejects the request outright. The rejection reason (policy name + rule + message) is embedded directly in the API server's response, which the audit log captures. So blocked events are fully explained by the audit log alone.
- **Audit mode** — Kyverno lets the request through untouched. The pass/fail verdict is written separately to a `PolicyReport` object, *after* admission. The audit log has no idea a violation was even flagged — it just sees a normal, successful create. So audit-mode violations can only be found by querying `PolicyReport`.

Neither source alone gives the full picture — that's why there are two scripts.

## Setup

1. Follow [`01-enable-audit-logging.md`](01-enable-audit-logging.md) first — your KIND cluster needs to be recreated with audit logging turned on. (Skip this if you already have a cluster running with the audit config.)
2. Reinstall Kyverno + ArgoCD + sync all 17 policies as usual.

## Usage

### Get blocked (Enforce) events

```bash
docker exec kyverno-lab-control-plane cat /var/log/kubernetes/audit/audit.log > audit-reporting/audit-logs/audit.log
python3 audit-reporting/parse_audit_log.py audit-reporting/audit-logs/audit.log > audit-reporting/blocked-events.json
```

Each entry includes: `timestamp`, `namespace`, `resource_kind`, `resource_name`, `requesting_user`, `user_groups`, `source_ips`, `outcome` (`BLOCKED (Enforce)` / `ALLOWED`), and `kyverno_message` (the full policy + rule + reason, when blocked).

### Get audit-mode flagged (but allowed) events

```bash
python3 audit-reporting/fetch_policy_reports.py > audit-reporting/audit-mode-events.json
```

Each entry includes: `namespace`, `policy`, `rule`, `resource_kind`, `resource_name`, `result` (`pass`/`fail`/`warn`), `message`, `timestamp`.

## What "requesting user / service account" will actually show on KIND

On a real cluster, `requesting_user` will show a human's identity (e.g. `sriram@company.com` via SSO) if they used `kubectl` with their own credentials, or a service account (`system:serviceaccount:<namespace>:<name>`) if a CI/CD pipeline or controller applied it. On a local KIND cluster, since you're the only person applying things with the default kubeconfig, this will typically show `kubernetes-admin` for everything you do manually via `kubectl`, and the ArgoCD service account for anything ArgoCD syncs. This becomes far more meaningful on a real multi-user EKS cluster — see the note in the root `README.md` about porting this there.

## Next step

Once both JSON files are generating correctly, the next stage is combining them into a single PDF report and emailing it — that's a separate task once this data-capture step is confirmed working.
