# Kubernetes PV/PVC Practical Labs — Lab 1 to Lab 32

This repository contains detailed hands-on documentation for 32 Kubernetes storage labs.

## Lab Index

- [Lab 1 — Kubernetes Storage Environment Check](./lab1-kubernetes-storage-environment-check.md)
- [Lab 2 — Create Your First PersistentVolume (PV)](./lab2-create-first-persistentvolume.md)
- [Lab 3 — Create Your First PersistentVolumeClaim (PVC)](./lab3-create-first-persistentvolumeclaim.md)
- [Lab 4 — Understand PV ↔ PVC Binding](./lab4-understand-pv-pvc-binding.md)
- [Lab 5 — Mount PVC to an Nginx Pod](./lab5-mount-pvc-to-nginx-pod.md)
- [Lab 6 — Access and Inspect Mounted PVC Inside Pod](./lab6-access-inspect-mounted-pvc.md)
- [Lab 7 — Write Data to Persistent Storage](./lab7-write-data-to-persistent-storage.md)
- [Lab 8 — Verify Persistent Data from Kubernetes Node](./lab8-verify-persistent-data-from-node.md)
- [Lab 9 — Delete Pod and Verify Data Persistence](./lab9-delete-pod-verify-data-persistence.md)
- [Lab 10 — Recreate Pod and Verify Persistent Data](./lab10-recreate-pod-verify-persistent-data.md)
- [Lab 11 — Complete PVC Data Persistence Test](./lab11-complete-pvc-data-persistence-test.md)
- [Lab 12 — PVC Smaller Than PV](./lab12-pvc-smaller-than-pv.md)
- [Lab 13 — PVC Larger Than PV — Pending Scenario](./lab13-pvc-larger-than-pv-pending.md)
- [Lab 14 — Troubleshoot Pending PVC](./lab14-troubleshoot-pending-pvc.md)
- [Lab 15 — PVC with Wrong StorageClass](./lab15-pvc-wrong-storageclass.md)
- [Lab 16 — Reclaim Policy: Retain](./lab16-reclaim-policy-retain.md)
- [Lab 17 — Reclaim Policy: Delete](./lab17-reclaim-policy-delete.md)
- [Lab 18 — Multiple Pods Using One PVC](./lab18-multiple-pods-one-pvc.md)
- [Lab 19 — ReadWriteOnce (RWO) Practical](./lab19-readwriteonce-rwo-practical.md)
- [Lab 20 — Deployment with PVC](./lab20-deployment-with-pvc.md)
- [Lab 21 — Deployment Restart and Data Persistence](./lab21-deployment-restart-data-persistence.md)
- [Lab 22 — Scale Deployment with PVC](./lab22-scale-deployment-with-pvc.md)
- [Lab 23 — PV, PVC and Pod Inspection & Troubleshooting Commands](./lab23-pv-pvc-pod-inspection-troubleshooting.md)
- [Lab 24 — Find Which Pod Is Using a PVC](./lab24-find-pod-using-pvc.md)
- [Lab 25 — Find Which PV Is Bound to a PVC](./lab25-find-pv-bound-to-pvc.md)
- [Lab 26 — Find Which PVC Is Using a PV](./lab26-find-pvc-using-pv.md)
- [Lab 27 — PVC Capacity Mismatch Troubleshooting](./lab27-pvc-capacity-mismatch-troubleshooting.md)
- [Lab 28 — Access Mode Mismatch Troubleshooting](./lab28-access-mode-mismatch-troubleshooting.md)
- [Lab 29 — StorageClass Mismatch Troubleshooting](./lab29-storageclass-mismatch-troubleshooting.md)
- [Lab 30 — Dynamic Provisioning with StorageClass](./lab30-dynamic-provisioning-with-storageclass.md)
- [Lab 31 — Understand Dynamic Provisioning Flow](./lab31-understand-dynamic-provisioning-flow.md)
- [Lab 32 — PVC Storage Expansion](./lab32-pvc-storage-expansion.md)

## Learning progression

```text
Environment
   ↓
PV
   ↓
PVC
   ↓
Binding
   ↓
Pod Mount
   ↓
Write / Read
   ↓
Persistence
   ↓
Capacity / Access Mode Troubleshooting
   ↓
Reclaim Policies
   ↓
Deployments / Scaling
   ↓
Inspection / Debugging
   ↓
Dynamic Provisioning
   ↓
Dynamic Provisioning Architecture
   ↓
PVC Expansion
```

## Lab safety

These are learning labs. Keep destructive experiments isolated.

Do not delete or modify production PVs/PVCs simply to reproduce a lab issue.

## Core Kubernetes storage model

```text
Pod
 |
 v
PVC
 |
 v
PV
 |
 v
Storage Backend
```

For dynamic provisioning:

```text
Pod
 |
 v
PVC
 |
 v
StorageClass
 |
 v
Provisioner / CSI
 |
 v
PV
 |
 v
Storage Backend
```

## Important lessons from the actual practice

- PVs are cluster-scoped.
- PVCs are namespaced.
- Pod and PVC must be in the same namespace.
- RWO is node-level read-write attachment semantics.
- `WaitForFirstConsumer` is not the same thing as dynamic provisioning.
- `kubernetes.io/no-provisioner` means a StorageClass does not dynamically provision storage.
- `local-path` can dynamically create local PVs through the Rancher local-path provisioner.
- PVC specification fields such as StorageClass cannot simply be changed after creation.
- `allowVolumeExpansion: true` permits expansion but does not guarantee backend support.
- A PVC can be `Bound` while application-level data safety still requires application-aware design.
- Persistence is different from high availability.
- HostPath is node-local and should not be treated as shared enterprise storage.
