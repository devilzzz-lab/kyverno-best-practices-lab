#!/usr/bin/env python3
"""
parse_audit_log.py

Reads the Kubernetes API server audit log and extracts every request that
Kyverno's admission webhook evaluated — capturing who made the request,
when, in what namespace, on what resource, and whether Kyverno allowed
(Audit mode) or blocked (Enforce mode) it, plus which policy/rule fired.

Usage:
    python3 parse_audit_log.py /path/to/audit.log > events.json
"""

import json
import sys
from datetime import datetime


def is_kyverno_relevant(entry):
    """Only care about Pod/Deployment create/update requests."""
    obj_ref = entry.get("objectRef", {})
    resource = obj_ref.get("resource", "")
    verb = entry.get("verb", "")
    return resource in ("pods", "deployments") and verb in ("create", "update", "patch")


def extract_kyverno_denial(entry):
    """
    If the request was blocked, Kyverno's admission webhook denial message
    is embedded in responseStatus.message. Returns (policy_name, rule_name,
    reason) or (None, None, None) if not a Kyverno denial.
    """
    status = entry.get("responseStatus", {})
    message = status.get("message", "") or ""
    if "admission webhook" in message and "kyverno" in message.lower():
        # Kyverno's denial messages look like:
        # "...denied the request: \n\nresource ... was blocked due to the following policies\n\n<policy>:\n  <rule>: '...'"
        return message
    return None


def parse_line(line):
    try:
        entry = json.loads(line)
    except json.JSONDecodeError:
        return None

    if not is_kyverno_relevant(entry):
        return None

    obj_ref = entry.get("objectRef", {})
    user = entry.get("user", {})
    status = entry.get("responseStatus", {})
    denial_message = extract_kyverno_denial(entry)

    was_blocked = status.get("code", 200) >= 400 and denial_message is not None

    record = {
        "timestamp": entry.get("requestReceivedTimestamp") or entry.get("stageTimestamp"),
        "verb": entry.get("verb"),
        "namespace": obj_ref.get("namespace", "default"),
        "resource_kind": obj_ref.get("resource"),
        "resource_name": obj_ref.get("name"),
        "requesting_user": user.get("username"),
        "user_groups": user.get("groups", []),
        "source_ips": entry.get("sourceIPs", []),
        "outcome": "BLOCKED (Enforce)" if was_blocked else "ALLOWED",
        "response_code": status.get("code"),
        "kyverno_message": denial_message,
    }
    return record


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse_audit_log.py <audit.log path>", file=sys.stderr)
        sys.exit(1)

    audit_log_path = sys.argv[1]
    events = []

    with open(audit_log_path, "r") as f:
        for line in f:
            record = parse_line(line.strip())
            if record:
                events.append(record)

    print(json.dumps(events, indent=2))


if __name__ == "__main__":
    main()
