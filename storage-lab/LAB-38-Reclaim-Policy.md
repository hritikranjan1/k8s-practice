# LAB 38 — PV Reclaim Policy Troubleshooting

## Objective
Understand what happens when a PVC is deleted and the PV has a reclaim policy such as `Delete` or `Retain`.

## Scenario
- PV: 2Gi, RWO
- StorageClass: `lab38-storage`
- PV reclaim policy: `Delete`
- PVC: 1Gi
- Pod: nginx

## 1. Storage directory
```bash
sudo mkdir -p /data/lab38
sudo chmod 777 /data/lab38
```

## 2. StorageClass
`lab38-storageclass.yaml`:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: lab38-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```
Apply:
```bash
kubectl apply -f lab38-storageclass.yaml
```

## 3. PV
`lab38-pv.yaml`:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: lab38-pv
spec:
  capacity:
    storage: 2Gi
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Delete
  storageClassName: lab38-storage
  hostPath:
    path: /data/lab38
    type: DirectoryOrCreate
```
Apply:
```bash
kubectl apply -f lab38-pv.yaml
```

## 4. PVC
`lab38-pvc.yaml`:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: lab38-pvc
  namespace: troubleshooting-lab
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: lab38-storage
  resources:
    requests:
      storage: 1Gi
```
Apply:
```bash
kubectl apply -f lab38-pvc.yaml
```

## 5. Pod
`lab38-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: lab38-pod
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
        claimName: lab38-pvc
```
Apply:
```bash
kubectl apply -f lab38-pod.yaml
kubectl get pod lab38-pod -n troubleshooting-lab
```

## 6. Write data
```bash
kubectl exec -it lab38-pod -n troubleshooting-lab -- bash
```
Inside:
```bash
echo "LAB38 IMPORTANT DATA" > /data/data.txt
cat /data/data.txt
exit
```
Verify host data:
```bash
sudo cat /data/lab38/data.txt
```

## 7. Failure simulation
Delete the PVC:
```bash
kubectl delete pvc lab38-pvc -n troubleshooting-lab
```
Investigate:
```bash
kubectl get pv lab38-pv
kubectl describe pv lab38-pv
kubectl get events -n troubleshooting-lab
sudo ls -la /data/lab38
```

## Important challenge
Do not assume `Delete` means every byte under every storage backend will be erased. Reclaim behavior depends on the volume type/provisioner. For a HostPath lab, inspect the actual directory rather than guessing.

## Retain vs Delete

### Retain
```text
PVC deleted
   ↓
PV retained / generally Released
   ↓
administrator handles recovery/reuse
```

### Delete
```text
PVC deleted
   ↓
PV is reclaimed/deleted according to volume/provisioner behavior
```

`Retain` is not a backup.

## Interview takeaway
Reclaim policy controls the lifecycle of storage after a claim is released. Production databases still require independent backups and disaster recovery.
