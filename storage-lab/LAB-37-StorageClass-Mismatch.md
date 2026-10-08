# LAB 37 — PV/PVC StorageClass Mismatch and Dynamic Provisioning

## Objective
Understand what happens when a PV and PVC use different StorageClasses, especially when the PVC's class has a dynamic provisioner.

## Intended scenario
```text
PV  -> StorageClass A (manual)
PVC -> StorageClass B (fast)
```
The PVC cannot directly bind to the existing PV because the StorageClasses differ.

## What actually happened in the lab
The PVC eventually showed `StorageClass: local-path` and became Bound to:

```text
pvc-5887bed7-1cde-446f-b1d6-3e285b09d706
```

while `lab37-pv` remained:

```text
5Gi  Available  manual
```

Events showed:

```text
ProvisioningFailed: storageclass.storage.k8s.io "fast" not found
ExternalProvisioning: ... rancher.io/local-path
ProvisioningSucceeded: Successfully provisioned volume ...
```

## Investigation commands
```bash
kubectl get pvc lab37-pvc -n troubleshooting-lab
kubectl describe pvc lab37-pvc -n troubleshooting-lab
kubectl get pv
kubectl get pv pvc-5887bed7-1cde-446f-b1d6-3e285b09d706
kubectl get events -n troubleshooting-lab
kubectl get storageclass
```

## Why did the Pod run?
It did **not** use `lab37-pv`. The `local-path` StorageClass has the provisioner `rancher.io/local-path`, so Kubernetes dynamically created a new PV for the PVC.

Actual flow:

```text
PVC (local-path)
      ↓
local-path provisioner
      ↓
new PV
      ↓
PVC Bound
      ↓
Pod Running
```

The manually created `lab37-pv` stayed `Available` because its class was `manual`.

## Pure mismatch test
If you want a clean failure:

```text
PV = manual
PVC = another existing class
```

and ensure the PVC's class has no dynamic provisioner capable of creating a volume. Then the PVC stays Pending because no existing PV matches and no new PV is provisioned.

## Important rule
A StorageClass mismatch prevents the PVC from binding to **that particular PV**. It does not necessarily prevent the PVC from becoming Bound through dynamic provisioning.

## Troubleshooting lesson
Never conclude `StorageClass mismatch = Pod always Pending`. First check:

```bash
kubectl get pvc
kubectl describe pvc
kubectl get pv
kubectl get storageclass
kubectl get events
```

## Interview takeaway
If PV uses `manual` and PVC uses `local-path`, they do not directly bind. The PVC may still get a new dynamically provisioned PV if `local-path` has a working provisioner.
