# Lab 22 — Scale Deployment with PVC

## 1. Objective

Scale a Deployment from one Pod to two and understand RWO behavior.

## 2. Scale

```bash
kubectl scale deployment nginx-storage -n storage-lab --replicas=2
```

Verify:

```bash
kubectl get pods -n storage-lab -l app=nginx-storage -o wide
```

## 3. What happened in this cluster?

The cluster has one node:

```text
server-1
```

Both replicas were scheduled on that node.

Therefore both could mount the RWO PVC.

## 4. Shared data test

Get Pod names:

```bash
POD1=$(kubectl get pods -n storage-lab -l app=nginx-storage -o jsonpath='{.items[0].metadata.name}')
POD2=$(kubectl get pods -n storage-lab -l app=nginx-storage -o jsonpath='{.items[1].metadata.name}')
```

Read from both:

```bash
kubectl exec "$POD1" -n storage-lab -- cat /usr/share/nginx/html/data.txt
kubectl exec "$POD2" -n storage-lab -- cat /usr/share/nginx/html/data.txt
```

Write from Pod 1:

```bash
kubectl exec "$POD1" -n storage-lab --   sh -c 'echo "Written by Pod 1" >> /usr/share/nginx/html/data.txt'
```

Read from Pod 2:

```bash
kubectl exec "$POD2" -n storage-lab --   cat /usr/share/nginx/html/data.txt
```

## 5. Important lesson

Scaling replicas does not automatically mean shared storage is safe.

There are two separate questions:

1. Can the volume be mounted?
2. Can the application safely share the data?

## 6. Multi-node limitation

If replicas land on different nodes, a typical RWO backend cannot be attached read-write to both nodes.

For genuinely shared multi-node file access, use a backend supporting RWX when appropriate.

## 7. Real-world use case

Stateless applications scale easily. Stateful applications require deliberate storage architecture.

## 8. Interview takeaway

Scaling a Deployment with a single RWO PVC is not automatically a valid production architecture for a multi-node stateful application.


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

