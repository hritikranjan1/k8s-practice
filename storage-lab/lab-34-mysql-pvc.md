# LAB 34 — MySQL + PVC: Persistent Database Storage in Kubernetes

## 📌 Overview

In this lab, we deployed **MySQL inside Kubernetes** and used a **PersistentVolume (PV)** and **PersistentVolumeClaim (PVC)** to store the MySQL database data.

The main goal was to prove that:

> **A Kubernetes Pod can be deleted and recreated without losing MySQL database data when the database uses persistent storage.**

### Architecture

```text
                    Kubernetes
                        │
                 MySQL Deployment
                        │
                        ▼
                   MySQL Pod
                     :3306
                        │
                        │ /var/lib/mysql
                        ▼
                  MySQL PVC
                  mysql-pvc
                        │
                        ▼
                   MySQL PV
                    mysql-pv
                        │
                        ▼
             HostPath: /data/mysql-lab
                        │
                        ▼
                  server-1 disk
```

---

# 1. Objective

By completing this lab, we will learn:

- How to run MySQL in Kubernetes
- How to create a PV for MySQL
- How to create a PVC for MySQL
- How to mount a PVC into a MySQL Pod
- How MySQL stores database files
- How to create a database
- How to create a table
- How to insert data
- How to verify persistent data
- What happens when the MySQL Pod is deleted
- How Kubernetes recreates the Pod
- How the new Pod accesses the existing database
- Why Pod storage and persistent storage are different
- Why HostPath is useful for labs but has production limitations

---

# 2. Environment

### Kubernetes

```text
Kubernetes: RKE2
Version: v1.35.6+rke2r1
Node: server-1
Context: default
```

Verify:

```bash
kubectl config current-context
kubectl get nodes
```

Expected:

```text
default
```

and:

```text
NAME       STATUS   ROLES                AGE   VERSION
server-1   Ready    control-plane,etcd   ...   v1.35.6+rke2r1
```

---

# 3. Lab Namespace

We isolated the complete lab inside:

```text
mysql-lab
```

Create it:

```bash
kubectl create namespace mysql-lab
```

Verify:

```bash
kubectl get namespace mysql-lab
```

---

# 4. Create MySQL PV

File:

```text
mysql-pv.yaml
```

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv

spec:
  capacity:
    storage: 5Gi

  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  storageClassName: mysql-manual

  hostPath:
    path: /data/mysql-lab
    type: DirectoryOrCreate
```

Apply:

```bash
kubectl apply -f mysql-pv.yaml
```

Verify:

```bash
kubectl get pv mysql-pv
```

Expected:

```text
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS
mysql-pv   5Gi        RWO            Retain           Bound
```

---

# 5. Create MySQL PVC

File:

```text
mysql-pvc.yaml
```

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: mysql-lab

spec:
  accessModes:
    - ReadWriteOnce

  storageClassName: mysql-manual

  resources:
    requests:
      storage: 2Gi
```

Apply:

```bash
kubectl apply -f mysql-pvc.yaml
```

Verify:

```bash
kubectl get pvc -n mysql-lab
```

Expected:

```text
NAME        STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS
mysql-pvc   Bound    mysql-pv   5Gi        RWO            mysql-manual
```

### Important observation

The PVC requests:

```text
2Gi
```

while the PV provides:

```text
5Gi
```

This is valid.

A PVC does not have to consume the complete capacity of the PV.

---

# 6. PV ↔ PVC Relationship

The relationship is:

```text
mysql-pv
   │
   │ Bound
   ▼
mysql-pvc
```

Check:

```bash
kubectl describe pvc mysql-pvc -n mysql-lab
```

Look for:

```text
Status:       Bound
Volume:       mysql-pv
StorageClass: mysql-manual
```

Check the PV:

```bash
kubectl describe pv mysql-pv
```

Look for:

```text
Claim: mysql-lab/mysql-pvc
```

---

# 7. Create MySQL Deployment

File:

```text
mysql-deployment.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: mysql
  namespace: mysql-lab

spec:
  replicas: 1

  selector:
    matchLabels:
      app: mysql

  template:
    metadata:
      labels:
        app: mysql

    spec:
      containers:
        - name: mysql
          image: mysql:8.0

          ports:
            - containerPort: 3306

          env:
            - name: MYSQL_ROOT_PASSWORD
              value: "root123"

          volumeMounts:
            - name: mysql-storage
              mountPath: /var/lib/mysql

      volumes:
        - name: mysql-storage
          persistentVolumeClaim:
            claimName: mysql-pvc
```

Apply:

```bash
kubectl apply -f mysql-deployment.yaml
```

Check:

```bash
kubectl get deployment -n mysql-lab
```

Check Pod:

```bash
kubectl get pods -n mysql-lab -o wide
```

Expected:

```text
NAME                     READY   STATUS    RESTARTS
mysql-xxxxxxxxxx-xxxxx   1/1     Running   0
```

---

# 8. Why `/var/lib/mysql`?

MySQL stores its database files under:

```text
/var/lib/mysql
```

Therefore, we mount the PVC at:

```yaml
mountPath: /var/lib/mysql
```

The storage chain becomes:

```text
MySQL
   │
   ▼
/var/lib/mysql
   │
   ▼
mysql-pvc
   │
   ▼
mysql-pv
   │
   ▼
/data/mysql-lab
```

This is the most important part of the lab.

---

# 9. Create MySQL Service

File:

```text
mysql-service.yaml
```

```yaml
apiVersion: v1
kind: Service

metadata:
  name: mysql
  namespace: mysql-lab

spec:
  selector:
    app: mysql

  ports:
    - port: 3306
      targetPort: 3306

  type: ClusterIP
```

Apply:

```bash
kubectl apply -f mysql-service.yaml
```

Check:

```bash
kubectl get svc -n mysql-lab
```

Expected:

```text
NAME    TYPE        CLUSTER-IP      PORT(S)
mysql   ClusterIP   10.43.x.x      3306/TCP
```

The Service provides stable internal networking for MySQL.

---

# 10. Verify Complete Deployment

Run:

```bash
kubectl get all -n mysql-lab
```

Expected components:

```text
Pod
Service
Deployment
ReplicaSet
```

Also:

```bash
kubectl get pv mysql-pv
kubectl get pvc -n mysql-lab
```

Expected:

```text
mysql-pv    Bound
mysql-pvc   Bound
```

---

# 11. Connect to MySQL

Find the MySQL Pod:

```bash
kubectl get pods -n mysql-lab -l app=mysql
```

Example:

```text
mysql-54f47bf789-cmpzf
```

Connect:

```bash
kubectl exec -it -n mysql-lab mysql-54f47bf789-cmpzf -- \
mysql -uroot -proot123
```

You should get:

```text
mysql>
```

---

# 12. Check Existing Databases

Inside MySQL:

```sql
SHOW DATABASES;
```

Expected system databases include:

```text
information_schema
mysql
performance_schema
sys
```

---

# 13. Create Database

Create:

```sql
CREATE DATABASE devops_lab;
```

Verify:

```sql
SHOW DATABASES;
```

Expected:

```text
devops_lab
```

---

# 14. Create Table

Select the database:

```sql
USE devops_lab;
```

Create table:

```sql
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(100)
);
```

Verify:

```sql
SHOW TABLES;
```

Expected:

```text
employees
```

---

# 15. Insert Data

Insert records:

```sql
INSERT INTO employees (name, role)
VALUES
('Anish', 'DevOps Engineer'),
('Rahul', 'QA Engineer'),
('Priya', 'Cloud Engineer');
```

Verify:

```sql
SELECT * FROM employees;
```

Actual lab result:

```text
+----+-------+-----------------+
| id | name  | role            |
+----+-------+-----------------+
|  1 | Anish | DevOps Engineer |
|  2 | Rahul | QA Engineer     |
|  3 | Priya | Cloud Engineer  |
+----+-------+-----------------+
```

Exit:

```sql
EXIT;
```

---

# 16. Verify MySQL Storage

Check the mounted filesystem:

```bash
kubectl exec -it -n mysql-lab mysql-54f47bf789-cmpzf -- \
df -h /var/lib/mysql
```

In this lab, the output showed:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       468G  326G  119G  74% /var/lib/mysql
```

### Important

The `468G` shown here does **not** mean the Kubernetes PV is 468Gi.

The Kubernetes PV is:

```text
5Gi
```

The HostPath points to a directory on the node's existing filesystem:

```text
/data/mysql-lab
```

Therefore the mounted filesystem reports the underlying node filesystem size.

---

# 17. Verify Data on Kubernetes Node

Because this lab uses:

```yaml
hostPath:
  path: /data/mysql-lab
```

the MySQL files can be seen on `server-1`.

Run:

```bash
sudo ls -lah /data/mysql-lab
```

The lab showed MySQL files such as:

```text
devops_lab/
ibdata1
mysql.ibd
mysql/
performance_schema/
sys/
binlog.000001
binlog.000002
```

This proves that MySQL's persistent files exist under:

```text
/data/mysql-lab
```

on the Kubernetes node.

### ⚠️ Warning

Never manually modify or delete MySQL files under:

```text
/data/mysql-lab
```

while MySQL is running.

Doing so can corrupt the database.

---

# 18. MAIN TEST — Delete the MySQL Pod

This is the most important part of the lab.

Delete only the Pod:

```bash
kubectl delete pod <MYSQL-POD-NAME> -n mysql-lab
```

Example:

```bash
kubectl delete pod mysql-54f47bf789-cmpzf -n mysql-lab
```

The Deployment notices that its Pod is missing and creates a replacement.

Watch:

```bash
kubectl get pods -n mysql-lab -w
```

You may see:

```text
mysql-54f47bf789-cmpzf     Terminating
mysql-54f47bf789-2qdhm     ContainerCreating
mysql-54f47bf789-2qdhm     Running
```

The Pod name changed.

---

# 19. Verify New Pod

Run:

```bash
kubectl get pods -n mysql-lab -o wide
```

Actual lab result:

```text
NAME                     READY   STATUS    RESTARTS   AGE   IP          NODE
mysql-54f47bf789-2qdhm   1/1     Running   0          ...   10.42.0.31  server-1
```

Notice:

```text
Old Pod:
mysql-54f47bf789-cmpzf

New Pod:
mysql-54f47bf789-2qdhm
```

The Pod was recreated.

---

# 20. Verify PVC After Pod Deletion

Run:

```bash
kubectl get pvc -n mysql-lab
```

Result:

```text
NAME        STATUS   VOLUME     CAPACITY
mysql-pvc   Bound    mysql-pv   5Gi
```

The PVC was not deleted.

Check PV:

```bash
kubectl get pv mysql-pv
```

Result:

```text
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM
mysql-pv   5Gi        RWO            Retain           Bound    mysql-lab/mysql-pvc
```

Therefore:

```text
Pod changed
PVC stayed
PV stayed
Data stayed
```

---

# 21. Verify Database After Pod Recreation

Find the new Pod:

```bash
kubectl get pods -n mysql-lab -l app=mysql
```

Then:

```bash
kubectl exec -it -n mysql-lab <NEW-POD-NAME> -- \
mysql -uroot -proot123 \
-e "SELECT * FROM devops_lab.employees;"
```

Actual lab result:

```text
+----+-------+-----------------+
| id | name  | role            |
+----+-------+-----------------+
|  1 | Anish | DevOps Engineer |
|  2 | Rahul | QA Engineer     |
|  3 | Priya | Cloud Engineer  |
+----+-------+-----------------+
```

# 🎉 Persistence Test PASSED

The Pod was deleted and recreated, but the database remained intact.

---

# 22. What Actually Happened?

Before deletion:

```text
MySQL Pod #1
     │
     ▼
mysql-pvc
     │
     ▼
mysql-pv
     │
     ▼
/data/mysql-lab
     │
     ▼
MySQL database files
```

Pod was deleted:

```text
MySQL Pod #1
      ❌
```

Deployment recreated it:

```text
MySQL Pod #2
      │
      ▼
mysql-pvc
      │
      ▼
mysql-pv
      │
      ▼
/data/mysql-lab
      │
      ▼
Existing MySQL database
```

Therefore:

```text
Pod lifecycle ≠ Data lifecycle
```

This is the central concept of this lab.

---

# 23. Add Another Record After Pod Recreation

We can also prove that the recreated Pod can write new data.

```bash
kubectl exec -it -n mysql-lab <NEW-POD-NAME> -- \
mysql -uroot -proot123 \
-e "INSERT INTO devops_lab.employees (name, role) VALUES ('DevOps Lab', 'Kubernetes Engineer');"
```

Verify:

```bash
kubectl exec -it -n mysql-lab <NEW-POD-NAME> -- \
mysql -uroot -proot123 \
-e "SELECT * FROM devops_lab.employees;"
```

Expected:

```text
+----+-----------+----------------------+
| id | name      | role                 |
+----+-----------+----------------------+
|  1 | Anish     | DevOps Engineer      |
|  2 | Rahul     | QA Engineer          |
|  3 | Priya     | Cloud Engineer       |
|  4 | DevOps Lab| Kubernetes Engineer  |
+----+-----------+----------------------+
```

This proves the new Pod can both **read and write** the persistent database.

---

# 24. Inspect Pod → PVC Relationship

Run:

```bash
kubectl describe pod -n mysql-lab <NEW-POD-NAME>
```

Look for:

```text
Volumes:
  mysql-storage:
    Type:       PersistentVolumeClaim
    ClaimName:  mysql-pvc
```

This confirms the Pod is using:

```text
mysql-pvc
```

---

# 25. Inspect PVC → PV Relationship

Run:

```bash
kubectl describe pvc mysql-pvc -n mysql-lab
```

Look for:

```text
Status:       Bound
Volume:       mysql-pv
```

Relationship:

```text
Pod
 │
 ▼
PVC: mysql-pvc
 │
 ▼
PV: mysql-pv
```

---

# 26. Inspect PV → Node Storage

Run:

```bash
kubectl describe pv mysql-pv
```

Look for:

```text
Source:
  Type:      HostPath
  Path:      /data/mysql-lab
```

Therefore:

```text
PV
 │
 ▼
HostPath
 │
 ▼
/data/mysql-lab
```

---

# 27. Important HostPath Limitation

This lab uses:

```yaml
hostPath:
  path: /data/mysql-lab
```

This is excellent for learning and local/on-prem experimentation.

However, HostPath is generally **not the preferred production database storage architecture**.

Why?

Because the data physically belongs to:

```text
server-1
```

If the Pod moves to another node:

```text
server-2
```

the directory:

```text
/data/mysql-lab
```

may not contain the same data.

Production environments commonly use storage systems that can provide storage independently of the individual Kubernetes node.

Examples include:

```text
CSI-based storage
Ceph
Longhorn
Cloud block storage
Enterprise SAN/NAS solutions
Cloud Persistent Disks
```

---

# 28. Why MySQL Production Deployments Are Different

For learning, we used:

```text
Deployment
   +
MySQL
   +
PVC
```

This works for demonstrating persistence.

For production databases, however, additional concerns exist:

- StatefulSet
- stable identity
- database replication
- backups
- recovery
- failover
- storage replication
- encryption
- secrets management
- resource limits
- monitoring
- alerts
- upgrades
- database operators

A production MySQL architecture may look more like:

```text
              Application
                   │
                   ▼
              MySQL Service
                   │
                   ▼
             MySQL StatefulSet
                   │
          ┌────────┴────────┐
          ▼                 ▼
       MySQL-0           MySQL-1
          │                 │
          ▼                 ▼
       PVC-0              PVC-1
          │                 │
          ▼                 ▼
     CSI Storage       CSI Storage
```

---

# 29. Common Troubleshooting

## Problem 1 — PVC Pending

Check:

```bash
kubectl get pvc -n mysql-lab
kubectl describe pvc mysql-pvc -n mysql-lab
```

Common causes:

- StorageClass mismatch
- PV doesn't exist
- PV capacity insufficient
- Access mode mismatch
- StorageClass name mismatch

---

## Problem 2 — MySQL Pod Pending

Check:

```bash
kubectl describe pod -n mysql-lab <POD-NAME>
```

Look at:

```text
Events:
```

Possible storage problem:

```text
persistentvolumeclaim "mysql-pvc" not found
```

Remember:

> PVCs are namespace-scoped.

The Pod and PVC must be in:

```text
mysql-lab
```

---

## Problem 3 — MySQL CrashLoopBackOff

Check:

```bash
kubectl logs -n mysql-lab <POD-NAME>
```

Possible causes:

- Incorrect environment variables
- Incorrect MySQL configuration
- Corrupted database files
- Permission problems
- Existing incompatible data directory

---

## Problem 4 — Database disappeared after Pod restart

Check:

```bash
kubectl get pvc -n mysql-lab
kubectl get pv mysql-pv
```

Then verify the Pod actually mounts the PVC:

```bash
kubectl describe pod -n mysql-lab <POD-NAME>
```

Check:

```text
ClaimName: mysql-pvc
```

Also verify:

```bash
df -h /var/lib/mysql
```

---

# 30. Useful Commands

### View all lab resources

```bash
kubectl get all -n mysql-lab
```

### View Pods

```bash
kubectl get pods -n mysql-lab -o wide
```

### View PVC

```bash
kubectl get pvc -n mysql-lab
```

### View PV

```bash
kubectl get pv mysql-pv
```

### Describe Pod

```bash
kubectl describe pod -n mysql-lab <POD-NAME>
```

### View logs

```bash
kubectl logs -n mysql-lab <POD-NAME>
```

### Execute MySQL query

```bash
kubectl exec -it -n mysql-lab <POD-NAME> -- \
mysql -uroot -proot123 \
-e "SHOW DATABASES;"
```

### Check mounted storage

```bash
kubectl exec -it -n mysql-lab <POD-NAME> -- \
df -h /var/lib/mysql
```

---

# 31. Lab Verification Checklist

| Test | Result |
|---|---|
| Namespace created | ✅ |
| PV created | ✅ |
| PVC created | ✅ |
| PV/PVC Bound | ✅ |
| MySQL Deployment | ✅ |
| MySQL Pod Running | ✅ |
| MySQL Service | ✅ |
| Database created | ✅ |
| Table created | ✅ |
| Data inserted | ✅ |
| Data visible | ✅ |
| MySQL files on persistent storage | ✅ |
| MySQL Pod deleted | ✅ |
| New Pod created | ✅ |
| PVC remained Bound | ✅ |
| PV remained Bound | ✅ |
| Database survived Pod deletion | ✅ |
| Records survived Pod deletion | ✅ |

---

# 32. Final Architecture

```text
                         Kubernetes Cluster
                                │
                                ▼
                       ┌─────────────────┐
                       │ MySQL Deployment│
                       │    replicas: 1  │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    MySQL Pod    │
                       │      :3306      │
                       └────────┬────────┘
                                │
                       /var/lib/mysql
                                │
                                ▼
                       ┌─────────────────┐
                       │    mysql-pvc    │
                       │      2Gi        │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     mysql-pv    │
                       │       5Gi       │
                       │      RWO        │
                       │     Retain      │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    HostPath     │
                       │ /data/mysql-lab │
                       └────────┬────────┘
                                │
                                ▼
                             server-1
```

---

# 33. Key DevOps Lessons

### Lesson 1

Pods are temporary.

```text
Pod can be deleted/recreated.
```

### Lesson 2

Database data should not depend on Pod lifetime.

```text
MySQL → PVC → PV → Storage
```

### Lesson 3

PVC requests storage; PV provides storage.

```text
PVC: 2Gi request
PV:  5Gi capacity
```

### Lesson 4

`ReadWriteOnce` means the volume can be mounted read-write by one node.

It does **not simply mean "one Pod only."**

### Lesson 5

`Retain` protects the PV/data from automatic deletion when the PVC is deleted.

### Lesson 6

HostPath is useful for labs but has node-local limitations.

### Lesson 7

For production databases, persistence alone is not enough.

You also need:

```text
Backup
Replication
Monitoring
Failover
Security
Recovery
Storage reliability
```

---

# 34. Interview Questions

### Q1. Why do we use PVC with MySQL?

To keep database data independent of the lifecycle of the MySQL Pod.

### Q2. What happens when the MySQL Pod is deleted?

The Deployment creates a replacement Pod. The new Pod mounts the same PVC and can access the existing database data.

### Q3. Does deleting a Pod delete the PVC?

No.

```text
Pod ≠ PVC
```

### Q4. Does deleting a PVC always delete the underlying data?

Not necessarily. It depends on the PV reclaim policy and storage backend.

In this lab:

```text
Retain
```

was used.

### Q5. Why did we use `/var/lib/mysql`?

That is the MySQL data directory used by the MySQL container.

### Q6. What is the difference between PV and PVC?

```text
PV = storage resource provided to Kubernetes

PVC = request for storage made by a workload/user
```

### Q7. Why did we use `hostPath`?

Because this is a local Kubernetes lab and it provides a simple way to demonstrate persistent storage.

### Q8. Is HostPath recommended for production databases?

Generally no. Production environments normally use reliable storage solutions exposed through CSI or other storage platforms.

### Q9. Why did the database survive Pod deletion?

Because the MySQL data directory was mounted from a PVC backed by a persistent PV.

### Q10. What is the most important concept from this lab?

```text
Pod lifecycle ≠ Data lifecycle
```

---

# 35. Cleanup

⚠️ Only perform cleanup when you have finished the lab.

Because the PV uses:

```text
Retain
```

deleting the PVC does not automatically mean the underlying data is safely gone.

Check first:

```bash
kubectl get pvc -n mysql-lab
kubectl get pv mysql-pv
```

If you want to remove the lab:

```bash
kubectl delete deployment mysql -n mysql-lab
kubectl delete service mysql -n mysql-lab
kubectl delete pvc mysql-pvc -n mysql-lab
kubectl delete pv mysql-pv
kubectl delete namespace mysql-lab
```

Then, because this is a HostPath lab, inspect:

```bash
sudo ls -lah /data/mysql-lab
```

Only remove the directory if you are **certain you no longer need the lab's database data**:

```bash
sudo rm -rf /data/mysql-lab
```

Never run that command against production database storage.

---

# 36. Final Result

**LAB 34 — MySQL + PVC completed successfully.**

The practical demonstrated:

```text
MySQL
  ↓
PVC
  ↓
PV
  ↓
Persistent Storage
```

We created:

```text
mysql-pv
mysql-pvc
mysql Deployment
mysql Service
```

We then:

```text
Created database
      ↓
Created table
      ↓
Inserted records
      ↓
Deleted MySQL Pod
      ↓
Deployment created new Pod
      ↓
Mounted same PVC
      ↓
Database still existed
      ↓
Records still existed
```

### 🎯 Core DevOps takeaway

> **Kubernetes Pods are disposable, but application data must live on persistent storage when the application requires state to survive Pod replacement.**
