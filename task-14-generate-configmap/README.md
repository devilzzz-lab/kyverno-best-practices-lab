# Task 14 — Auto-generate Default ConfigMap (Generate)

## What this policy does

Whenever a new Namespace is created, Kyverno automatically creates a baseline `ConfigMap` called `namespace-defaults` inside it, pre-populated with common default values (`LOG_LEVEL`, `ENVIRONMENT`, etc.). System namespaces and `default` are excluded.

## Why it matters

This demonstrates that `generate` isn't limited to security resources like NetworkPolicy/ResourceQuota — it can bootstrap **any** Kubernetes resource a namespace should start with. Real-world uses include seeding a namespace with standard config values, default RBAC RoleBindings, a shared imagePullSecret, or a baseline LimitRange — anything a platform team wants every new namespace to have from day one, without a human running a setup script.

## Rule type

`generate` — creates a `ConfigMap` whenever a `Namespace` is created. `synchronize: true` keeps it self-healing if deleted manually.

## Files

- `policy.yaml` — the ClusterPolicy
- `setup.md` — how to apply the policy
- `demo.md` — how to prove the ConfigMap gets auto-created
