# LAB 40 — Final PV/PVC Mini Project

## Objective
Build a complete persistent application stack without relying on previous lab YAML: Nginx and MySQL, each with Deployment + PVC + PV, then prove persistence across Pod and Deployment deletion and understand reclaim behavior.

## Architecture
```text
                    Kubernetes Cluster
                           |
              ┌────────────┴────────────┐
              |                         |
            Nginx                     MySQL
              |                         |
        Deployment                 Deployment
              |                         |
            PVC                       PVC
              |                         |
             PV                        PV
              |                         |
      /data/lab40-nginx        /data/lab40-mysql
```

## 1. Namespace
```bash
kubectl create namespace pv-pvc-final
kubectl get ns pv-pvc-final
```

## 2. Directory
```bash
cd ~/test/k8s-practice
mkdir -p lab40
cd lab40
```

## 3. Host storage
```bash
sudo mkdir -p /data/lab40-nginx /data/lab40-mysql
sudo chmod 777 /data/lab40-nginx /data/lab40-mysql
```
For production, do not blindly use `777`; use correct UID/GID and security controls.

## 4. Nginx PV — `nginx-pv.yaml`
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: lab40-nginx-pv
spec:
  capacity:
    storage: 2Gi
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: lab40-nginx
  hostPath:
    path: /data/lab40-nginx
    type: DirectoryOrCreate
```
Apply:
```bash
kubectl apply -f nginx-pv.yaml
kubectl get pv lab40-nginx-pv
```

## 5. MySQL PV — `mysql-pv.yaml`
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: lab40-mysql-pv
spec:
  capacity:
    storage: 5Gi
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  storageClassName: lab40-mysql
  hostPath:
    path: /data/lab40-mysql
    type: DirectoryOrCreate
```
Apply:
```bash
kubectl apply -f mysql-pv.yaml
kubectl get pv
```

## 6. Nginx PVC — `nginx-pvc.yaml`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: lab40-nginx-pvc
  namespace: pv-pvc-final
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: lab40-nginx
  resources:
    requests:
      storage: 1Gi
```
Apply:
```bash
kubectl apply -f nginx-pvc.yaml
kubectl get pvc -n pv-pvc-final
```

## 7. MySQL PVC — `mysql-pvc.yaml`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: lab40-mysql-pvc
  namespace: pv-pvc-final
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: lab40-mysql
  resources:
    requests:
      storage: 3Gi
```
Apply:
```bash
kubectl apply -f mysql-pvc.yaml
kubectl get pvc -n pv-pvc-final
```

Checkpoint:
```bash
kubectl get pv
kubectl get pvc -n pv-pvc-final
```
Expected:
```text
lab40-nginx-pv  <-> lab40-nginx-pvc
lab40-mysql-pv  <-> lab40-mysql-pvc
```

## 8. Nginx Deployment — `nginx-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lab40-nginx
  namespace: pv-pvc-final
spec:
  replicas: 1
  selector:
    matchLabels:
      app: lab40-nginx
  template:
    metadata:
      labels:
        app: lab40-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-storage
              mountPath: /usr/share/nginx/html
      volumes:
        - name: nginx-storage
          persistentVolumeClaim:
            claimName: lab40-nginx-pvc
```
Apply:
```bash
kubectl apply -f nginx-deployment.yaml
kubectl get deployment -n pv-pvc-final
kubectl get pods -n pv-pvc-final
```

## 9. Persistent Nginx HTML
Find the Pod:
```bash
kubectl get pods -n pv-pvc-final
```
Enter it:
```bash
kubectl exec -it <NGINX_POD> -n pv-pvc-final -- bash
```
Create the page:
```bash
cat > /usr/share/nginx/html/index.html <<'HTML'
<html>
<head><title>LAB 40</title></head>
<body>
<h1>Welcome to LAB 40</h1>
<h2>Kubernetes Persistent Storage</h2>
<p>This HTML file is stored on a Persistent Volume.</p>
<p>Application: Nginx</p>
</body>
</html>
HTML
cat /usr/share/nginx/html/index.html
exit
```
Verify on host:
```bash
sudo cat /data/lab40-nginx/index.html
```

## 10. MySQL Deployment — `mysql-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lab40-mysql
  namespace: pv-pvc-final
spec:
  replicas: 1
  selector:
    matchLabels:
      app: lab40-mysql
  template:
    metadata:
      labels:
        app: lab40-mysql
    spec:
      containers:
        - name: mysql
          image: mysql:8.0
          ports:
            - containerPort: 3306
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: rootpass
            - name: MYSQL_DATABASE
              value: devops_final
          volumeMounts:
            - name: mysql-storage
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-storage
          persistentVolumeClaim:
            claimName: lab40-mysql-pvc
```
Apply:
```bash
kubectl apply -f mysql-deployment.yaml
kubectl get pods -n pv-pvc-final
```
If MySQL fails:
```bash
kubectl logs deployment/lab40-mysql -n pv-pvc-final
kubectl describe pod -l app=lab40-mysql -n pv-pvc-final
```

## 11. Create database, table, records
Find MySQL Pod:
```bash
kubectl get pods -n pv-pvc-final
```
Connect:
```bash
kubectl exec -it <MYSQL_POD> -n pv-pvc-final -- mysql -uroot -prootpass
```
Run:
```sql
SHOW DATABASES;
USE devops_final;
CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  role VARCHAR(100)
);
INSERT INTO employees VALUES
(1, 'Anish', 'DevOps Engineer'),
(2, 'Rahul', 'QA Engineer'),
(3, 'Priya', 'Cloud Engineer');
SELECT * FROM employees;
exit;
```

## 12. Verify storage
```bash
sudo ls -lah /data/lab40-mysql
```
Do not manually edit/delete MySQL files while MySQL is running.

# Persistence Test 1 — Delete Nginx Pod

```bash
kubectl get pods -n pv-pvc-final
kubectl delete pod <NGINX_POD> -n pv-pvc-final
kubectl get pods -n pv-pvc-final -w
```
Press `Ctrl+C` after the replacement is Running.

Verify:
```bash
kubectl exec <NEW_NGINX_POD> -n pv-pvc-final -- cat /usr/share/nginx/html/index.html
```
Expected: custom HTML still exists.

# Persistence Test 2 — Delete MySQL Pod

```bash
kubectl delete pod <MYSQL_POD> -n pv-pvc-final
kubectl get pods -n pv-pvc-final -w
```
Connect to the new Pod:
```bash
kubectl exec -it <NEW_MYSQL_POD> -n pv-pvc-final -- mysql -uroot -prootpass
```
Verify:
```sql
USE devops_final;
SELECT * FROM employees;
```
Expected: all three records remain.

# Persistence Test 3 — Delete Nginx Deployment

```bash
kubectl delete deployment lab40-nginx -n pv-pvc-final
kubectl get pods -n pv-pvc-final
kubectl get pvc -n pv-pvc-final
kubectl get pv
```
The Pod disappears, but the PVC/PV remain.

Recreate:
```bash
kubectl apply -f nginx-deployment.yaml
kubectl get pods -n pv-pvc-final
```
Verify HTML again.

# Persistence Test 4 — Delete MySQL Deployment

```bash
kubectl delete deployment lab40-mysql -n pv-pvc-final
kubectl get pvc -n pv-pvc-final
kubectl get pv
```
Recreate:
```bash
kubectl apply -f mysql-deployment.yaml
kubectl get pods -n pv-pvc-final
```
Verify the database records again.

# Final Reclaim Test — Retain

Delete Nginx Deployment first:
```bash
kubectl delete deployment lab40-nginx -n pv-pvc-final
```
Delete its PVC:
```bash
kubectl delete pvc lab40-nginx-pvc -n pv-pvc-final
```
Check:
```bash
kubectl get pv lab40-nginx-pv
```
Expected status: `Released`.

Verify the underlying HostPath:
```bash
sudo ls -lah /data/lab40-nginx
sudo cat /data/lab40-nginx/index.html
```
The data should still be present because the PV uses `Retain`.

Repeat for MySQL:
```bash
kubectl delete deployment lab40-mysql -n pv-pvc-final
kubectl delete pvc lab40-mysql-pvc -n pv-pvc-final
kubectl get pv
sudo ls -lah /data/lab40-mysql
```

# What the project proved

## Pod deletion
```text
Pod deleted
  ↓
Deployment creates new Pod
  ↓
Same PVC/PV
  ↓
Same data
```

## Deployment deletion
```text
Deployment deleted
  ↓
Pod deleted
  ↓
PVC remains
  ↓
PV remains
  ↓
Data remains
```

## PVC deletion with Retain
```text
PVC deleted
  ↓
PV becomes Released
  ↓
Storage is retained
  ↓
Administrator handles recovery/reuse
```

# Important production lessons

- `Retain` is not a backup.
- HostPath is mainly suitable for local/testing scenarios and has node-local limitations.
- Do not use `chmod 777` blindly in production.
- Database persistence should be combined with tested backups and disaster recovery.
- A Deployment manages Pods; it does not own the persistent data itself.

# Final checklist

- [x] Nginx PV/PVC/Deployment
- [x] Persistent custom HTML
- [x] MySQL PV/PVC/Deployment
- [x] Database/table/records
- [x] Pod deletion and data verification
- [x] Deployment deletion/recreation and data verification
- [x] PVC deletion
- [x] PV `Released` observation
- [x] Underlying storage verification
- [x] Reclaim policy understanding

# Interview summary

```text
PV  = actual Kubernetes storage resource
PVC = request for storage
StorageClass = storage/provisioning policy
Pod = consumes the PVC
Deployment = manages Pods
```

Core rule:

```text
Pod deletion != data deletion
Deployment deletion != PVC deletion
PVC deletion + Retain -> PV Released and administrator intervention
```
