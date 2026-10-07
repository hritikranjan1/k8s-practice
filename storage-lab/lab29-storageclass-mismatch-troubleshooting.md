# Lab 29 — StorageClass Mismatch Troubleshooting

## 1. Objective

Diagnose a PVC that cannot use the intended PV because of StorageClass differences.

## 2. Inspect all StorageClasses

```bash
kubectl get sc
kubectl get sc -o wide
```

## 3. Inspect PV

```bash
kubectl get pv
kubectl describe pv <pv-name>
```

## 4. Inspect PVC

```bash
kubectl describe pvc <pvc-name> -n <namespace>
```

Compare:

```text
PV StorageClass
PVC StorageClass
```

## 5. Understand this environment

### `manual`

```text
provisioner: kubernetes.io/no-provisioner
```

Used for manually created PVs.

### `local-path`

```text
provisioner: rancher.io/local-path
```

Used for dynamic local-path provisioning.

### `pvc-expansion`

```text
provisioner: rancher.io/local-path
allowVolumeExpansion: true
```

Created specifically for the expansion lab.

## 6. Common mistake

Using:

```yaml
storageClassName: manual
```

while expecting Kubernetes to dynamically create a PV.

That will not happen because `manual` has no dynamic provisioner.

## 7. Resolution

Decide:

```text
Static storage?
    -> matching manually created PV

Dynamic storage?
    -> appropriate dynamic StorageClass
```

## 8. Interview takeaway

Always know the provisioner behind a StorageClass. The StorageClass name alone does not tell the whole story.


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

