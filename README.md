# Kubernetes PV/PVC Labs 36–40

| Lab | Topic | Main lesson |
|---|---|---|
| 36 | PVC larger than PV | Capacity mismatch |
| 37 | StorageClass mismatch | Static vs dynamic provisioning |
| 38 | Reclaim policy | Retain/Delete lifecycle |
| 39 | PVC Bound, Pod Pending | Storage binding vs Pod scheduling |
| 40 | Final mini project | Nginx + MySQL persistent storage |

## Standard troubleshooting flow

```text
Observe
  ↓
get status
  ↓
describe resource
  ↓
read Events
  ↓
compare related resources
  ↓
identify root cause
  ↓
change one thing
  ↓
verify
```

## Useful commands

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl get pvc -n <namespace>
kubectl describe pvc <pvc> -n <namespace>
kubectl get pv
kubectl describe pv <pv>
kubectl get storageclass
kubectl describe storageclass <sc>
kubectl get events -n <namespace>
```

## Safety

Before destructive operations:

```bash
kubectl config current-context
kubectl get pv
kubectl get pvc -A
```

Do not use broad destructive commands on a real cluster:

```bash
kubectl delete pv --all
kubectl delete pvc --all -A
```

Always verify namespace, resource name, and ownership before deleting storage.
