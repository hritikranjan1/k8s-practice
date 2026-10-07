# Lab 27 — PVC Capacity Mismatch Troubleshooting

## 1. Objective

Diagnose a PVC that requests more storage than available static capacity.

## 2. Example

PV:

```text
5Gi
```

PVC:

```text
10Gi
```

## 3. Inspect

```bash
kubectl get pv
kubectl get pvc -n storage-lab
kubectl describe pvc large-pvc -n storage-lab
```

## 4. Root cause

The claim needs at least 10Gi, but the available compatible PV provides only 5Gi.

## 5. Resolution options

### Reduce the claim

For a disposable Pending PVC, recreate it with a smaller request.

### Increase available storage

Create a compatible larger PV.

### Use dynamic provisioning

Select a StorageClass whose provisioner can create a volume of the requested size.

## 6. Important PVC immutability lesson

Do not assume you can freely shrink a PVC request after creation. PVC storage requests have strict rules, and shrinking persistent storage is generally not supported as a simple edit.

## 7. Real-world use case

A Helm chart might default to:

```yaml
storage: 100Gi
```

while the on-prem environment has only small static volumes.

## 8. Interview takeaway

Capacity is one of the first compatibility checks when diagnosing a Pending PVC.


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

