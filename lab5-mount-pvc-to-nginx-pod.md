# Lab 5 — Mount PVC to an Nginx Pod

## 1. Objective

Use a PVC from a Pod and mount the persistent storage into Nginx.

## 2. Why Nginx?

Nginx is simple to inspect and provides an easy way to prove that a directory is mounted.

## 3. Pod manifest

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-storage
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
        claimName: storage-lab-pvc
```

Apply:

```bash
kubectl apply -f pod.yaml
```

## 4. Verify

```bash
kubectl get pods -n storage-lab
kubectl describe pod nginx-storage -n storage-lab
```

Check the mount:

```bash
kubectl exec nginx-storage -n storage-lab -- df -h
kubectl exec nginx-storage -n storage-lab -- mount
kubectl exec nginx-storage -n storage-lab -- ls -la /usr/share/nginx/html
```

## 5. Critical namespace rule

The Pod and PVC must be in the same namespace.

A Pod in `default` cannot use:

```text
storage-lab/storage-lab-pvc
```

Kubernetes will report that the PVC does not exist in the Pod's namespace.

## 6. Issue encountered

A Deployment/Pod was initially created without:

```yaml
metadata:
  namespace: storage-lab
```

The workload therefore went into `default` and could not find `storage-lab-pvc`.

### Resolution

Add:

```yaml
metadata:
  namespace: storage-lab
```

Then recreate/apply the workload.

## 7. Architecture

```text
Nginx Pod
   |
   +-- volumeMount
          |
          PVC
          |
          PV
          |
       HostPath
```

## 8. Real-world use case

Applications commonly mount:
- application uploads
- media
- reports
- database files
- logs
- shared application data

## 9. Interview takeaway

A Pod references a PVC. The PVC references a PV. The Pod does not normally specify the PV directly.


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

