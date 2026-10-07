# Lab 14 — Troubleshoot Pending PVC

## 1. Objective

Develop a repeatable troubleshooting process for a PVC stuck in `Pending`.

## 2. First command

```bash
kubectl get pvc -n storage-lab
```

Then:

```bash
kubectl describe pvc <pvc-name> -n storage-lab
```

The Events section is often the most useful part.

## 3. Check PVs

```bash
kubectl get pv
kubectl get pv -o wide
```

Inspect candidates:

```bash
kubectl describe pv <pv-name>
```

## 4. Check StorageClass

```bash
kubectl get sc
kubectl get sc <storage-class> -o yaml
```

## 5. Check access modes

```bash
kubectl get pv
kubectl get pvc -n storage-lab
```

Compare:

```text
PV: RWO
PVC: RWO
```

or:

```text
PV: RWO
PVC: RWX
```

The second is incompatible.

## 6. Check capacity

Example failure:

```text
PV = 5Gi
PVC = 10Gi
```

No match.

## 7. Check StorageClass

Example:

```text
PV StorageClass = manual
PVC StorageClass = local-path
```

A static PV may not satisfy the claim.

## 8. Check WaitForFirstConsumer

If the StorageClass uses:

```text
WaitForFirstConsumer
```

the PVC may wait for a Pod before binding/provisioning decisions complete.

This is normal in many topology-aware scenarios.

## 9. Check events

```bash
kubectl get events -n storage-lab --sort-by=.lastTimestamp
```

## 10. Practical troubleshooting checklist

```bash
kubectl get pvc -n storage-lab
kubectl describe pvc <pvc> -n storage-lab
kubectl get pv
kubectl get sc
kubectl get pods -n storage-lab
kubectl describe pod <pod> -n storage-lab
kubectl get events -n storage-lab --sort-by=.lastTimestamp
```

## 11. Interview takeaway

When a PVC is Pending, do not guess. Start with `kubectl describe pvc` and inspect Events, then compare PVC requirements against PV and StorageClass.


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

