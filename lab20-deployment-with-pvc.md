# Lab 20 — Deployment with PVC

## 1. Objective

Move from a standalone Pod to a Deployment while keeping persistent storage.

## 2. Architecture

```text
Deployment
    |
    v
Pod
    |
    v
PVC
    |
    v
PV
    |
    v
Storage
```

## 3. Example Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-storage
  namespace: storage-lab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-storage
  template:
    metadata:
      labels:
        app: nginx-storage
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
            claimName: storage-lab-pvc
```

Apply:

```bash
kubectl apply -f deployment.yaml
```

## 4. Verify

```bash
kubectl get deployment -n storage-lab
kubectl get pods -n storage-lab
kubectl get pvc -n storage-lab
kubectl get pv
```

## 5. Issue encountered

The Deployment was initially created without a namespace and therefore created in `default`.

The Pod reported:

```text
persistentvolumeclaim "storage-lab-pvc" not found
```

## 6. Root cause

PVCs are namespaced.

The Pod was in:

```text
default
```

The PVC was in:

```text
storage-lab
```

A Pod cannot consume a PVC from another namespace.

## 7. Resolution

Add:

```yaml
metadata:
  namespace: storage-lab
```

to the Deployment and recreate/apply it.

## 8. Real-world use case

Most production applications are managed by Deployments, StatefulSets, or Operators rather than standalone Pods.

## 9. Interview takeaway

PV is cluster-scoped. Deployment/Pod/PVC are namespace-scoped. The Pod and PVC must be in the same namespace.


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

