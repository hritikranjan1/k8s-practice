# Lab 30 — Dynamic Provisioning with StorageClass

## 1. Objective

Create a PVC that causes Kubernetes to dynamically create a PV.

## 2. Static vs dynamic

### Static

```text
Admin creates PV
       ↓
PVC binds to PV
```

### Dynamic

```text
PVC
 ↓
StorageClass
 ↓
Provisioner
 ↓
PV automatically created
```

## 3. Initial issue encountered

The initial PVC used:

```yaml
storageClassName: manual
```

But `manual` uses:

```text
kubernetes.io/no-provisioner
```

Therefore Kubernetes could not dynamically create storage.

The PVC remained Pending.

## 4. Troubleshooting

```bash
kubectl get storageclass
kubectl get sc -o wide
kubectl get storageclass manual -o yaml
kubectl describe pvc dynamic-pvc -n dynamic-storage-lab
kubectl describe pod dynamic-pod -n dynamic-storage-lab
```

The Pod event indicated that no available PV could satisfy the claim.

## 5. Install local-path provisioner

In the isolated lab environment:

```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

Verify:

```bash
kubectl get sc
kubectl get pods -A | grep local-path
```

## 6. Correct PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
  namespace: dynamic-storage-lab
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: local-path
  resources:
    requests:
      storage: 1Gi
```

## 7. Important issue: PVC StorageClass immutability

The existing Pending PVC was changed from `manual` to `local-path`.

Kubernetes rejected the update because PVC specification fields are largely immutable after creation.

### Lab resolution

Because the claim was an isolated Pending lab:

```bash
kubectl delete pod dynamic-pod -n dynamic-storage-lab
kubectl delete pvc dynamic-pvc -n dynamic-storage-lab
```

Then recreate the PVC using `local-path`.

## 8. Successful result

A new PV was automatically created with a name similar to:

```text
pvc-<uuid>
```

The result looked conceptually like:

```text
PVC dynamic-pvc -> Bound
PV pvc-<uuid>   -> Bound
```

## 9. Verify

```bash
kubectl get pvc -n dynamic-storage-lab
kubectl get pv
kubectl describe pvc dynamic-pvc -n dynamic-storage-lab
```

## 10. Real-world use case

Dynamic provisioning is standard for cloud and enterprise Kubernetes storage:
- AWS EBS
- Azure Disk
- Google Persistent Disk
- Ceph
- enterprise SAN/NAS CSI drivers

## 11. Interview takeaway

A dynamic PVC does not magically create storage. A StorageClass references a provisioner/CSI implementation that performs the provisioning.


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

