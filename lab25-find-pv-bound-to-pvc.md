# Lab 25 — Find Which PV Is Bound to a PVC

## 1. Objective

Find the PV backing a specific PVC.

## 2. Easy method

```bash
kubectl get pvc storage-lab-pvc -n storage-lab
```

Look at the `VOLUME` column.

Example:

```text
storage-lab-pvc   Bound   storage-lab-pv
```

## 3. JSONPath

```bash
kubectl get pvc storage-lab-pvc -n storage-lab   -o jsonpath='{.spec.volumeName}{{"\n"}}'
```

## 4. Inspect PV

```bash
kubectl describe pv storage-lab-pv
```

## 5. Why this matters

The PVC is the application's storage request. The PV tells you which storage resource satisfied that request.

## 6. Real-world use case

During an incident:

```text
Application -> PVC -> Which actual volume?
```

This command gives the answer quickly.

## 7. Interview takeaway

The PVC's `spec.volumeName` identifies its bound PV.


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

