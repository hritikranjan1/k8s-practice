# Lab 6 — Access and Inspect Mounted PVC Inside Pod

## 1. Objective

Learn how to inspect a mounted volume from inside the running container.

## 2. Check Pod

```bash
kubectl get pod nginx-storage -n storage-lab
```

## 3. Inspect filesystem

```bash
kubectl exec nginx-storage -n storage-lab -- df -h /usr/share/nginx/html
```

Check directory contents:

```bash
kubectl exec nginx-storage -n storage-lab -- ls -lah /usr/share/nginx/html
```

Check mount information:

```bash
kubectl exec nginx-storage -n storage-lab -- mount
```

## 4. Open a shell

```bash
kubectl exec -it nginx-storage -n storage-lab -- /bin/bash
```

If Bash is unavailable:

```bash
kubectl exec -it nginx-storage -n storage-lab -- /bin/sh
```

Inside:

```bash
cd /usr/share/nginx/html
pwd
df -h .
ls -lah
exit
```

## 5. Verify from Pod specification

```bash
kubectl get pod nginx-storage -n storage-lab -o yaml
```

Look for:

```yaml
volumes:
- name: storage
  persistentVolumeClaim:
    claimName: storage-lab-pvc
```

and:

```yaml
volumeMounts:
- mountPath: /usr/share/nginx/html
  name: storage
```

## 6. Troubleshooting

If the mount is missing:

```bash
kubectl describe pod nginx-storage -n storage-lab
kubectl get pvc -n storage-lab
kubectl get pv
```

Check Pod events at the bottom of `describe`.

## 7. Real-world use case

This is a standard first step when an application says:

```text
Cannot find uploaded file
Permission denied
Disk full
No such directory
```

A DevOps engineer should inspect the actual mounted filesystem, not only the YAML.


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

