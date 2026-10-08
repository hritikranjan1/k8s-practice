# LAB 36 — PVC Larger Than PV

## Objective
Troubleshoot a PVC that requests more storage than the available PV.

## Scenario
- PV: `lab36-pv`, 5Gi, RWO, StorageClass `manual`, Retain
- PVC: `lab36-pvc`, 10Gi, RWO, StorageClass `manual`
- Pod: `lab36-pod` consumes the PVC

Expected: PVC Pending and Pod Pending.

## 1. Namespace
```bash
kubectl create namespace troubleshooting-lab
kubectl get ns troubleshooting-lab
```

## 2. PV
Create `lab36-pv.yaml`:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: lab36-pv
spec:
  capacity:
    storage: 5Gi
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /data/lab36
    type: DirectoryOrCreate
```
Apply:
```bash
kubectl apply -f lab36-pv.yaml
kubectl get pv lab36-pv
```

## 3. PVC
Create `lab36-pvc.yaml`:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: lab36-pvc
  namespace: troubleshooting-lab
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: manual
  resources:
    requests:
      storage: 10Gi
```
Apply:
```bash
kubectl apply -f lab36-pvc.yaml
kubectl get pvc lab36-pvc -n troubleshooting-lab
```

## 4. Pod
Create `lab36-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: lab36-pod
  namespace: troubleshooting-lab
spec:
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - name: storage
          mountPath: /data
  volumes:
    - name: storage
      persistentVolumeClaim:
        claimName: lab36-pvc
```
Apply:
```bash
kubectl apply -f lab36-pod.yaml
kubectl get pod lab36-pod -n troubleshooting-lab
```

## 5. Investigation
```bash
kubectl describe pvc lab36-pvc -n troubleshooting-lab
kubectl describe pod lab36-pod -n troubleshooting-lab
kubectl describe pv lab36-pv
kubectl get events -n troubleshooting-lab
```

### Challenge encountered
The PVC showed `Pending` and initially displayed `WaitForFirstConsumer`. The decisive evidence was the Pod event:

```text
FailedScheduling: 0/1 nodes are available: 1 node(s) didn't find available persistent volumes to bind.
```

### Root cause
The PV is only 5Gi but the PVC requests 10Gi:

```text
5Gi < 10Gi
```

StorageClass and access mode match, but capacity does not.

### Fix
Either provide a PV >= 10Gi or recreate the PVC with a request <= 5Gi. Do not expect a claim to shrink an existing request in place.

### Key lesson
`WaitForFirstConsumer` is a scheduling/binding mode, not automatically the root cause. Always inspect Pod/PVC events and compare PV capacity with the PVC request.

### Interview takeaway
A 10Gi PVC cannot bind to a 5Gi PV. Kubernetes needs a suitable PV satisfying the claim's requirements.
