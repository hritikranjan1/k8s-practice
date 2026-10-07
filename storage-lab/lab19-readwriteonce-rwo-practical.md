# Lab 19 — ReadWriteOnce (RWO) Practical

## 1. Objective

Understand exactly what RWO means and test it in a Kubernetes environment.

## 2. RWO definition

```text
ReadWriteOnce (RWO)
```

means the volume can be mounted read-write by a single node at a time.

## 3. Verify access mode

```bash
kubectl get pv
kubectl get pvc -n storage-lab
```

You should see:

```text
RWO
```

## 4. Same-node behavior

On this single-node RKE2 cluster, multiple Pods can mount the same RWO PVC because they are all on `server-1`.

Check:

```bash
kubectl get pods -n storage-lab -o wide
```

## 5. Different-node behavior

On a multi-node cluster, attempt to place workloads on different nodes only with an appropriate isolated backend/test environment.

Do not assume HostPath can be shared between nodes.

## 6. RWO vs RWX

| Mode | Meaning |
|---|---|
| RWO | Read-write by one node |
| ROX | Read-only by multiple nodes |
| RWX | Read-write by multiple nodes |

Actual support depends on the storage backend/CSI driver.

## 7. Real-world use case

RWO is common for:
- single-instance databases
- application state
- block storage volumes
- single-node workloads

## 8. Interview trap

Question:

> Does RWO mean only one Pod can use the volume?

Answer:

> No. RWO means read-write attachment from one node. Multiple Pods on that same node may use the volume.


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

