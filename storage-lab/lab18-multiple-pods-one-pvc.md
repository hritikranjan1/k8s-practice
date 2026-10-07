# Lab 18 — Multiple Pods Using One PVC

## 1. Objective

Mount one PVC into multiple Pods and understand the effect of the access mode and node placement.

## 2. Lab setup

Namespace:

```text
storage-lab
```

PVC:

```text
storage-lab-pvc
```

Pods:

```text
nginx-1
nginx-2
```

Both mount the same PVC.

## 3. Verify

```bash
kubectl get pods -n storage-lab -o wide
kubectl get pvc -n storage-lab
```

Both Pods were running on the same node in the single-node cluster.

## 4. Shared data test

Write from Pod 1:

```bash
kubectl exec nginx-1 -n storage-lab --   sh -c 'echo "Hello from nginx-1" > /data/test.txt'
```

Read from Pod 2:

```bash
kubectl exec nginx-2 -n storage-lab --   cat /data/test.txt
```

Append from Pod 2:

```bash
kubectl exec nginx-2 -n storage-lab --   sh -c 'echo "Hello from nginx-2" >> /data/test.txt'
```

Read from Pod 1:

```bash
kubectl exec nginx-1 -n storage-lab --   cat /data/test.txt
```

## 5. Important RWO lesson

RWO means:

```text
ReadWriteOnce = volume mounted read-write by one node
```

It does **not** strictly mean:

```text
only one Pod can ever mount it
```

Multiple Pods on the same node can use the same RWO volume.

## 6. Multi-node warning

On a multi-node cluster, a typical RWO backend cannot provide simultaneous read-write attachment to multiple nodes.

## 7. Application safety

Even when Kubernetes permits both Pods to mount the volume, that does not guarantee that the application can safely write the same file concurrently.

## 8. Real-world use case

Shared storage between replicas usually requires a backend and access mode designed for it, often RWX for multi-node shared writes.

## 9. Interview takeaway

RWO is node-level attachment semantics, not simply Pod-count semantics.


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

