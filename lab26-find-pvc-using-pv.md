# Lab 10 — Recreate Pod and Verify Persistent Data

## 1. Objective

Recreate a Pod that uses the same PVC and prove the old data is still available.

## 2. Recreate

Apply the Pod manifest again:

```bash
kubectl apply -f pod.yaml
```

Check:

```bash
kubectl get pods -n storage-lab
```

## 3. Verify data

```bash
kubectl exec nginx-storage -n storage-lab --   cat /usr/share/nginx/html/data.txt
```

Expected:

```text
Persistent Data
```

## 4. Why data survived

The sequence was:

```text
Pod A
  |
  PVC
  |
  PV
  |
  Data

Pod A deleted
  |
PVC/PV remain
  |
Pod B starts
  |
same PVC
  |
same data
```

## 5. Real-world use case

This is exactly the principle needed when:
- a container crashes
- a Pod is rescheduled
- a Deployment rolls out
- a node is replaced (depending on storage backend)
- an application is restarted

## 6. Important caveat

Persistence does not automatically mean high availability. HostPath is node-local. If the node itself is lost, another node cannot necessarily access that same directory.

## 7. Interview takeaway

Persistence and availability are different concepts.


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

