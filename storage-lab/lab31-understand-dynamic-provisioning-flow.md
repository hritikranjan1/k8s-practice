# Lab 31 — Understand Dynamic Provisioning Flow

## 1. Objective

Understand the complete lifecycle behind dynamic provisioning.

## 2. Static flow

```text
Administrator
     |
     v
    PV
     |
     v
    PVC
     |
     v
    Pod
```

The administrator manually creates the PV.

## 3. Dynamic flow

```text
Developer
   |
   v
PVC
   |
   v
StorageClass
   |
   v
Provisioner / CSI Driver
   |
   v
Physical / virtual storage
   |
   v
Automatically created PV
   |
   v
PVC Bound
   |
   v
Pod
```

## 4. What happened in the lab

The PVC requested:

```text
1Gi
RWO
local-path
```

The `local-path` StorageClass used:

```text
rancher.io/local-path
```

The provisioner created a PV automatically.

## 5. WaitForFirstConsumer

The StorageClass used:

```text
volumeBindingMode: WaitForFirstConsumer
```

This can delay binding/provisioning until Kubernetes knows about the workload consuming the volume. This is especially useful for topology-aware storage.

## 6. Important distinction

This:

```text
WaitForFirstConsumer
```

does not mean:

```text
dynamic provisioning
```

Dynamic provisioning comes from the provisioner.

Example:

```text
kubernetes.io/no-provisioner
```

means no dynamic provisioning.

## 7. Reclaim policy

Dynamic StorageClasses often use:

```text
Delete
```

for disposable environments.

Production storage may use a policy appropriate for data protection.

## 8. Real-world use case

A developer creates:

```yaml
resources:
  requests:
    storage: 100Gi
```

The developer does not manually create a cloud disk. Kubernetes asks the CSI provisioner to create it.

## 9. Interview takeaway

Know all three components:

```text
PVC = what application requests
StorageClass = how storage should be provisioned
Provisioner/CSI = component that actually performs provisioning
```


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

