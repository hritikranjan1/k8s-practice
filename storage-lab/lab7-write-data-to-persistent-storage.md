# Lab 7 — Write Data to Persistent Storage

## 1. Objective

Prove that data written inside the mounted directory is actually going to persistent storage.

## 2. Write test data

```bash
kubectl exec nginx-storage -n storage-lab --   sh -c 'echo "Persistent Data" > /usr/share/nginx/html/data.txt'
```

Read it:

```bash
kubectl exec nginx-storage -n storage-lab --   cat /usr/share/nginx/html/data.txt
```

Expected:

```text
Persistent Data
```

## 3. Why this test matters

Creating a mount is not enough. A real persistence test must write data and later prove that the data survives Pod replacement.

## 4. Check the file

```bash
kubectl exec nginx-storage -n storage-lab --   ls -lah /usr/share/nginx/html/data.txt
```

## 5. Check Nginx

Because the file is inside Nginx's document root, you can also expose it through Nginx if networking is configured.

## 6. Real-world equivalent

The same test represents:
- uploading an image
- creating a report
- writing application state
- saving a generated file
- storing database data

## 7. Interview takeaway

Container filesystem and persistent volume are different lifecycle domains. Data written to a mounted PVC is intended to outlive the Pod.


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

