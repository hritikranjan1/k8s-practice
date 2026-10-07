# Lab 28 — Access Mode Mismatch Troubleshooting

## 1. Objective

Understand and troubleshoot incompatible access modes.

## 2. Example

PV:

```text
RWO
```

PVC:

```text
RWX
```

This is not a compatible match.

## 3. Inspect

```bash
kubectl get pv
kubectl get pvc -n storage-lab
kubectl describe pvc <pvc> -n storage-lab
```

## 4. Access modes

### RWO

```text
ReadWriteOnce
```

Read-write from one node.

### ROX

```text
ReadOnlyMany
```

Read-only from multiple nodes.

### RWX

```text
ReadWriteMany
```

Read-write from multiple nodes.

Support depends on the backend.

## 5. Resolution

Choose an access mode supported by the storage backend.

Do not simply change the YAML and assume the backend can provide RWX.

## 6. Real-world use case

If ten application replicas need shared read-write files across multiple nodes, an RWO block volume is usually the wrong storage architecture.

## 7. Interview takeaway

Access mode is a storage capability requirement, not merely a Pod setting.


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

