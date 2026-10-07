# Lab 15 — PVC with Wrong StorageClass

## 1. Objective

Understand how a StorageClass mismatch can prevent a static PVC from binding.

## 2. Scenario

Suppose:

```text
PV StorageClass = manual
PVC StorageClass = local-path
```

If the PVC is intended to use the manually created PV, the requirements do not match.

## 3. Inspect

```bash
kubectl get pv
kubectl get pvc -n storage-lab
kubectl get sc
```

Detailed:

```bash
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name> -n storage-lab
```

## 4. Why this happens

StorageClass is part of the PV/PVC matching model.

`manual` and `local-path` represent different provisioning models in this environment:

```text
manual
  -> no-provisioner
  -> static PVs

local-path
  -> rancher.io/local-path
  -> dynamic provisioning
```

## 5. Resolution

Choose the correct model.

For a manually created PV:

```yaml
storageClassName: manual
```

For dynamic provisioning:

```yaml
storageClassName: local-path
```

## 6. Important immutable-field lesson

A PVC's `storageClassName` cannot simply be changed after creation.

During the dynamic provisioning lab, changing an existing Pending PVC from `manual` to `local-path` produced an immutability error.

For an isolated Pending lab, the safe practice resolution was:

```bash
kubectl delete pod <consumer-pod> -n <namespace>
kubectl delete pvc <pvc-name> -n <namespace>
```

Then recreate the PVC with the correct StorageClass.

> Never delete a production PVC just to change its configuration. Investigate data and workload impact first.

## 7. Real-world use case

A deployment may fail after a Helm value or environment change accidentally points to the wrong StorageClass.

## 8. Interview takeaway

Static and dynamic provisioning are different workflows. Know which StorageClass and provisioner your cluster actually provides.


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

