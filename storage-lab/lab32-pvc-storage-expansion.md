# Lab 32 — PVC Storage Expansion

## 1. Objective

Test PVC expansion and understand why `allowVolumeExpansion: true` does not guarantee that the backend can actually expand storage.

## 2. Dedicated StorageClass

A dedicated lab StorageClass was created:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: pvc-expansion
provisioner: rancher.io/local-path
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

## 3. Initial PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: expansion-pvc
  namespace: pvc-expansion-lab
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: pvc-expansion
  resources:
    requests:
      storage: 1Gi
```

The PVC initially requested 1Gi.

## 4. Pod

The Pod mounted:

```text
expansion-pvc
```

at:

```text
/data
```

## 5. Write important data

```bash
kubectl exec -n pvc-expansion-lab expansion-pod --   sh -c 'echo "Important persistent data" > /data/test.txt'
```

Verify:

```bash
kubectl exec -n pvc-expansion-lab expansion-pod --   cat /data/test.txt
```

## 6. Request expansion

Edit:

```bash
kubectl edit pvc expansion-pvc -n pvc-expansion-lab
```

Change:

```text
1Gi
```

to:

```text
2Gi
```

Or:

```bash
kubectl patch pvc expansion-pvc   -n pvc-expansion-lab   -p '{"spec":{"resources":{"requests":{"storage":"2Gi"}}}}'
```

In the actual lab, the patch later returned:

```text
patched (no change)
```

because the PVC request had already been changed to 2Gi.

## 7. Important observation

There were three different values to compare:

### PVC requested size

```bash
kubectl get pvc expansion-pvc -n pvc-expansion-lab   -o jsonpath='{.spec.resources.requests.storage}{{"\n"}}'
```

Result:

```text
2Gi
```

### PV capacity

```bash
kubectl get pv
```

The PV remained:

```text
1Gi
```

### Filesystem size

```bash
kubectl exec -it expansion-pod -n pvc-expansion-lab -- df -h /data
```

The filesystem did not become a real 2Gi volume.

## 8. Why expansion failed

The StorageClass correctly said:

```text
allowVolumeExpansion: true
```

However, the cluster had:

```bash
kubectl get csidrivers
```

Result:

```text
No resources found
```

Also:

```bash
kubectl get pods -A | grep -i csi
```

returned no CSI Pods.

The provisioner was:

```text
rancher.io/local-path
```

and the local-path provisioner was running, but this environment did not have an external CSI expansion controller capable of performing the requested volume expansion.

## 9. Critical concept

`allowVolumeExpansion: true` means:

> Kubernetes permits PVC expansion requests for this StorageClass.

It does **not** mean:

> The storage backend is guaranteed to be able to expand.

Actual expansion requires support from the storage implementation/CSI driver and, where applicable, filesystem expansion.

## 10. Troubleshooting result

The PVC ended in a state conceptually like:

```text
PVC requested: 2Gi
PV capacity:   1Gi
Filesystem:    1Gi
```

The PVC events indicated that it was waiting for an external controller to expand the claim.

## 11. Correct resolution

Do not keep editing/patching the PVC once the request is already 2Gi.

For a real successful expansion lab, use a CSI-backed storage system that supports expansion, such as an appropriate cloud block-storage CSI driver, Ceph CSI, or enterprise CSI platform.

Do not install a CSI driver blindly into a production cluster just for a lab.

## 12. Real-world use case

PVC expansion is useful when:

```text
Application starts with 100Gi
        ↓
Data grows
        ↓
Need 200Gi
        ↓
Expand volume without rebuilding application storage
```

Common examples:
- databases
- log storage
- media platforms
- file repositories

## 13. Three-layer troubleshooting model

When expansion fails, inspect:

```text
PVC requested size
        ↓
PV/backend capacity
        ↓
Filesystem visible to application
```

All three must eventually reflect the expanded capacity.

## 14. Interview questions

### Does `allowVolumeExpansion: true` guarantee expansion?

No.

### Why can PVC request show 2Gi while PV remains 1Gi?

Because Kubernetes accepted the desired request, but the backend/controller has not successfully performed the physical/storage expansion.

### Why is CSI important?

CSI provides the standardized interface through which Kubernetes communicates with external storage systems.

## 15. Lab conclusion

This was intentionally valuable as a troubleshooting lab because the failure demonstrated an important production lesson:

```text
Kubernetes API capability
        !=
Storage backend capability
```


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

