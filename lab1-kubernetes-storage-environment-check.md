# Lab 1 — Kubernetes Storage Environment Check

## 1. Objective

Before creating PVs and PVCs, verify that the Kubernetes cluster, nodes, namespaces, StorageClasses, provisioners, and existing storage resources are healthy.

## 2. Why this lab matters

Storage problems are often caused by the environment rather than the YAML. A DevOps engineer should check the cluster first instead of immediately changing manifests.

Typical production questions:
- Is the node Ready?
- Which StorageClasses exist?
- Is the cluster using static or dynamic provisioning?
- Is a CSI driver installed?
- Is a storage provisioner running?
- Are there already PVs/PVCs?
- Is the target namespace available?

## 3. Step-by-step

### Check Kubernetes context

```bash
kubectl config current-context
kubectl config get-contexts
```

For these labs, use only:

```text
default
```

Never run destructive lab cleanup against the other production-like contexts.

### Check cluster and nodes

```bash
kubectl cluster-info
kubectl get nodes
kubectl get nodes -o wide
```

Expected:

```text
server-1   Ready
```

### Check namespaces

```bash
kubectl get namespaces
```

Create the lab namespace if required:

```bash
kubectl create namespace storage-lab
```

If it already exists, Kubernetes reports that it already exists; that is not a problem.

### Check StorageClasses

```bash
kubectl get storageclass
kubectl get sc -o wide
```

Important observations from this environment:

- `manual` uses `kubernetes.io/no-provisioner`
- `local-path` uses `rancher.io/local-path`
- `manual` is for static/manual PV creation
- `local-path` is for dynamic provisioning

Inspect them:

```bash
kubectl get storageclass manual -o yaml
kubectl get storageclass local-path -o yaml
```

### Check PV/PVC state

```bash
kubectl get pv
kubectl get pvc -A
```

### Check CSI drivers

```bash
kubectl get csidrivers
```

In this lab environment, no CSI drivers were installed:

```text
No resources found
```

### Check storage-related Pods

```bash
kubectl get pods -A | grep -Ei 'csi|local-path|storage'
```

The local-path provisioner was running:

```text
local-path-provisioner-...   1/1   Running
```

## 4. Important discovery

`WaitForFirstConsumer` does **not** mean dynamic provisioning.

For example, `manual` had:

```yaml
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

That means the PV is still manually created. `WaitForFirstConsumer` controls when binding/provisioning decisions happen; it does not itself create storage.

## 5. Verification checklist

```bash
kubectl config current-context
kubectl get nodes
kubectl get ns storage-lab
kubectl get sc
kubectl get pv
kubectl get pvc -A
kubectl get csidrivers
```

## 6. Troubleshooting

### Problem: wrong Kubernetes context

**Symptom:** You see unexpected production resources.

**Resolution:**

```bash
kubectl config get-contexts
kubectl config use-context default
kubectl config current-context
```

### Problem: no StorageClass for dynamic provisioning

**Cause:** No dynamic provisioner was installed.

**Resolution in the isolated lab:**

```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

Then:

```bash
kubectl get sc
kubectl get pods -A | grep local-path
```

## 7. Real-world use case

During incident troubleshooting, a PVC stuck in `Pending` should trigger environment checks before changing application manifests.

## 8. Interview takeaway

A StorageClass is not storage itself. It describes how Kubernetes should provision storage. A provisioner/CSI driver actually performs the storage operation.



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

