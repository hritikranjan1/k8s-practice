# Lab 24 — Understand the Kubernetes NodePort Port Range

## 1. Objective

In this lab, we will understand the NodePort port range and see how Kubernetes assigns a NodePort automatically.

You will learn:

- What the NodePort range is.
- Why NodePort values are different from Service ports.
- How Kubernetes chooses a NodePort.
- How to check the actual assigned port.
- How to troubleshoot a NodePort that is outside the configured range or already in use.

## 2. Theory

A NodePort Service exposes a Service through a port on Kubernetes nodes.

Kubernetes commonly uses the default NodePort range:

```text
30000–32767
```

The range can be customized by a cluster administrator, so check your cluster configuration if you need certainty.

There are three different ports to understand:

| Port | Meaning | Example |
|---|---|---:|
| `port` | Port exposed by the Service | 80 |
| `targetPort` | Port used by the application in the Pod | 80 |
| `nodePort` | Port exposed on Kubernetes nodes | 30123 |

When a NodePort is not specified in the Service manifest, Kubernetes normally allocates an available port automatically from the configured range.

Do not hard-code a port merely because it worked in another cluster. The port must be available and valid for your cluster.

## 3. Safety and prerequisites

Check the context:

```bash
kubectl config current-context
kubectl get nodes
```

Confirm that you are using the intended lab cluster.

Check whether the namespace exists:

```bash
kubectl get namespace service-lab
```

Create it only if it does not exist:

```bash
kubectl create namespace service-lab
```

This lab uses a unique Pod and Service name so that it does not overwrite another lab's resources.

## 4. Step 1 — Create a Pod

Run:

```bash
kubectl run range-nginx \
  --image=nginx:stable \
  --labels=app=range-nginx \
  --restart=Never \
  -n service-lab
```

Wait until the Pod is ready:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/range-nginx \
  -n service-lab \
  --timeout=120s
```

Check:

```bash
kubectl get pod range-nginx -n service-lab -o wide
kubectl get pod range-nginx -n service-lab --show-labels
```

The Pod should have this label:

```text
app=range-nginx
```

## 5. Step 2 — Create a NodePort Service without specifying a NodePort

Create a YAML file:

```bash
vim nodeport-auto.yaml
```

Paste:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nodeport-auto
  namespace: service-lab
spec:
  type: NodePort
  selector:
    app: range-nginx
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
```

Notice that `nodePort` is not present.

Validate:

```bash
kubectl apply --dry-run=client -f nodeport-auto.yaml
```

Apply:

```bash
kubectl apply -f nodeport-auto.yaml
```

Check the result:

```bash
kubectl get svc nodeport-auto -n service-lab -o wide
```

Expected output will show a port mapping similar to:

```text
80:30xxx/TCP
```

The exact value depends on your cluster and should not be assumed in advance.

## 6. Step 3 — Read the automatically assigned NodePort

Run:

```bash
kubectl get svc nodeport-auto \
  -n service-lab \
  -o jsonpath='{.spec.ports[0].nodePort}'

echo
```

This prints the actual assigned NodePort.

Save the value in your notes. Use it for any later network test.

You can also inspect the Service:

```bash
kubectl describe svc nodeport-auto -n service-lab
```

## 7. Step 4 — Test the Service internally

Create a temporary client:

```bash
kubectl run range-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/range-client \
  -n service-lab \
  --timeout=120s
```

Test:

```bash
kubectl exec range-client -n service-lab -- \
  curl -v http://nodeport-auto:80
```

Expected result: the Nginx welcome page is returned.

Inspect the endpoints:

```bash
kubectl get endpoints nodeport-auto -n service-lab
```

The ready Nginx Pod should be listed.

## 8. Step 5 — Understand a fixed NodePort

A Service manifest can specify a particular NodePort:

```yaml
ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

This is useful when a network configuration depends on a known port.

However:

- The port must be inside the configured range.
- The port must be available.
- The cluster API server must accept the configuration.
- Network access must still be permitted by routing and firewall rules.

Automatic allocation avoids choosing a port manually, but it does not automatically make that port accessible from outside the cluster.

## 9. Common issues and solutions

### Issue 1: `provided port is not in the valid range`

The requested NodePort is outside the range configured for the cluster.

Resolution:

1. Check the error returned by Kubernetes.
2. Use automatic allocation by omitting `nodePort`, or select a valid unused port.
3. Reapply the manifest.
4. Read the actual assigned port with `kubectl get svc`.

Do not change cluster-wide configuration just to accommodate a practice Service.

### Issue 2: `provided port is already allocated`

Another Service is already using the requested port.

Check Services:

```bash
kubectl get svc -A
```

Inspect the `PORT(S)` column. If you need a fixed port, choose another available port. Otherwise, omit `nodePort` and let Kubernetes allocate it.

### Issue 3: The NodePort is assigned but the application cannot be accessed

An assigned NodePort does not guarantee that the node is reachable from your computer.

Check:

```bash
kubectl get svc nodeport-auto -n service-lab -o wide
kubectl get endpoints nodeport-auto -n service-lab
kubectl get nodes -o wide
```

Test internally before investigating firewall and network access.

### Issue 4: The Service has no endpoints

Check the labels:

```bash
kubectl get pod range-nginx -n service-lab --show-labels
kubectl describe svc nodeport-auto -n service-lab
```

The Service selector is `app=range-nginx`, so the Pod must have the matching label and be ready.

## 10. What did we learn?

- Kubernetes commonly uses NodePort values from `30000–32767`.
- The range can be customized.
- Kubernetes can assign a NodePort automatically.
- The actual NodePort should be obtained from the Service object.
- A valid NodePort does not guarantee network reachability.
- Port allocation and external network access are separate concerns.

## 11. Real-world use

Automatic allocation is useful for labs and development because it avoids hard-coding port numbers.

A fixed NodePort can be useful when a known port is required by an external network appliance, but the design must account for conflicts and the cluster's configured port range.

## 12. Evidence to save

```bash
kubectl get svc nodeport-auto -n service-lab -o wide
kubectl get endpoints nodeport-auto -n service-lab
kubectl exec range-client -n service-lab -- \
  curl -s http://nodeport-auto:80
```

Record the assigned NodePort and whether internal access worked.

## 13. Cleanup

Delete only the resources created in this lab:

```bash
kubectl delete pod range-client -n service-lab
kubectl delete svc nodeport-auto -n service-lab
kubectl delete pod range-nginx -n service-lab
```

## 14. Interview questions

**Q1. What is the default NodePort range?**

Common Kubernetes defaults are `30000–32767`, but a cluster administrator can customize the range.

**Q2. What happens if you omit `nodePort`?**

Kubernetes normally allocates an available port from the configured NodePort range.

**Q3. Why might a fixed NodePort fail?**

It may be outside the configured range or already allocated to another Service.

**Q4. Does an assigned NodePort mean the application is publicly accessible?**

No. Routing, firewall rules, node addresses, and network configuration determine whether a client can reach it.

---

**Lab 24 complete.**
