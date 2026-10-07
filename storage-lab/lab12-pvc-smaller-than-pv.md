# Lab 12 — PVC Smaller Than PV

## 1. Objective

Understand why a smaller PVC request can bind to a larger compatible PV.

## 2. Example

PV:

```text
5Gi
RWO
manual
```

PVC:

```text
2Gi
RWO
manual
```

This is compatible.

## 3. Check

```bash
kubectl get pv
kubectl get pvc -n storage-lab
```

## 4. Key point

A PVC requesting 2Gi does not mean Kubernetes must find a PV exactly equal to 2Gi. A 5Gi PV can satisfy the request if other matching conditions are satisfied.

## 5. What happens to unused capacity?

The remaining capacity is still part of the PV. It is not automatically turned into another PVC.

For example:

```text
PV = 5Gi
PVC = 2Gi
Remaining physical capacity = potentially 3Gi
```

But that does not mean another PVC can automatically use the remaining portion of that same PV.

## 6. Real-world use case

An administrator may have a 500Gi volume but an application initially needs only 100Gi.

Dynamic storage systems may provision a volume according to the request instead of manually reusing a larger PV.

## 7. Interview takeaway

PVC capacity is a minimum request, not necessarily an exact physical partition of a PV.


# Environment Used

These labs were performed as Kubernetes storage practice on an RKE2 cluster.

- Kubernetes: RKE2
- Node used in the lab environment: `server-1`
- Kubernetes version observed: `v1.35.6+rke2r1`
- Primary practice namespace: `storage-lab`
- Additional isolated namespaces used for specific scenarios:
  - `dynamic-storage-lab`
  - `pvc-expansion-lab`
- Primary static StorageClass: `manual`
- Dynamic StorageClass: `local-path`
- Expansion lab StorageClass: `pvc-expansion`
- Local-path provisioner: `rancher.io/local-path`

> **Safety:** Production-like `jarvis-*` PVs/PVCs were not used for destructive experiments. Labs were isolated in dedicated namespaces/resources.

## Useful aliases

```bash
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgpa='kubectl get pods -A'
alias cgp='kubectl get pods -o wide'
alias kgn='kubectl get nodes'
alias kgs='kubectl get svc'
alias kgpv='kubectl get pv'
alias kgpvc='kubectl get pvc'
alias kgns='kubectl get namespaces'
alias kga='kubectl get all'
```

Use `kubectl` or the aliases directly. Do not use `sudo cgp`; Bash aliases are not expanded after `sudo`.

