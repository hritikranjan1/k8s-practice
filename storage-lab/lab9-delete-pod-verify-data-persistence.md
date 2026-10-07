# Lab 9 — Delete Pod and Verify Data Persistence

## 1. Objective

Prove that deleting a Pod does not delete data stored in the PVC/PV.

## 2. Confirm data

```bash
kubectl exec nginx-storage -n storage-lab --   cat /usr/share/nginx/html/data.txt
```

## 3. Delete the Pod

```bash
kubectl delete pod nginx-storage -n storage-lab
```

Verify:

```bash
kubectl get pods -n storage-lab
kubectl get pvc -n storage-lab
kubectl get pv
```

## 4. Important observation

The Pod disappears, but the PVC and PV remain.

If the Pod was a standalone Pod, it will not automatically return unless you recreate it. A Deployment would recreate its Pod.

## 5. Verify underlying data

```bash
sudo cat /data/k8s-pv/data.txt
```

Expected data remains.

## 6. Core concept

```text
Pod lifecycle != PVC lifecycle != PV lifecycle
```

Deleting a Pod normally does not delete its PVC.

## 7. Real-world use case

When a Deployment performs a rollout, Kubernetes may terminate old Pods and create new Pods. Persistent application data should remain available through the PVC.

## 8. Interview takeaway

Pods are ephemeral compute objects. Persistent storage is designed to have an independent lifecycle.


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

