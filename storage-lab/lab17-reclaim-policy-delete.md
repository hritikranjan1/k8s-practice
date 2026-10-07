# Lab 17 — Reclaim Policy: Delete

## 1. Objective

Understand the `Delete` reclaim policy and why it is commonly used with dynamically provisioned temporary storage.

## 2. Concept

With:

```yaml
persistentVolumeReclaimPolicy: Delete
```

the storage resource may be deleted when its PVC is deleted, depending on the provisioner/backend.

## 3. Important safety rule

Use only an isolated disposable lab.

Do **not** test destructive reclaim behavior on production-like `jarvis-*` resources.

## 4. Verify reclaim policy

```bash
kubectl get pv
kubectl describe pv <pv-name>
```

## 5. Delete test claim

```bash
kubectl delete pvc <test-pvc> -n <test-namespace>
```

Then:

```bash
kubectl get pv
```

With supported dynamic provisioning, the dynamically created PV and backing storage can be cleaned up according to the provisioner's behavior.

## 6. Retain vs Delete

| Policy | Typical behavior |
|---|---|
| Retain | Keep volume for manual recovery |
| Delete | Remove dynamically managed storage when claim is deleted |

## 7. Real-world use case

`Delete` is convenient for:
- temporary CI environments
- development namespaces
- disposable test databases
- dynamically provisioned application volumes

## 8. Interview takeaway

Reclaim policy determines what Kubernetes should do with the PV/backend after the claim is released. Always understand the backend's actual deletion behavior.


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

