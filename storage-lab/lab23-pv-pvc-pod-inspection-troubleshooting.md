# Lab 23 — PV, PVC and Pod Inspection & Troubleshooting Commands

## 1. Objective

Build a reusable command toolkit for Kubernetes storage troubleshooting.

## 2. PV commands

List:

```bash
kubectl get pv
```

Wide:

```bash
kubectl get pv -o wide
```

Describe:

```bash
kubectl describe pv <pv-name>
```

YAML:

```bash
kubectl get pv <pv-name> -o yaml
```

## 3. PVC commands

```bash
kubectl get pvc -n <namespace>
kubectl get pvc -n <namespace> -o wide
kubectl describe pvc <pvc-name> -n <namespace>
kubectl get pvc <pvc-name> -n <namespace> -o yaml
```

## 4. Pod commands

```bash
kubectl get pods -n <namespace>
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
kubectl get pod <pod-name> -n <namespace> -o yaml
```

## 5. StorageClass

```bash
kubectl get storageclass
kubectl get sc -o wide
kubectl describe sc <storageclass>
kubectl get sc <storageclass> -o yaml
```

## 6. Events

```bash
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

This is one of the most useful troubleshooting commands.

## 7. Inspect mounts

```bash
kubectl exec <pod> -n <namespace> -- df -h
kubectl exec <pod> -n <namespace> -- mount
kubectl exec <pod> -n <namespace> -- ls -lah <mount-path>
```

## 8. Useful JSONPath

PVC requested capacity:

```bash
kubectl get pvc <pvc> -n <ns> -o jsonpath='{.spec.resources.requests.storage}{{"\n"}}'
```

PVC bound PV:

```bash
kubectl get pvc <pvc> -n <ns> -o jsonpath='{.spec.volumeName}{{"\n"}}'
```

PV claim:

```bash
kubectl get pv <pv> -o jsonpath='{.spec.claimRef.namespace}/{.spec.claimRef.name}{{"\n"}}'
```

## 9. Troubleshooting order

Use:

```text
PVC status
   ↓
PVC Events
   ↓
PV compatibility
   ↓
StorageClass
   ↓
Provisioner/CSI
   ↓
Pod Events
   ↓
Node/storage backend
```

## 10. Interview takeaway

`kubectl describe` plus Events often provides the fastest route to the root cause.


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

