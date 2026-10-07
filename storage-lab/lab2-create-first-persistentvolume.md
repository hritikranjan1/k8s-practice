# Lab 2 — Create Your First PersistentVolume (PV)

## 1. Objective

Create a manually provisioned PersistentVolume using a local HostPath.

## 2. What is a PV?

A PersistentVolume is a cluster-scoped storage resource made available to workloads.

A PV describes:
- capacity
- access modes
- reclaim policy
- storage class
- storage backend

The Pod normally does not consume the PV directly. It consumes a PVC.

## 3. Real-world use case

Static PVs are useful in:
- small on-premise clusters
- lab environments
- pre-existing disks
- storage manually managed by administrators
- environments without a CSI provisioner

## 4. Prepare the node directory

For this lab:

```bash
sudo mkdir -p /data/k8s-pv
sudo chmod 777 /data/k8s-pv
```

> `chmod 777` is acceptable only for a disposable lab. Production should use controlled ownership and permissions.

## 5. Create PV manifest

Example:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: storage-lab-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /data/k8s-pv
```

Save as:

```text
pv.yaml
```

Apply:

```bash
kubectl apply -f pv.yaml
```

## 6. Verify

```bash
kubectl get pv
kubectl describe pv storage-lab-pv
```

Expected important state before a matching PVC:

```text
STATUS: Available
CAPACITY: 5Gi
ACCESS MODES: RWO
RECLAIM POLICY: Retain
STORAGECLASS: manual
```

## 7. Important concepts

### PV is cluster-scoped

You do not specify a namespace for a PV.

```bash
kubectl get pv
```

### HostPath

The PV points to a directory on the Kubernetes node:

```text
/data/k8s-pv
```

HostPath is node-local and is not equivalent to shared network storage.

## 8. Issue encountered: PV source is immutable

During the practice, the HostPath was changed after the PV already existed.

For example, an existing PV pointed to:

```text
/data/k8s-pv
```

and the manifest was changed to another path.

Kubernetes rejected the update because PV source fields are immutable.

### Why?

Changing the backend of an existing PV could silently point a bound claim to different physical data.

### Lab resolution

Because this was an isolated practice resource, recreate it:

```bash
kubectl delete pvc storage-lab-pvc -n storage-lab
kubectl delete pv storage-lab-pv
```

Prepare the desired directory and recreate the PV.

> Never casually delete a production PV. First identify ownership, data, backups, reclaim policy, and application impact.

## 9. Verification checklist

```bash
kubectl get pv storage-lab-pv
kubectl describe pv storage-lab-pv
sudo ls -la /data/k8s-pv
```

## 10. Interview takeaway

PV is cluster-scoped; PVC is namespaced. A PV represents available storage, while a PVC represents a workload's request for storage.



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

