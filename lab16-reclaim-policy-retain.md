# Lab 16 — Reclaim Policy: Retain

## 1. Objective

Understand how `Retain` protects persistent storage from automatic deletion after a PVC is deleted.

## 2. PV configuration

Example:

```yaml
persistentVolumeReclaimPolicy: Retain
```

Check:

```bash
kubectl get pv
kubectl describe pv storage-lab-pv
```

## 3. Test

First verify data:

```bash
sudo cat /data/k8s-pv/test.txt
```

Delete the claim:

```bash
kubectl delete pvc storage-lab-pvc -n storage-lab
```

Check:

```bash
kubectl get pv
```

The PV can move to:

```text
Released
```

## 4. What happened?

The claim was deleted, but Kubernetes did not automatically remove the retained storage data.

Check:

```bash
sudo ls -lah /data/k8s-pv
sudo cat /data/k8s-pv/test.txt
```

## 5. Why Retain is useful

Use Retain when data is valuable and an administrator should decide what happens next.

Examples:
- databases
- important application data
- audit records
- customer uploads
- production persistent data

## 6. Important caveat

A `Released` PV is not automatically ready for another claim. Manual cleanup/recovery may be required.

## 7. Interview takeaway

Retain separates deletion of the claim from deletion of the underlying storage. It is useful for data protection and manual recovery.


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

