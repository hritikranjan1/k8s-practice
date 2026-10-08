# LAB 39 — PVC Bound but Pod Pending

## Objective
Prove that a successfully bound PVC does not guarantee that a Pod can be scheduled.

## Scenario
```text
PV  -> Bound
PVC -> Bound
Pod -> Pending
```
The Pod has an intentionally invalid node selector.

## 1. PV
`lab39-pv.yaml`:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: lab39-pv
spec:
  capacity:
    storage: 2Gi
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: lab39-storage
  hostPath:
    path: /data/lab39
    type: DirectoryOrCreate
```
Apply:
```bash
kubectl apply -f lab39-pv.yaml
```

## 2. PVC
`lab39-pvc.yaml`:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: lab39-pvc
  namespace: troubleshooting-lab
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: lab39-storage
  resources:
    requests:
      storage: 1Gi
```
Apply:
```bash
kubectl apply -f lab39-pvc.yaml
```

## 3. Intentionally broken Pod
`lab39-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: lab39-pod
  namespace: troubleshooting-lab
spec:
  nodeSelector:
    kubernetes.io/hostname: nonexistent-node
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - name: storage
          mountPath: /data
  volumes:
    - name: storage
      persistentVolumeClaim:
        claimName: lab39-pvc
```
Apply:
```bash
kubectl apply -f lab39-pod.yaml
```

## 4. Investigation
```bash
kubectl get pv lab39-pv
kubectl get pvc lab39-pvc -n troubleshooting-lab
kubectl get pod lab39-pod -n troubleshooting-lab
kubectl describe pod lab39-pod -n troubleshooting-lab
kubectl get events -n troubleshooting-lab
kubectl get nodes -o wide
kubectl get nodes --show-labels
```

## Root cause
The cluster has no node with:

```text
kubernetes.io/hostname=nonexistent-node
```

Therefore the scheduler cannot place the Pod. The storage is already successfully bound.

## Fix
Remove the invalid `nodeSelector` from the YAML and recreate the Pod:

```bash
kubectl delete pod lab39-pod -n troubleshooting-lab
kubectl apply -f lab39-pod.yaml
kubectl get pod lab39-pod -n troubleshooting-lab
```

## Troubleshooting lesson
When a Pod is Pending, do not immediately blame storage. Inspect the scheduler Events.

Possible causes include:
- nodeSelector mismatch
- node affinity
- taints/tolerations
- insufficient CPU/memory
- topology constraints
- PVC/storage constraints
- quotas and other scheduler conditions

## Interview takeaway
PVC binding and Pod scheduling are separate stages. A Bound PVC can coexist with a Pending Pod.
