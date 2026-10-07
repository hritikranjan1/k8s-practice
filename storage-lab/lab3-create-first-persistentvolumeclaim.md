# Lab 3 — Create Your First PersistentVolumeClaim (PVC)

## 1. Objective

Create a PVC that requests a portion of the storage exposed by a PV.

## 2. What is a PVC?

A PersistentVolumeClaim is a request for storage by a user/application.

A PVC can specify:
- requested capacity
- access mode
- StorageClass

The Kubernetes control plane finds a compatible PV or dynamically provisions one.

## 3. Example PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: storage-lab-pvc
  namespace: storage-lab
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: manual
  resources:
    requests:
      storage: 2Gi
```

Save as:

```text
pvc.yaml
```

Apply:

```bash
kubectl apply -f pvc.yaml
```

## 4. Verify

```bash
kubectl get pvc -n storage-lab
kubectl describe pvc storage-lab-pvc -n storage-lab
kubectl get pv
```

Expected:

```text
PVC STATUS: Bound
PV STATUS: Bound
```

The PVC requested 2Gi while the PV provided 5Gi. The claim does not need to request the full PV capacity.

## 5. Important concept

The basic relationship is:

```text
Application
    |
   Pod
    |
   PVC
    |
   PV
    |
Storage backend
```

The application normally references the PVC, not the PV.

## 6. Common problems

### PVC stays Pending

Check:

```bash
kubectl describe pvc storage-lab-pvc -n storage-lab
kubectl get pv
kubectl get sc
```

Look for:
- capacity mismatch
- access mode mismatch
- StorageClass mismatch
- PV already Bound
- no suitable PV
- topology/binding issues

## 7. Real-world use case

A development team may request:

```text
storage: 20Gi
accessMode: ReadWriteOnce
storageClass: fast-ssd
```

without knowing which physical disk or cloud volume will satisfy it.

## 8. Interview takeaway

PVC is namespaced. PV is cluster-scoped. Pods and PVCs must be in the same namespace.



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

