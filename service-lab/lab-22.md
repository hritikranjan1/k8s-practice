# Lab 22 — Create a NodePort Service in Kubernetes

## 1. Objective

In this lab, we will create a NodePort Service and understand how to expose an application through a Kubernetes node's IP address and a port.

You will learn:

- What a NodePort Service is.
- How NodePort differs from ClusterIP.
- How to define a NodePort Service using YAML.
- How the Service selector connects the Service to a Pod.
- How to inspect the automatically assigned or manually specified NodePort.
- How to troubleshoot a Service that has no endpoints.

## 2. Theory: What is NodePort?

A NodePort Service exposes an application on a port of each Kubernetes node.

The access pattern is:

```text
Browser or external client
          |
          | http://NODE-IP:NODEPORT
          v
    Kubernetes node
          |
          v
    NodePort Service
          |
          v
       Nginx Pod
```

For example, a NodePort might be `30080`. If a node is reachable at `192.168.1.50`, a client might access:

```text
http://192.168.1.50:30080
```

This example IP is only illustrative. Always use an actual reachable node IP from your cluster.

### Common Service types

- `ClusterIP`: internal cluster access.
- `NodePort`: access through a node IP and a port.
- `LoadBalancer`: requests an external load balancer through supported infrastructure.

NodePort Services generally also receive a ClusterIP, so they can still be used internally.

## 3. Safety and prerequisites

Check the current context:

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Make sure you are using the intended lab cluster.

Create the namespace if needed:

```bash
kubectl get namespace service-lab
```

If it does not exist:

```bash
kubectl create namespace service-lab
```

Do not use an existing Service name if it belongs to another lab. This lab uses `nodeport-service`.

## 4. Step 1 — Create the Nginx Pod

Create the Pod with a specific label:

```bash
kubectl run nodeport-nginx \
  --image=nginx:stable \
  --labels=app=nodeport-nginx \
  --restart=Never \
  -n service-lab
```

Wait until it is Ready:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/nodeport-nginx \
  -n service-lab \
  --timeout=120s
```

Inspect the Pod:

```bash
kubectl get pod nodeport-nginx -n service-lab -o wide
kubectl get pod nodeport-nginx -n service-lab --show-labels
```

The expected label is:

```text
app=nodeport-nginx
```

## 5. Step 2 — Write the NodePort Service YAML

Create a manifest:

```bash
vim nodeport-service.yaml
```

Paste:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nodeport-service
  namespace: service-lab
spec:
  type: NodePort
  selector:
    app: nodeport-nginx
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30080
```

Save the file.

### Understand each field

- `apiVersion: v1`: the API version for this Service resource.
- `kind: Service`: tells Kubernetes that this is a Service.
- `metadata.name`: the Service name.
- `metadata.namespace`: the namespace where the Service will exist.
- `type: NodePort`: requests a NodePort Service.
- `selector`: identifies the backend Pods.
- `protocol: TCP`: uses TCP for HTTP traffic.
- `port: 80`: the port exposed by the Service.
- `targetPort: 80`: the port on the Nginx Pod.
- `nodePort: 30080`: the port exposed on the nodes.

Kubernetes commonly uses the default NodePort range `30000–32767`, but a cluster administrator can configure a different range.

Port `30080` must be within your cluster's configured range and available for use. If it is already assigned, choose an unused port from the configured range.

## 6. Step 3 — Validate and apply the YAML

Validate the manifest on the client:

```bash
kubectl apply --dry-run=client -f nodeport-service.yaml
```

If validation succeeds, apply it:

```bash
kubectl apply -f nodeport-service.yaml
```

Check the Service:

```bash
kubectl get svc nodeport-service -n service-lab -o wide
```

Expected output will resemble:

```text
NAME               TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
nodeport-service   NodePort   <assigned-IP>  <none>        80:30080/TCP   ...
```

The ClusterIP is assigned by the cluster. `80:30080/TCP` means that the Service uses port 80 internally and NodePort 30080 for node-level access.

Check the detailed configuration:

```bash
kubectl describe svc nodeport-service -n service-lab
```

Check endpoints:

```bash
kubectl get endpoints nodeport-service -n service-lab
```

Or inspect EndpointSlices:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=nodeport-service
```

The ready Nginx Pod should appear as a backend endpoint.

## 7. Step 4 — Test the Service inside the cluster

Create a client Pod:

```bash
kubectl run nodeport-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/nodeport-client \
  -n service-lab \
  --timeout=120s
```

Test the Service using DNS:

```bash
kubectl exec nodeport-client -n service-lab -- \
  curl -v http://nodeport-service:80
```

Expected result: Nginx HTML is returned.

This test confirms internal Service access. It does not yet prove that a client outside the cluster can reach the NodePort.

## 8. Step 5 — Inspect node IPs and NodePort

List node addresses:

```bash
kubectl get nodes -o wide
```

Identify an address reachable from your client machine or network.

The address shown under `INTERNAL-IP` may not be reachable from your desktop if the cluster is running inside a VM, behind NAT, or behind a firewall.

Confirm the assigned NodePort:

```bash
kubectl get svc nodeport-service \
  -n service-lab \
  -o jsonpath='{.spec.ports[0].nodePort}'

echo
```

If your node IP is reachable and network rules permit traffic, test from a machine that can reach that IP:

```bash
curl -v http://<NODE-IP>:30080
```

Replace `<NODE-IP>` with the actual reachable node address.

If testing from the same VM, use a node address that is valid from that VM. Do not assume `localhost` will work.

## 9. Common issues and troubleshooting

### Issue 1: `nodePort` is already allocated

If Kubernetes rejects the manifest because the requested NodePort is in use, select another unused port within the configured NodePort range.

Check existing Services:

```bash
kubectl get svc -A
```

Look at the `PORT(S)` column for ports such as `80:30080/TCP`.

Edit the manifest:

```bash
vim nodeport-service.yaml
```

Change `nodePort` to an available port and reapply:

```bash
kubectl apply -f nodeport-service.yaml
```

### Issue 2: The Service has no endpoints

Check the Service selector and Pod labels:

```bash
kubectl describe svc nodeport-service -n service-lab
kubectl get pod nodeport-nginx -n service-lab --show-labels
kubectl get endpoints nodeport-service -n service-lab
```

The selector must match the Pod label:

```text
Selector: app=nodeport-nginx
Pod label: app=nodeport-nginx
```

Correct the selector or Pod labels if necessary.

### Issue 3: Internal access works, but external access fails

Check:

```bash
kubectl get nodes -o wide
kubectl get svc nodeport-service -n service-lab -o wide
kubectl get endpoints nodeport-service -n service-lab
```

Possible causes:

- The node IP is not reachable from your client.
- A host firewall blocks the NodePort.
- A cloud firewall or network ACL blocks the traffic.
- The VM is using NAT and the port is not forwarded.
- The application or Service has no ready backend endpoints.
- The cluster's networking configuration affects NodePort access.

Test internal access first. Then investigate node routing and firewalls. Do not disable the firewall completely just to make the lab work.

### Issue 4: The YAML is invalid

Validate the file:

```bash
kubectl apply --dry-run=client -f nodeport-service.yaml
```

Check indentation, spelling, and whether all fields are nested under the correct parent. YAML uses spaces; avoid tab indentation.

### Issue 5: Nginx Pod is not Ready

Inspect:

```bash
kubectl describe pod nodeport-nginx -n service-lab
kubectl logs nodeport-nginx -n service-lab
kubectl get events -n service-lab --sort-by=.lastTimestamp
```

Resolve image-pull, scheduling, or container startup errors before testing the Service.

## 10. What did we learn?

- NodePort makes a Service reachable through a node IP and a port.
- A NodePort Service also has a ClusterIP.
- The Service selector must match backend Pod labels.
- `port`, `targetPort`, and `nodePort` have different purposes.
- A working internal Service does not guarantee external network reachability.
- Firewalls, VM networking, and node routing can affect access.

## 11. Real-world use

NodePort can be useful for small labs, development environments, and testing access through node addresses.

In production, teams often use a LoadBalancer or Ingress-based design when supported, rather than asking users to connect directly to individual node addresses.

## 12. Evidence to save

```bash
kubectl get pod nodeport-nginx -n service-lab -o wide
kubectl get svc nodeport-service -n service-lab -o wide
kubectl get endpoints nodeport-service -n service-lab
kubectl exec nodeport-client -n service-lab -- \
  curl -s http://nodeport-service:80
```

If external access is supported, record the node IP you used and the result of the `curl` test. Do not publish private IPs or sensitive network information unnecessarily.

## 13. Cleanup

Delete only the resources created in this lab:

```bash
kubectl delete pod nodeport-client -n service-lab
kubectl delete svc nodeport-service -n service-lab
kubectl delete pod nodeport-nginx -n service-lab
```

Keep `nodeport-service.yaml` if you want to retain the practice manifest.

## 14. Interview questions

**Q1. What is NodePort?**

It exposes a Service through a port on Kubernetes nodes.

**Q2. What is the default NodePort range?**

Common Kubernetes defaults are `30000–32767`, although administrators can configure a different range.

**Q3. What is the difference between `port`, `targetPort`, and `nodePort`?**

`port` is the Service port, `targetPort` is the backend Pod port, and `nodePort` is the port exposed on nodes.

**Q4. Why can NodePort fail even when the Service works internally?**

The node IP may be unreachable or traffic may be blocked by a firewall, NAT, or other network configuration.

**Q5. Does a NodePort Service require a LoadBalancer?**

No. NodePort exposes the Service through node IPs and ports. A LoadBalancer is a separate Service type that requests external load-balancer integration.

---

**Lab 22 complete.**
