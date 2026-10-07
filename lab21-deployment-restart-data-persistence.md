# Lab 21 — Deployment Restart and Data Persistence

## 1. Objective

Prove that restarting a Deployment creates a new Pod while persistent data remains.

## 2. Write data

Find the Pod:

```bash
kubectl get pods -n storage-lab -l app=nginx-storage
```

Write:

```bash
kubectl exec <pod-name> -n storage-lab --   sh -c 'echo "Persistent Data" > /usr/share/nginx/html/data.txt'
```

Verify:

```bash
kubectl exec <pod-name> -n storage-lab --   cat /usr/share/nginx/html/data.txt
```

## 3. Restart Deployment

```bash
kubectl rollout restart deployment nginx-storage -n storage-lab
```

Watch:

```bash
kubectl get pods -n storage-lab -w
```

## 4. Verify new Pod

```bash
kubectl get pods -n storage-lab -l app=nginx-storage
```

Then:

```bash
kubectl exec <new-pod-name> -n storage-lab --   cat /usr/share/nginx/html/data.txt
```

Expected:

```text
Persistent Data
```

## 5. What this proves

Deployment replaced the Pod.

PVC remained.

PV remained.

The data remained.

## 6. Core principle

```text
Deployment lifecycle
       !=
Pod lifecycle
       !=
PVC lifecycle
       !=
PV lifecycle
```

## 7. Real-world use case

This is important during:
- rolling deployments
- image updates
- configuration changes
- Pod crashes
- node rescheduling

## 8. Interview takeaway

A Pod restart/replacement does not inherently delete persistent volume data.


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

