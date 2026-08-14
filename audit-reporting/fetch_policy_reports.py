#!/usr/bin/env python3
"""
fetch_policy_reports.py

Complements parse_audit_log.py. The API server audit log only tells you
WHO did WHAT and WHETHER it was blocked — it does NOT tell you which
specific Audit-mode policy flagged a resource that was still allowed
through, because Audit mode never touches the request at admission time.

That information only exists in Kyverno's PolicyReport / ClusterPolicyReport
CRDs, which this script queries directly via kubectl.

Usage:
    python3 fetch_policy_reports.py > policy_report_events.json

Requires: kubectl configured against the cluster, and the `kubectl` binary
on PATH.
"""

import json
import subprocess
import sys


def run_kubectl(args):
    result = subprocess.run(
        ["kubectl"] + args,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"kubectl error: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout


def fetch_all_policy_reports():
    raw = run_kubectl(["get", "policyreport", "-A", "-o", "json"])
    if not raw:
        return []
    data = json.loads(raw)
    return data.get("items", [])


def extract_events(reports):
    events = []
    for report in reports:
        namespace = report.get("metadata", {}).get("namespace", "unknown")
        for result in report.get("results", []):
            events.append({
                "namespace": namespace,
                "policy": result.get("policy"),
                "rule": result.get("rule"),
                "resource_kind": (result.get("resources", [{}])[0] or {}).get("kind"),
                "resource_name": (result.get("resources", [{}])[0] or {}).get("name"),
                "result": result.get("result"),  # pass / fail / warn / error / skip
                "message": result.get("message"),
                "timestamp": result.get("timestamp"),
            })
    return events


def main():
    reports = fetch_all_policy_reports()
    events = extract_events(reports)
    print(json.dumps(events, indent=2))


if __name__ == "__main__":
    main()
