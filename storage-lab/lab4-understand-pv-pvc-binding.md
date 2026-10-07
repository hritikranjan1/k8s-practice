# Lab 4 — Understand PV ↔ PVC Binding

## 1. Objective

Understand exactly how Kubernetes decides whether a PVC can bind to a PV.

## 2. Matching factors

Kubernetes considers compatibility such as:

1. Requested capacity
2. Access modes
3. StorageClass
4. Volume availability
5. Binding/topology rules

Example:

```text
PV:
  5Gi
  RWO
  manual
  Available

PVC:
  2Gi
  RWO
  manual
```

Result:

```text
PV -> Bound
PVC -> Bound
```

## 3. Observe the relationship

```bash
kubectl get pv
kubectl get pvc -n storage-lab
```

More detail:

```bash
kubectl describe pv storage-lab-pv
kubectl describe pvc storage-lab-pvc -n storage-lab
```

The PV shows a claim reference similar to:

```text
Claim: storage-lab/storage-lab-pvc
```

The PVC shows:

```text
Volume: storage-lab-pv
```

## 4. Capacity rule

A 2Gi request can bind to a 5Gi PV.

A 10Gi request cannot bind to a 5Gi PV.

Kubernetes does not combine several unrelated PVs to satisfy one ordinary PVC.

## 5. Access mode rule

A PVC requesting RWX cannot be satisfied by a PV that only provides RWO.

## 6. StorageClass rule

A PVC with:

```yaml
storageClassName: manual
```

normally needs a compatible PV using:

```yaml
storageClassName: manual
```

For static provisioning, `manual` is commonly paired with a manually created PV.

## 7. Why binding can be delayed

A StorageClass can use:

```text
WaitForFirstConsumer
```

This can defer the binding/provisioning decision until a consuming Pod exists.

## 8. Troubleshooting workflow

```bash
kubectl get pvc -n storage-lab
kubectl describe pvc <pvc> -n storage-lab
kubectl get pv
kubectl describe pv <pv>
kubectl get sc
```

## 9. Interview takeaway

PVC binding is not simply “PVC size <= PV size.” StorageClass, access modes, availability, and binding/topology rules also matter.


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

