# Lab 13 — PVC Larger Than PV — Pending Scenario

## 1. Objective

Intentionally create an incompatible PVC and observe the `Pending` state.

## 2. Scenario

Available PV:

```text
5Gi
RWO
manual
```

Requested PVC:

```text
10Gi
RWO
manual
```

## 3. Create the large PVC

Example:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: large-pvc
  namespace: storage-lab
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: manual
  resources:
    requests:
      storage: 10Gi
```

Apply:

```bash
kubectl apply -f large-pvc.yaml
```

## 4. Observe

```bash
kubectl get pvc -n storage-lab
```

Expected:

```text
large-pvc   Pending
```

Describe:

```bash
kubectl describe pvc large-pvc -n storage-lab
```

## 5. Why it is Pending

Kubernetes cannot satisfy a 10Gi request using a compatible 5Gi PV.

## 6. Pod consequence

A Pod using the Pending PVC will also remain Pending.

During the practice, `large-pod` was observed Pending because its storage claim could not be satisfied.

## 7. Resolution

Options:

### Option A — reduce request

Request 5Gi or less, if that matches the actual requirement.

### Option B — create a larger PV

Create an appropriate PV, for example 10Gi, using a valid backend.

### Option C — use dynamic provisioning

Use a StorageClass whose provisioner can create a sufficiently large volume.

## 8. Real-world use case

This is a common deployment failure when an application team requests more storage than the available static capacity.

## 9. Interview takeaway

A PVC can remain Pending even when the cluster has PVs. The PV must satisfy the claim's requirements.


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

