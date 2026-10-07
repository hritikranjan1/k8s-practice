# Lab 24 — Find Which Pod Is Using a PVC

## 1. Objective

Identify Pods that reference a particular PVC.

## 2. Why this matters

Before deleting or modifying a PVC, determine whether an application is currently using it.

## 3. Basic search

```bash
kubectl get pods -A -o yaml | grep -B5 -A5 'claimName: storage-lab-pvc'
```

This is useful for quick investigation but is not ideal for automation.

## 4. JSON output approach

```bash
kubectl get pods -A -o json
```

Then inspect each Pod's:

```text
spec.volumes[].persistentVolumeClaim.claimName
```

## 5. Namespace-aware approach

If the namespace is known:

```bash
kubectl get pods -n storage-lab -o yaml | grep -B5 -A5 'claimName: storage-lab-pvc'
```

## 6. Check the workload too

A Pod may be controlled by a Deployment:

```bash
kubectl get pod <pod> -n storage-lab -o jsonpath='{.metadata.ownerReferences[*].name}{{"\n"}}'
```

Then:

```bash
kubectl get deployment -n storage-lab
```

## 7. Real-world use case

Before:

```bash
kubectl delete pvc ...
```

you should know which workload depends on it.

## 8. Safety rule

Never delete a production PVC merely because a Pod is not currently running. A stopped workload can still depend on the data.

## 9. Interview takeaway

A PVC is referenced from a Pod's `spec.volumes[].persistentVolumeClaim.claimName`.


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

