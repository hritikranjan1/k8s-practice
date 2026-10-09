
# Kubernetes Persistent Volumes (PV) & Persistent Volume Claims (PVC)

> Complete Kubernetes PV/PVC learning notes, practical implementation, troubleshooting, real-world use cases, failure scenarios, and interview preparation.

---

## Table of Contents

- [1. What I Learned](#1-what-i-learned)
- [2. Why Kubernetes Storage Is Required](#2-why-kubernetes-storage-is-required)
- [3. Container Storage vs Persistent Storage](#3-container-storage-vs-persistent-storage)
- [4. Kubernetes Storage Architecture](#4-kubernetes-storage-architecture)
- [5. PersistentVolume PV](#5-persistentvolume-pv)
- [6. PersistentVolumeClaim PVC](#6-persistentvolumeclaim-pvc)
- [7. StorageClass](#7-storageclass)
- [8. Provisioner](#8-provisioner)
- [9. Static Provisioning](#9-static-provisioning)
- [10. Dynamic Provisioning](#10-dynamic-provisioning)
- [11. PV PVC Binding](#11-pv-pvc-binding)
- [12. PV and PVC Matching Rules](#12-pv-and-pvc-matching-rules)
- [13. Access Modes](#13-access-modes)
- [14. Volume Modes](#14-volume-modes)
- [15. Reclaim Policies](#15-reclaim-policies)
- [16. WaitForFirstConsumer](#16-waitforfirstconsumer)
- [17. HostPath](#17-hostpath)
- [18. StorageClass in My RKE2 Cluster](#18-storageclass-in-my-rke2-cluster)
- [19. Important kubectl Commands](#19-important-kubectl-commands)
- [20. PV/PVC YAML Examples](#20-pvpvc-yaml-examples)
- [21. Practical Labs 1-40](#21-practical-labs-1-40)
- [22. Important Issues I Faced](#22-important-issues-i-faced)
- [23. Troubleshooting Methodology](#23-troubleshooting-methodology)
- [24. Nginx Persistent Storage](#24-nginx-persistent-storage)
- [25. MySQL Persistent Storage](#25-mysql-persistent-storage)
- [26. Final Nginx + MySQL Project](#26-final-nginx--mysql-project)
- [27. Real-World DevOps Use Cases](#27-real-world-devops-use-cases)
- [28. Production Considerations](#28-production-considerations)
- [29. Common Mistakes](#29-common-mistakes)
- [30. Troubleshooting Decision Tree](#30-troubleshooting-decision-tree)
- [31. Interview Questions](#31-interview-questions)
- [32. Important Commands Cheat Sheet](#32-important-commands-cheat-sheet)
- [33. What I Implemented](#33-what-i-implemented)
- [34. What I Learned](#34-what-i-learned)
- [35. Final Summary](#35-final-summary)

---

# 1. What I Learned

This documentation contains my complete learning and practical implementation of Kubernetes:

- PersistentVolume (PV)
- PersistentVolumeClaim (PVC)
- StorageClass
- Static provisioning
- Dynamic provisioning
- Provisioners
- Access modes
- Volume modes
- Reclaim policies
- HostPath
- `WaitForFirstConsumer`
- PV/PVC binding
- PVC expansion
- Persistent application data
- Storage troubleshooting
- Nginx persistent storage
- MySQL persistent storage
- Pod failure testing
- Deployment failure testing
- PVC deletion testing
- Retain policy
- StorageClass mismatch
- Capacity mismatch
- Pending PVC troubleshooting
- Pending Pod troubleshooting

I performed multiple practical labs, including intentionally creating storage failures so that I could understand how Kubernetes behaves in real situations.

---

# 2. Why Kubernetes Storage Is Required

Kubernetes Pods are generally temporary.

A Pod can be:

- deleted
- recreated
- restarted
- rescheduled
- replaced during Deployment updates
- moved between nodes

For stateless applications, this is usually fine.

But many applications store important data.

Examples:

- MySQL
- PostgreSQL
- MongoDB
- Redis
- application uploads
- images
- videos
- reports
- user files
- generated documents
- persistent logs

For example:

```text
MySQL Pod
    |
    +-- /var/lib/mysql
            |
            +-- database files
```

If MySQL stores everything only inside the temporary container filesystem, deleting the Pod can cause data loss.

Therefore Kubernetes provides persistent storage abstractions.

---

# 3. Container Storage vs Persistent Storage

## 3.1 Container Filesystem

A container has its own writable filesystem.

Example:

```text
Container
   |
   +-- /app
   +-- /tmp
   +-- /data
```

If the container is destroyed, data written only to this filesystem may disappear.

---

## 3.2 Persistent Storage

Persistent storage exists separately from the container lifecycle.

```text
Pod
 |
PVC
 |
PV
 |
Storage
```

If the Pod is deleted:

```text
Pod
 X
 |
PVC
 |
PV
 |
Storage
```

The storage can continue to exist.

A new Pod can mount the same PVC.

---

# 4. Kubernetes Storage Architecture

The basic Kubernetes storage architecture is:

```text
                 Application
                      |
                      v
                     Pod
                      |
                      v
                     PVC
                      |
                      v
                StorageClass
                      |
                      v
                 Provisioner
                      |
                      v
                     PV
                      |
                      v
              Storage Backend
```

For static provisioning:

```text
Administrator
      |
      v
     PV
      |
      v
     PVC
      |
      v
     Pod
```

For dynamic provisioning:

```text
Pod
 |
PVC
 |
StorageClass
 |
Provisioner
 |
PV
 |
Storage Backend
```

---

# 5. PersistentVolume (PV)

## 5.1 What is a PV?

PersistentVolume is a Kubernetes resource representing storage available to the cluster.

Simple explanation:

> PV is the actual storage resource that Kubernetes can assign to an application.

Example:

```yaml
apiVersion: v1
kind: PersistentVolume

metadata:
  name: example-pv

spec:

  capacity:
    storage: 5Gi

  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  storageClassName: manual

  hostPath:
    path: /data/example
    type: DirectoryOrCreate
```

---

## 5.2 Important PV Fields

### capacity

```yaml
capacity:
  storage: 5Gi
```

Defines the capacity of the PV.

---

### accessModes

```yaml
accessModes:
  - ReadWriteOnce
```

Defines how the volume can be accessed.

---

### storageClassName

```yaml
storageClassName: manual
```

Associates the PV with a StorageClass.

---

### persistentVolumeReclaimPolicy

Example:

```yaml
persistentVolumeReclaimPolicy: Retain
```

Controls what happens to the PV after its PVC is deleted.

---

### hostPath

Example:

```yaml
hostPath:
  path: /data/example
```

Uses a directory from the Kubernetes node.

---

# 6. PersistentVolumeClaim (PVC)

## 6.1 What is a PVC?

PVC stands for:

> PersistentVolumeClaim

A PVC is a request for storage.

Simple explanation:

```text
PV  = Storage available

PVC = Storage required
```

Example:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: example-pvc
  namespace: storage-lab

spec:

  accessModes:
    - ReadWriteOnce

  storageClassName: manual

  resources:
    requests:
      storage: 2Gi
```

The application normally uses the PVC rather than directly selecting a PV.

---

# 7. StorageClass

## 7.1 What is a StorageClass?

StorageClass defines a type/class of storage.

It tells Kubernetes:

- which provisioner to use
- how storage should be created
- when volume binding should happen
- reclaim behavior
- expansion capabilities
- storage parameters

Example:

```yaml
apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:
  name: example-storage

provisioner: kubernetes.io/no-provisioner

volumeBindingMode: WaitForFirstConsumer
```

---

## 7.2 Simple Example

Think about a company with different storage types:

```text
StorageClass
|
+-- fast-storage
|
+-- standard-storage
|
+-- high-capacity-storage
|
+-- encrypted-storage
```

An application can request the required type.

---

# 8. Provisioner

A provisioner creates/provides storage for dynamic provisioning.

Example from my cluster:

```text
local-path
    |
    +-- rancher.io/local-path
```

The provisioner receives a storage request and creates the appropriate PV/backend storage.

---

# 9. Static Provisioning

In static provisioning, the administrator creates PVs manually.

Flow:

```text
Administrator
      |
      v
     PV
      |
      v
     PVC
      |
      v
     Pod
```

Example:

```text
PV = 5Gi
PVC = 2Gi
```

If all requirements match:

```text
PV
 |
 +--- Bound ---+
               |
              PVC
```

---

## Advantages

- Easy to understand
- Useful for learning
- Useful for pre-existing storage
- Administrator has direct control

## Disadvantages

- Manual work
- Difficult to manage at scale
- Every PV may need manual creation

---

# 10. Dynamic Provisioning

Dynamic provisioning automatically creates storage when a PVC requests a StorageClass supported by a provisioner.

Flow:

```text
PVC
 |
StorageClass
 |
Provisioner
 |
PV
 |
Storage
```

Example:

```yaml
storageClassName: local-path
```

The provisioner:

```text
rancher.io/local-path
```

can create the PV automatically.

---

## Static vs Dynamic

| Feature | Static | Dynamic |
|---|---|---|
| PV creation | Manual | Automatic |
| Provisioner required | Usually no | Yes |
| Scaling | More manual | Easier |
| Production usage | Possible | Very common |
| Lab learning | Excellent | Excellent |

---

# 11. PV/PVC Binding

Kubernetes tries to match a PVC with a suitable PV.

Example:

```text
PV
5Gi
RWO
manual

       |
       | Match
       v

PVC
2Gi
RWO
manual
```

Result:

```text
PV  = Bound
PVC = Bound
```

---

# 12. PV and PVC Matching Rules

Kubernetes considers multiple requirements.

Important factors include:

- capacity
- access modes
- StorageClass
- volume mode
- selectors
- volume binding constraints
- other compatibility requirements

---

## Example 1 — Works

```text
PV = 5Gi
PVC = 2Gi
```

Because:

```text
5Gi >= 2Gi
```

---

## Example 2 — Does Not Work

```text
PV = 5Gi
PVC = 10Gi
```

Because:

```text
5Gi < 10Gi
```

---

## Example 3 — StorageClass mismatch

```text
PV:
storageClassName = manual

PVC:
storageClassName = fast
```

The PVC cannot use that specific manual PV simply because both are storage resources.

The StorageClass requirement must also be satisfied.

However, if `fast` is a valid dynamic StorageClass, Kubernetes may provision a different PV for the PVC.

---

# 13. Access Modes

Kubernetes supports several access modes.

---

## 13.1 ReadWriteOnce — RWO

```yaml
accessModes:
  - ReadWriteOnce
```

Meaning:

> The volume can be mounted read-write from one node.

Simple representation:

```text
Node 1
 |
 +---- Pod
       |
      PVC
       |
      PV
```

Important:

> RWO should not simply be interpreted as "only one Pod can ever use the volume."

The important restriction is generally one node for read-write mounting.

---

## 13.2 ReadOnlyMany — ROX

```text
Read Only
Many Nodes
```

Multiple nodes can mount the volume read-only if the storage backend supports it.

---

## 13.3 ReadWriteMany — RWX

```text
Read + Write
Many Nodes
```

Useful for shared storage.

The underlying storage backend must support RWX.

---

# 14. Volume Modes

Kubernetes supports two common volume modes.

---

## 14.1 Filesystem

```yaml
volumeMode: Filesystem
```

The volume is mounted as a filesystem.

Example:

```text
/data
```

Most normal applications use this.

---

## 14.2 Block

```yaml
volumeMode: Block
```

The application gets a raw block device.

Useful for applications requiring direct block storage.

---

# 15. Reclaim Policies

The reclaim policy controls what happens to storage after a PVC is deleted.

---

## 15.1 Retain

```yaml
persistentVolumeReclaimPolicy: Retain
```

Flow:

```text
PV
 |
PVC
 |
Pod
 |
Data
 |
PVC deleted
 |
PV becomes Released
```

The underlying data can remain.

---

## Important

Retain does NOT mean:

```text
Backup
```

It means storage is retained according to the PV/storage backend lifecycle.

You still need:

- backups
- snapshots
- disaster recovery
- replication

---

## 15.2 Delete

```yaml
persistentVolumeReclaimPolicy: Delete
```

The storage may be deleted/cleaned up according to the storage backend/provisioner.

---

## 15.3 Recycle

Recycle was an older reclaim mechanism and is deprecated/removed from modern Kubernetes usage.

Do not design new production systems around it.

---

# 16. WaitForFirstConsumer

One of the most important concepts I learned.

A StorageClass may contain:

```yaml
volumeBindingMode: WaitForFirstConsumer
```

Instead of immediately binding/provisioning a volume, Kubernetes waits until a Pod actually consumes the PVC.

Flow:

```text
PVC created
     |
     v
PVC Pending
     |
     v
Pod created
     |
     v
Scheduler evaluates Pod
     |
     v
Storage binding/provisioning
     |
     v
Pod scheduled
```

This is especially useful for topology-aware storage.

For local storage, Kubernetes needs to consider:

```text
Which node will run the Pod?
```

before deciding which local storage should be used.

---

# 17. HostPath

HostPath uses a directory from the Kubernetes node.

Example:

```yaml
hostPath:
  path: /data/k8s-storage
  type: DirectoryOrCreate
```

If the Pod runs on:

```text
server-1
```

the data is stored on:

```text
server-1:/data/k8s-storage
```

---

## Advantages

- Very easy for labs
- Easy to inspect
- Easy to understand
- Good for local testing

---

## Disadvantages

- Storage is tied to a node
- Not automatically distributed
- Node failure can affect access
- Not ideal for production
- Moving a Pod to another node can cause storage problems

---

# 18. StorageClass in My RKE2 Cluster

During the practical work, I inspected the cluster StorageClasses.

Important classes included:

```text
manual
local-path
pvc-expansion
```

---

## manual

The manual StorageClass used:

```text
kubernetes.io/no-provisioner
```

Meaning:

```text
No dynamic provisioning
```

PV must be manually created.

---

## local-path

The local-path StorageClass used:

```text
rancher.io/local-path
```

This supports dynamic provisioning of local storage.

Flow:

```text
PVC
 |
local-path
 |
rancher.io/local-path
 |
Dynamic PV
```

---

## pvc-expansion

The expansion lab used a StorageClass with:

```text
allowVolumeExpansion: true
```

However, PVC expansion still depended on backend/controller support.

---

## CSI Check

I checked:

```bash
kubectl get csidrivers
```

There were no CSI drivers available in the lab environment.

This helped explain why the expansion test did not automatically complete.

---

# 19. Important kubectl Commands

## Get PVs

```bash
kubectl get pv
```

Alias:

```bash
kgpv
```

---

## Get PVCs

```bash
kubectl get pvc
```

Alias:

```bash
kgpvc
```

---

## Get PVCs from namespace

```bash
kubectl get pvc -n storage-lab
```

---

## Describe PV

```bash
kubectl describe pv <pv-name>
```

---

## Describe PVC

```bash
kubectl describe pvc <pvc-name> -n <namespace>
```

---

## Get StorageClasses

```bash
kubectl get storageclass
```

---

## Describe StorageClass

```bash
kubectl describe storageclass <storageclass-name>
```

---

## Get Pods

```bash
kubectl get pods -n <namespace>
```

---

## Get Pod with node information

```bash
kubectl get pods -o wide -n <namespace>
```

---

## Describe Pod

```bash
kubectl describe pod <pod-name> -n <namespace>
```

---

## Get Events

```bash
kubectl get events -n <namespace>
```

Better:

```bash
kubectl get events -n <namespace> \
  --sort-by='.lastTimestamp'
```

---

## Get YAML

```bash
kubectl get pv <pv-name> -o yaml
```

```bash
kubectl get pvc <pvc-name> -n <namespace> -o yaml
```

---

## Get all resources

```bash
kubectl get all -n <namespace>
```

---

# 20. PV/PVC YAML Examples

## Basic PV

```yaml
apiVersion: v1
kind: PersistentVolume

metadata:
  name: demo-pv

spec:

  capacity:
    storage: 5Gi

  accessModes:
    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  storageClassName: manual

  hostPath:
    path: /data/demo
    type: DirectoryOrCreate
```

---

## Basic PVC

```yaml
apiVersion: v1
kind: PersistentVolumeClaim

metadata:
  name: demo-pvc
  namespace: storage-lab

spec:

  accessModes:
    - ReadWriteOnce

  storageClassName: manual

  resources:
    requests:
      storage: 2Gi
```

---

## Pod using PVC

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: demo-pod
  namespace: storage-lab

spec:

  containers:

    - name: nginx
      image: nginx:latest

      volumeMounts:

        - name: storage
          mountPath: /usr/share/nginx/html

  volumes:

    - name: storage

      persistentVolumeClaim:
        claimName: demo-pvc
```

---

# 21. Practical Labs 1-40

---

# LAB 1 — Kubernetes Storage Environment Check

## Objective

Understand the existing Kubernetes storage environment.

## Commands

```bash
kubectl get nodes

kubectl get pv

kubectl get pvc -A

kubectl get storageclass

kubectl get pods -A
```

## Learning

Before changing a cluster, first inspect existing resources.

This is especially important in a production-like cluster.

---

# LAB 2 — Create First PV

Created a basic PV.

Example:

```text
PV:
my-pv

Capacity:
5Gi

Access:
RWO

StorageClass:
manual

Reclaim:
Retain
```

The PV used HostPath.

---

# LAB 3 — Create First PVC

Created:

```text
my-pvc
```

Request:

```text
2Gi
```

StorageClass:

```text
manual
```

The PVC became:

```text
Bound
```

---

# LAB 4 — PV to PVC Binding

Observed:

```text
PV:
Bound

PVC:
Bound
```

Learned how Kubernetes connects storage supply with storage request.

---

# LAB 5 — Mount PVC to Nginx Pod

Mounted the PVC to:

```text
/usr/share/nginx/html
```

Architecture:

```text
Nginx
 |
PVC
 |
PV
 |
HostPath
```

---

# LAB 6 — Inspect Mounted PVC

Entered the Pod:

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

Checked:

```bash
df -h
```

and:

```bash
ls -la /usr/share/nginx/html
```

---

# LAB 7 — Write Data

Example:

```bash
kubectl exec <pod-name> -- \
sh -c 'echo "Persistent Storage Test" > /usr/share/nginx/html/test.txt'
```

Verified:

```bash
kubectl exec <pod-name> -- \
cat /usr/share/nginx/html/test.txt
```

---

# LAB 8 — Verify Data on Node

Because HostPath was used:

```bash
sudo ls -la /data/k8s-storage
```

The file could be seen on the node.

---

# LAB 9 — Delete Pod and Verify Persistence

Deleted the Pod:

```bash
kubectl delete pod <pod-name>
```

After recreation:

```bash
kubectl exec <new-pod> -- \
cat /usr/share/nginx/html/test.txt
```

The data remained.

---

# LAB 10 — Recreate Pod

Repeated the test.

The same PVC was mounted by the new Pod.

---

# LAB 11 — Complete Persistence Test

The complete flow:

```text
Create PV
   ↓
Create PVC
   ↓
Create Pod
   ↓
Write data
   ↓
Delete Pod
   ↓
Recreate Pod
   ↓
Read data
```

---

# LAB 12 — PVC Smaller Than PV

Example:

```text
PV = 5Gi
PVC = 2Gi
```

This is valid if other requirements match.

---

# LAB 13 — PVC Larger Than PV

Example:

```text
PV = 5Gi
PVC = 10Gi
```

PVC remains Pending.

Reason:

```text
PV capacity < PVC request
```

---

# LAB 14 — Troubleshoot Pending PVC

Used:

```bash
kubectl get pvc
```

Then:

```bash
kubectl describe pvc <pvc>
```

Then:

```bash
kubectl get pv
```

Then:

```bash
kubectl describe pv <pv>
```

Then:

```bash
kubectl get events
```

---

# LAB 15 — Wrong StorageClass

Tested PV and PVC with different StorageClasses.

Important discovery:

A PVC using a dynamically provisioned StorageClass can create a new PV instead of binding to the manually created PV.

---

# LAB 16 — Retain Policy

Tested:

```yaml
persistentVolumeReclaimPolicy: Retain
```

After deleting PVC:

```text
PVC deleted
   ↓
PV = Released
```

Data can remain.

---

# LAB 17 — Delete Policy

Tested:

```yaml
persistentVolumeReclaimPolicy: Delete
```

Learned that exact cleanup behavior depends on the storage backend/provisioner.

---

# LAB 18 — Multiple Pods and PVC

Tested multiple Pods using persistent storage.

Learned that access mode and node placement matter.

---

# LAB 19 — RWO

Practiced:

```yaml
accessModes:
  - ReadWriteOnce
```

Learned the node-level semantics of RWO.

---

# LAB 20 — Deployment with PVC

Created a Deployment using a PVC.

Architecture:

```text
Deployment
 |
Pod
 |
PVC
 |
PV
```

---

# LAB 21 — Deployment Restart

Deleted/restarted the Pod.

The Deployment recreated it.

The PVC and data remained.

---

# LAB 22 — Scale Deployment

Practiced scaling a Deployment.

Important lesson:

> Stateful applications should not automatically be scaled like stateless applications without considering their storage architecture.

---

# LAB 23 — Inspection and Troubleshooting

Practiced:

```bash
kubectl get pv
kubectl get pvc
kubectl describe pv <pv>
kubectl describe pvc <pvc>
kubectl get pods -o wide
kubectl describe pod <pod>
kubectl get events
```

---

# LAB 24 — Find Pod Using PVC

Checked:

```bash
kubectl describe pod <pod>
```

Looked at:

```text
Volumes
```

and:

```text
ClaimName
```

---

# LAB 25 — Find PV Bound to PVC

Used:

```bash
kubectl get pvc <pvc>
```

The `VOLUME` column identifies the PV.

---

# LAB 26 — Find PVC Using PV

Used:

```bash
kubectl get pv <pv>
```

The `CLAIM` column identifies the PVC.

---

# LAB 27 — Capacity Mismatch

Tested:

```text
PV = 5Gi
PVC = 2Gi
```

and:

```text
PV = 5Gi
PVC = 10Gi
```

Learned how capacity affects binding.

---

# LAB 28 — Access Mode Mismatch

Tested incompatible access modes.

Learned:

> The PV must support the access mode requested by the PVC.

---

# LAB 29 — StorageClass Mismatch

Tested different StorageClasses.

Learned that a PVC cannot simply take an unrelated manual PV.

---

# LAB 30 — Dynamic Provisioning

Used:

```text
local-path
```

The provisioner:

```text
rancher.io/local-path
```

created storage dynamically.

---

# LAB 31 — Dynamic Provisioning Flow

Complete flow:

```text
PVC
 |
StorageClass
 |
Provisioner
 |
Dynamic PV
 |
Pod
```

---

# LAB 32 — PVC Expansion

Attempted:

```text
1Gi → 2Gi
```

The StorageClass allowed expansion, but the PVC did not immediately expand.

Observed an event similar to:

```text
ExternalExpanding:
waiting for an external controller to expand this PVC
```

Checked:

```bash
kubectl get csidrivers
```

There were no CSI drivers in the environment.

## Lesson

```text
allowVolumeExpansion
```

does not guarantee expansion.

The storage backend/controller must support it.

---

# LAB 33 — MySQL Persistent Storage

Created a MySQL persistent storage environment.

Architecture:

```text
MySQL Deployment
       |
       v
   MySQL Pod
       |
       v
    mysql-pvc
       |
       v
    mysql-pv
       |
       v
/data/mysql-lab
```

Configuration:

```text
PV = 5Gi
PVC = 2Gi
Access = RWO
Reclaim = Retain
StorageClass = mysql-manual
```

---

# LAB 34 — MySQL Persistence Verification

Created database:

```text
devops_lab
```

Table:

```text
employees
```

Example data:

```text
1 | Anish | DevOps Engineer
2 | Rahul | QA Engineer
3 | Priya | Cloud Engineer
```

Deleted the Pod.

The new Pod was able to access the same database.

---

# LAB 35 — Failure Simulation

Tested:

### Scenario 1

Delete Pod.

Result:

```text
Pod recreated
Data remains
```

### Scenario 2

Delete Deployment.

Result:

```text
Deployment deleted
Pod deleted
PVC remains
PV remains
```

### Scenario 3

Delete PVC.

With Retain:

```text
PVC deleted
PV = Released
```

### Scenario 4

Verify underlying storage.

Data can remain on the HostPath.

---

# LAB 36 — PVC Larger Than PV

## Scenario

```text
PV = 5Gi

PVC = 10Gi
```

PVC:

```text
Pending
```

Pod:

```text
Pending
```

Important event:

```text
0/1 nodes are available:
1 node(s) didn't find available persistent volumes to bind
```

## Root Cause

```text
Requested = 10Gi

Available = 5Gi
```

No suitable PV exists.

## Important Learning

The presence of:

```text
WaitForFirstConsumer
```

does not automatically mean it is the root cause.

Always read the actual error/event.

---

# LAB 37 — StorageClass Mismatch

## Intended Setup

```text
PV:
StorageClass = manual

PVC:
StorageClass = fast
```

Expected:

```text
PVC Pending
```

But the cluster did not have the expected `fast` StorageClass.

The PVC eventually used:

```text
local-path
```

and Kubernetes dynamically created another PV.

The manually created PV remained:

```text
Available
```

This was a very important lesson.

---

## What Actually Happened

```text
lab37-pv
   |
   +-- StorageClass = manual
   |
   +-- Status = Available
```

PVC:

```text
lab37-pvc
   |
   +-- StorageClass = local-path
   |
   +-- Status = Bound
```

Dynamic PV:

```text
pvc-5887bed7-1cde-446f-b1d6-3e285b09d706
```

was created.

---

## Lesson

Different StorageClasses do not mean the PVC can use any PV.

But a dynamic StorageClass can create another PV.

---

# LAB 38 — Reclaim Policy

Created a separate storage lab using:

```text
lab38-storage
```

PV:

```text
lab38-pv
```

Storage:

```text
/data/lab38
```

Tested:

```text
Delete
```

reclaim behavior.

Flow:

```text
PV
 ↓
PVC
 ↓
Pod
 ↓
Write data
 ↓
Delete PVC
 ↓
Inspect PV
 ↓
Inspect backend
```

---

# LAB 39 — PVC Bound but Pod Pending

This was an important troubleshooting lab.

Storage:

```text
PV = Bound
PVC = Bound
```

But:

```text
Pod = Pending
```

The Pod had:

```yaml
nodeSelector:
  kubernetes.io/hostname: nonexistent-node
```

No node had that label.

Therefore the Pod could not be scheduled.

---

## Troubleshooting

```bash
kubectl describe pod lab39-pod \
  -n troubleshooting-lab
```

Also:

```bash
kubectl get nodes --show-labels
```

## Lesson

```text
PVC Bound
```

does not guarantee:

```text
Pod Running
```

Storage binding and Pod scheduling are separate processes.

---

# LAB 40 — Final Nginx + MySQL Project

The final project combined the major concepts.

Architecture:

```text
                  Kubernetes Cluster
                         |
              +----------+----------+
              |                     |
            Nginx                 MySQL
              |                     |
           nginx-pvc             mysql-pvc
              |                     |
           nginx-pv              mysql-pv
              |                     |
      Persistent Storage    Persistent Storage
```

Namespace:

```text
pv-pvc-final
```

---

# Nginx Configuration

PV:

```text
lab40-nginx-pv
```

Capacity:

```text
2Gi
```

PVC:

```text
lab40-nginx-pvc
```

Request:

```text
1Gi
```

StorageClass:

```text
lab40-nginx
```

Reclaim:

```text
Retain
```

HostPath:

```text
/data/lab40-nginx
```

---

# MySQL Configuration

PV:

```text
lab40-mysql-pv
```

Capacity:

```text
5Gi
```

PVC:

```text
lab40-mysql-pvc
```

Request:

```text
3Gi
```

StorageClass:

```text
lab40-mysql
```

Reclaim:

```text
Retain
```

HostPath:

```text
/data/lab40-mysql
```

---

# Nginx Persistent HTML

Nginx mounted:

```text
/usr/share/nginx/html
```

to the PVC.

Architecture:

```text
Nginx
 |
/usr/share/nginx/html
 |
PVC
 |
PV
 |
/data/lab40-nginx
```

A custom `index.html` was stored there.

---

# MySQL Persistent Database

MySQL mounted:

```text
/var/lib/mysql
```

to:

```text
mysql-pvc
```

Database:

```text
devops_final
```

Table:

```text
employees
```

Records:

```text
1 | Anish | DevOps Engineer
2 | Rahul | QA Engineer
3 | Priya | Cloud Engineer
```

---

# Final Persistence Test

## Step 1

Create all resources.

```text
PV
 ↓
PVC
 ↓
Deployment
 ↓
Pod
```

---

## Step 2

Write data.

Nginx:

```text
index.html
```

MySQL:

```text
database
table
records
```

---

## Step 3

Delete Pod.

```text
Pod deleted
       |
       v
Deployment recreates Pod
       |
       v
PVC mounted
       |
       v
PV mounted
       |
       v
Data available
```

---

## Step 4

Delete Deployment.

```text
Deployment deleted
       |
       v
Pod deleted
       |
       v
PVC remains
       |
       v
PV remains
```

---

## Step 5

Recreate Deployment.

The new Pod mounts the existing PVC.

Data should still exist.

---

## Step 6

Delete PVC.

Because the PV uses:

```text
Retain
```

the PV can become:

```text
Released
```

The underlying HostPath data can remain.

---

# 22. Important Issues I Faced

This section is especially important because these were not just theoretical examples.

They were real troubleshooting situations during my practical work.

---

# Issue 1 — PVC Pending Because Requested Capacity Was Too Large

Situation:

```text
PV = 5Gi
PVC = 10Gi
```

PVC:

```text
Pending
```

Pod:

```text
Pending
```

## Investigation

```bash
kubectl describe pvc lab36-pvc \
  -n troubleshooting-lab
```

Then:

```bash
kubectl describe pod lab36-pod \
  -n troubleshooting-lab
```

The scheduler reported:

```text
didn't find available persistent volumes to bind
```

## Solution

Either:

```text
Increase PV capacity
```

or:

```text
Decrease PVC request
```

---

# Issue 2 — StorageClass Mismatch

Situation:

```text
PV = manual
PVC = different StorageClass
```

Expected the PVC to use the manual PV.

It did not.

## Actual behavior

The PVC used:

```text
local-path
```

and a dynamic PV was created.

## Learning

Always check:

```bash
kubectl get storageclass
```

and:

```bash
kubectl get pv
kubectl get pvc
```

---

# Issue 3 — WaitForFirstConsumer Confusion

At first, seeing:

```text
WaitForFirstConsumer
```

could look like the main problem.

But in LAB 36, the actual issue was:

```text
PV = 5Gi
PVC = 10Gi
```

The scheduler could not find a suitable PV.

## Learning

Never diagnose from one event line only.

Read the complete event history.

---

# Issue 4 — PVC Bound but Pod Pending

Storage was correct:

```text
PV = Bound
PVC = Bound
```

But Pod was:

```text
Pending
```

The actual problem was an invalid node selector.

## Learning

Check Pod scheduling separately.

---

# Issue 5 — PVC Expansion Did Not Complete

The StorageClass had:

```text
allowVolumeExpansion: true
```

but expansion remained pending.

The cluster had no CSI drivers.

## Learning

The complete chain matters:

```text
PVC
 |
StorageClass
 |
Provisioner/CSI
 |
Backend
```

A setting alone does not guarantee backend functionality.

---

# Issue 6 — PV Fields Are Not Always Editable

Attempting to change certain PV source details after creation can result in immutable field errors.

For labs, it is often safer to recreate the test PV when appropriate.

For production:

> Never delete/recreate storage blindly. First understand the data lifecycle and backup state.

---

# 23. Troubleshooting Methodology

My general troubleshooting process became:

---

## Step 1 — Check the resource

```bash
kubectl get pv
kubectl get pvc -n <namespace>
kubectl get pods -n <namespace>
```

---

## Step 2 — Describe it

```bash
kubectl describe pvc <pvc> -n <namespace>
```

or:

```bash
kubectl describe pod <pod> -n <namespace>
```

---

## Step 3 — Read Events

```bash
kubectl get events -n <namespace> \
  --sort-by='.lastTimestamp'
```

---

## Step 4 — Check StorageClass

```bash
kubectl get storageclass
```

---

## Step 5 — Check PV

```bash
kubectl get pv
```

---

## Step 6 — Check capacity

Compare:

```text
PV capacity
```

with:

```text
PVC requested capacity
```

---

## Step 7 — Check access mode

Compare:

```text
PV accessModes
```

with:

```text
PVC accessModes
```

---

## Step 8 — Check scheduling

If PVC is Bound but Pod is Pending:

```bash
kubectl describe pod <pod> -n <namespace>
```

Look for:

```text
FailedScheduling
```

---

# 24. Nginx Persistent Storage

Nginx is a simple way to demonstrate persistent storage.

Architecture:

```text
Browser
   |
   v
Nginx Pod
   |
   v
/usr/share/nginx/html
   |
   v
PVC
   |
   v
PV
   |
   v
HostPath
```

The important point is that HTML content is stored on persistent storage.

---

# 25. MySQL Persistent Storage

MySQL is a more realistic stateful application.

Architecture:

```text
Application
    |
    v
MySQL Pod
    |
    v
/var/lib/mysql
    |
    v
PVC
    |
    v
PV
    |
    v
Persistent Storage
```

If the Pod is recreated:

```text
Old MySQL Pod
      X
      |
      v
New MySQL Pod
      |
      v
Same PVC
      |
      v
Same PV
      |
      v
Same database
```

---

# 26. Final Nginx + MySQL Project

The final project demonstrated two different application types.

## Nginx

Mostly stateless application logic with persistent website content.

```text
Nginx
 |
PVC
 |
PV
 |
HTML
```

## MySQL

Stateful database workload.

```text
MySQL
 |
PVC
 |
PV
 |
Database files
```

---

# Final Architecture

```text
                         Kubernetes
                             |
            +----------------+----------------+
            |                                 |
          Nginx                              MySQL
            |                                 |
       nginx-pvc                           mysql-pvc
            |                                 |
       nginx-pv                            mysql-pv
            |                                 |
   /data/lab40-nginx              /data/lab40-mysql
            |                                 |
       HTML content                    Database content
```

---

# 27. Real-World DevOps Use Cases

## 27.1 MySQL

```text
MySQL
 |
PVC
 |
Persistent Storage
```

Database data should survive Pod recreation.

---

## 27.2 PostgreSQL

Same concept:

```text
PostgreSQL
 |
PVC
 |
Persistent Storage
```

---

## 27.3 Application Uploads

Example:

```text
Django
 |
/media
 |
PVC
```

User-uploaded files survive Pod recreation.

---

## 27.4 Static Website

```text
Nginx
 |
HTML
 |
PVC
```

---

## 27.5 Reports

Applications generating reports can store them on persistent storage.

---

## 27.6 Media

Images/videos can use persistent storage.

For large production workloads, object storage is often a better architecture.

---

## 27.7 CI/CD

Persistent storage can be used for build artifacts, caches, or workspaces when required by the CI architecture.

---

# 28. Production Considerations

The labs used:

```text
HostPath
```

because it is simple.

Production environments often use:

```text
Cloud block storage
Cloud file storage
NFS
Ceph
Longhorn
SAN
NAS
CSI-based storage
```

---

# CSI

CSI means:

> Container Storage Interface

CSI allows Kubernetes to interact with external storage systems through standardized drivers.

Production environments commonly depend on CSI drivers for:

- provisioning
- attaching
- mounting
- snapshots
- expansion
- cloning

---

# HostPath Production Problem

Suppose:

```text
Pod
 |
server-1
 |
/data/application
```

If the Pod is rescheduled to:

```text
server-2
```

then:

```text
server-2:/data/application
```

may not contain the same data.

Therefore HostPath is not automatically shared storage.

---

# Production Storage Should Consider

- High availability
- Backup
- Disaster recovery
- Replication
- Encryption
- Performance
- IOPS
- Capacity
- Expansion
- Monitoring
- Security
- Access control
- Recovery time objective (RTO)
- Recovery point objective (RPO)

---

# 29. Common Mistakes

## Mistake 1

Thinking:

```text
PVC = physical disk
```

Incorrect.

PVC is a storage request.

---

## Mistake 2

Thinking:

```text
PV = backup
```

Incorrect.

---

## Mistake 3

Thinking:

```text
Retain = backup
```

Incorrect.

---

## Mistake 4

Thinking:

```text
RWO = exactly one Pod
```

Too simplistic.

RWO primarily means read-write access from one node.

---

## Mistake 5

Ignoring StorageClass.

Always check:

```bash
kubectl get storageclass
```

---

## Mistake 6

Ignoring Events.

Use:

```bash
kubectl describe pvc
```

and:

```bash
kubectl describe pod
```

---

## Mistake 7

Assuming Bound PVC means Pod will run.

Pod scheduling can still fail.

---

## Mistake 8

Assuming `allowVolumeExpansion` guarantees expansion.

The backend must support it.

---

# 30. Troubleshooting Decision Tree

## PVC Pending

```text
PVC Pending
     |
     v
kubectl describe pvc
     |
     +---- Capacity issue?
     |          |
     |          +---- Check PV capacity
     |
     +---- StorageClass issue?
     |          |
     |          +---- Check StorageClass
     |
     +---- WaitForFirstConsumer?
     |          |
     |          +---- Check consuming Pod
     |
     +---- Provisioning failure?
                |
                +---- Check provisioner
```

---

## Pod Pending

```text
Pod Pending
     |
     v
kubectl describe pod
     |
     +---- FailedScheduling?
     |          |
     |          +---- Check node/scheduling
     |
     +---- Volume issue?
     |
     +---- CPU/memory issue?
     |
     +---- Node selector?
     |
     +---- Affinity?
     |
     +---- Taint/toleration?
```

---

# 31. Interview Questions

## Q1. What is PV?

PV is a Kubernetes resource representing persistent storage available to the cluster.

---

## Q2. What is PVC?

PVC is a request for persistent storage made by an application/workload.

---

## Q3. PV vs PVC?

Simple answer:

```text
PV = storage supply

PVC = storage request
```

---

## Q4. What is StorageClass?

StorageClass defines a category of storage and how storage should be provisioned.

---

## Q5. What is dynamic provisioning?

Automatic creation/provisioning of storage when a PVC requests a StorageClass supported by a provisioner.

---

## Q6. What is static provisioning?

Administrator manually creates PVs.

---

## Q7. What is RWO?

ReadWriteOnce.

The volume can be mounted read-write from one node.

---

## Q8. What is RWX?

ReadWriteMany.

The volume can be mounted read-write from multiple nodes if supported by the backend.

---

## Q9. What is Retain?

The PV/data is retained after PVC deletion according to the storage backend lifecycle.

---

## Q10. Is Retain a backup?

No.

---

## Q11. Why is PVC Pending?

Possible reasons:

- insufficient capacity
- StorageClass mismatch
- StorageClass doesn't exist
- no suitable PV
- provisioner failure
- access mode mismatch
- selector mismatch
- topology constraints

---

## Q12. Why is Pod Pending while PVC is Bound?

Because storage binding and Pod scheduling are different operations.

The Pod may have:

- node selector problem
- affinity problem
- taint problem
- insufficient CPU/memory
- storage topology problem

---

## Q13. What is WaitForFirstConsumer?

It delays volume binding/provisioning until a Pod using the PVC is being scheduled.

---

## Q14. What happens when Pod is deleted?

Usually:

```text
Pod deleted
PVC remains
PV remains
Data remains
```

assuming the storage lifecycle has not separately caused deletion.

---

## Q15. What happens when Deployment is deleted?

Deployment and managed Pods are deleted.

PVC is not automatically deleted just because the Deployment was deleted.

---

## Q16. What happens when PVC is deleted?

Depends on reclaim policy.

For Retain:

```text
PVC deleted
PV becomes Released
```

---

## Q17. Can 5Gi PV satisfy 10Gi PVC?

No.

---

## Q18. Can 5Gi PV satisfy 2Gi PVC?

Yes, assuming all other requirements match.

---

## Q19. Why did my manual PV remain Available while PVC became Bound?

Because the PVC used a different dynamic StorageClass and Kubernetes provisioned another PV.

---

## Q20. What is HostPath?

HostPath mounts a node filesystem directory into a Pod.

---

## Q21. Why is HostPath not ideal for production?

Because data is tied to a node and is not automatically distributed or replicated.

---

## Q22. What is CSI?

Container Storage Interface.

It provides a standardized interface between Kubernetes and storage systems.

---

# 32. Important Commands Cheat Sheet

## PV

```bash
kubectl get pv

kubectl describe pv <pv-name>

kubectl get pv <pv-name> -o yaml
```

---

## PVC

```bash
kubectl get pvc

kubectl get pvc -n <namespace>

kubectl describe pvc <pvc> -n <namespace>

kubectl get pvc <pvc> -n <namespace> -o yaml
```

---

## StorageClass

```bash
kubectl get storageclass

kubectl describe storageclass <name>

kubectl get storageclass <name> -o yaml
```

---

## Pods

```bash
kubectl get pods -n <namespace>

kubectl get pods -o wide -n <namespace>

kubectl describe pod <pod> -n <namespace>
```

---

## Events

```bash
kubectl get events -n <namespace>
```

Better:

```bash
kubectl get events \
  -n <namespace> \
  --sort-by='.lastTimestamp'
```

---

## Storage drivers

```bash
kubectl get csidrivers
```

---

## Execute inside Pod

```bash
kubectl exec -it <pod> -n <namespace> -- /bin/bash
```

or:

```bash
kubectl exec -it <pod> -n <namespace> -- /bin/sh
```

---

## Check mounted filesystem

```bash
kubectl exec <pod> -n <namespace> -- df -h
```

---

## Check mount

```bash
kubectl exec <pod> -n <namespace> -- mount
```

---

# 33. What I Implemented

During the PV/PVC learning journey, I implemented:

## Kubernetes Storage

- PV creation
- PVC creation
- PV/PVC binding
- StorageClass
- Static provisioning
- Dynamic provisioning
- HostPath
- RWO
- Filesystem volumes

## Persistence

- Write data
- Verify data
- Delete Pod
- Recreate Pod
- Restart Deployment
- Verify persistence

## Troubleshooting

- Pending PVC
- Pending Pod
- Capacity mismatch
- Access mode mismatch
- StorageClass mismatch
- Dynamic provisioning
- `WaitForFirstConsumer`
- PVC expansion
- Scheduler errors
- Reclaim policy

## Application Storage

- Nginx persistent HTML
- MySQL persistent database

## Failure Testing

- Pod deletion
- Deployment deletion
- PVC deletion
- PV Released state
- Retain behavior

---

# 34. What I Learned

The most important lessons from these practicals are:

### 1. Pod lifecycle and storage lifecycle are different

```text
Pod can disappear
Storage can remain
```

---

### 2. PVC is an abstraction

Applications request storage through PVC.

---

### 3. PV represents available storage

PV is the storage resource.

---

### 4. StorageClass controls provisioning

StorageClass determines how storage should be provisioned.

---

### 5. Dynamic provisioning reduces manual work

```text
PVC
 |
StorageClass
 |
Provisioner
 |
PV
```

---

### 6. Events are extremely important

When something is Pending:

```bash
kubectl describe ...
```

is one of the first commands I should run.

---

### 7. Bound PVC does not mean Running Pod

There are separate processes:

```text
Storage Binding
```

and:

```text
Pod Scheduling
```

---

### 8. Retain is not backup

Backups and disaster recovery are separate responsibilities.

---

### 9. HostPath is mainly useful for local learning/testing

Production systems generally require better storage architectures.

---

### 10. Storage backend matters

Kubernetes storage behavior depends heavily on the underlying backend/provisioner.

---

# 35. Final Summary

The simplest way to remember Kubernetes persistent storage is:

```text
PV
=
Storage Supply
```

```text
PVC
=
Storage Request
```

```text
StorageClass
=
Storage Type / Provisioning Rules
```

```text
Provisioner
=
Component That Provides/Creates Storage
```

The basic relationship is:

```text
Pod
 |
PVC
 |
PV
 |
Storage
```

Dynamic provisioning adds:

```text
Pod
 |
PVC
 |
StorageClass
 |
Provisioner
 |
PV
 |
Storage
```

---

# Complete Persistence Flow

```text
                Application
                     |
                     v
                    Pod
                     |
                     v
                    PVC
                     |
                     v
               StorageClass
                     |
                     v
                Provisioner
                     |
                     v
                    PV
                     |
                     v
             Storage Backend
```

---

# Failure Flow

Example:

```text
PVC requests 10Gi
        |
        v
PV has 5Gi
        |
        v
No suitable PV
        |
        v
PVC Pending
        |
        v
Pod cannot be scheduled
```

---

# Successful Flow

```text
PVC requests 2Gi
        |
        v
PV has 5Gi
        |
        v
Requirements match
        |
        v
PVC Bound
        |
        v
Pod scheduled
        |
        v
Pod Running
        |
        v
Data stored persistently
```

---

# Persistence Flow

```text
Pod 1
  |
  v
PVC
  |
  v
PV
  |
  v
Data

Pod 1 deleted
  |
  X

Pod 2
  |
  v
Same PVC
  |
  v
Same PV
  |
  v
Same Data
```

---

# Final Project Flow

```text
              Kubernetes Cluster
                     |
          +----------+----------+
          |                     |
        Nginx                  MySQL
          |                     |
      nginx-pvc             mysql-pvc
          |                     |
      nginx-pv              mysql-pv
          |                     |
      HTML data            DB data
```

Test:

```text
Create
  ↓
Write data
  ↓
Delete Pod
  ↓
Pod recreated
  ↓
Verify data
  ↓
Delete Deployment
  ↓
Recreate Deployment
  ↓
Verify data
  ↓
Delete PVC
  ↓
Inspect PV
  ↓
Understand reclaim policy
```

---

# Final Interview Statement

> Kubernetes PersistentVolume (PV) represents persistent storage available to the cluster, while PersistentVolumeClaim (PVC) represents an application's request for storage. A StorageClass defines how storage should be provisioned, and a provisioner can dynamically create the required PV. Pods consume storage through PVCs, allowing application data to survive Pod/container lifecycle changes.

---

# Final Checklist

Before considering Kubernetes PV/PVC fundamentals complete:

- [x] Understand PV
- [x] Understand PVC
- [x] Understand StorageClass
- [x] Understand Provisioner
- [x] Understand static provisioning
- [x] Understand dynamic provisioning
- [x] Understand PV/PVC binding
- [x] Understand capacity matching
- [x] Understand access modes
- [x] Understand volume modes
- [x] Understand reclaim policies
- [x] Understand Retain
- [x] Understand Delete
- [x] Understand `WaitForFirstConsumer`
- [x] Understand HostPath
- [x] Create PV
- [x] Create PVC
- [x] Mount PVC to Pod
- [x] Write persistent data
- [x] Verify data
- [x] Delete Pod
- [x] Recreate Pod
- [x] Test Deployment
- [x] Test MySQL persistence
- [x] Test Nginx persistence
- [x] Troubleshoot Pending PVC
- [x] Troubleshoot Pending Pod
- [x] Troubleshoot capacity mismatch
- [x] Troubleshoot StorageClass mismatch
- [x] Understand dynamic provisioning
- [x] Test reclaim policy
- [x] Understand PVC expansion limitations
- [x] Complete final Nginx + MySQL project

---

# Next-Level Kubernetes Storage Topics

After completing these fundamentals, the next topics to practice are:

1. CSI architecture
2. CSI drivers
3. VolumeSnapshots
4. Volume cloning
5. StatefulSets
6. StatefulSet + PVC
7. Headless Services
8. NFS storage
9. Longhorn
10. Ceph
11. Cloud persistent disks
12. RWX storage
13. Storage topology
14. Storage monitoring
15. Backup and restore
16. Velero
17. Database backup
18. Disaster recovery
19. Multi-node storage
20. Production storage architecture

---

# Conclusion

This PV/PVC practical journey helped me understand that Kubernetes storage is not just about creating a PV and PVC.

The complete picture is:

```text
Application
     |
     v
    Pod
     |
     v
    PVC
     |
     v
StorageClass
     |
     v
Provisioner
     |
     v
    PV
     |
     v
Storage Backend
```

The most important practical lesson is:

> **When a Kubernetes storage problem occurs, do not guess. Check the PV, PVC, StorageClass, Pod, and Events one by one and identify the actual root cause.**

The most important commands are:

```bash
kubectl get pv
kubectl get pvc -A
kubectl get storageclass
kubectl describe pv <pv>
kubectl describe pvc <pvc> -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

This completes my foundational Kubernetes **Persistent Volumes and Persistent Volume Claims** theory, practical implementation, troubleshooting, and project work.
