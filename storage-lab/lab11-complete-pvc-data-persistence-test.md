# Lab 11 — Complete PVC Data Persistence Test

## 1. Objective

Perform the complete end-to-end persistence test rather than checking only one step.

## 2. Test sequence

### Step 1 — Verify PVC

```bash
kubectl get pvc -n storage-lab
```

### Step 2 — Verify Pod

```bash
kubectl get pod -n storage-lab
```

### Step 3 — Write data

```bash
kubectl exec nginx-storage -n storage-lab --   sh -c 'echo "Persistence Test $(date)" > /usr/share/nginx/html/persistence.txt'
```

### Step 4 — Read from Pod

```bash
kubectl exec nginx-storage -n storage-lab --   cat /usr/share/nginx/html/persistence.txt
```

### Step 5 — Read from node

```bash
sudo cat /data/k8s-pv/persistence.txt
```

### Step 6 — Delete Pod

```bash
kubectl delete pod nginx-storage -n storage-lab
```

### Step 7 — Recreate

```bash
kubectl apply -f pod.yaml
```

### Step 8 — Read again

```bash
kubectl exec nginx-storage -n storage-lab --   cat /usr/share/nginx/html/persistence.txt
```

## 3. What the complete test proves

It proves all of these independently:

- PVC successfully bound
- Pod can mount PVC
- Pod can write to volume
- data reaches backend
- Pod deletion does not delete PVC/PV
- new Pod can read old data

## 4. Production interpretation

This is a simplified version of a persistence smoke test. Production tests should additionally verify:
- backups
- restore
- permissions
- failover
- node failure
- application consistency
- performance
- monitoring

## 5. Interview takeaway

Never claim storage is persistent merely because a PVC is `Bound`. Prove it with a write-delete-recreate-read test.


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

