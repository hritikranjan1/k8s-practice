# Lab 8 — Verify Persistent Data from Kubernetes Node

## 1. Objective

Verify that data written by the Pod exists in the HostPath backing the PV.

## 2. Check inside Pod

```bash
kubectl exec nginx-storage -n storage-lab --   cat /usr/share/nginx/html/data.txt
```

## 3. Check the node

For the HostPath lab:

```bash
sudo ls -lah /data/k8s-pv
sudo cat /data/k8s-pv/data.txt
```

Expected:

```text
Persistent Data
```

## 4. What this proves

The path relationship is:

```text
Pod
  |
  | /usr/share/nginx/html
  v
PVC
  |
PV
  |
HostPath
  |
/data/k8s-pv
```

The exact backend is implementation-specific. This direct node check is appropriate for this HostPath lab, but not a universal method for cloud/CSI volumes.

## 5. Important warning

Do not manually edit production volume data from the node while the application is running unless you fully understand the storage/application semantics.

For databases, direct filesystem manipulation can cause corruption.

## 6. Real-world use case

Node-level inspection can help troubleshoot:
- missing files
- disk usage
- HostPath problems
- node-local storage failures

## 7. Interview takeaway

A HostPath PV maps to a directory on a node. A cloud/CSI PV may not have a meaningful user-visible host directory.


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

