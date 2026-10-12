# Lab 27 — Compare ClusterIP, NodePort, and LoadBalancer

## 1. Objective

In this lab, we will compare the three common Kubernetes Service types:

- ClusterIP
- NodePort
- LoadBalancer

We will learn when each type is used, how their traffic paths differ, and how to choose the right type for a real application.

## 2. Theory

A Kubernetes Service provides a stable way to access an application running in one or more Pods.

The Service type determines how the application is exposed.

### ClusterIP

ClusterIP is intended for internal access within the cluster.

```text
Client Pod
    |
    v
ClusterIP Service
    |
    v
Application Pod
```

Example use: a frontend Pod calls an internal backend API.

### NodePort

NodePort exposes the Service through a port on the Kubernetes nodes.

```text
External client
    |
    v
Node IP : NodePort
    |
    v
Service
    |
    v
Application Pod
```

Example use: a small lab where you want to test access through a node address.

### LoadBalancer

LoadBalancer requests an external load balancer through a supported infrastructure integration.

```text
External client
    |
    v
External load balancer
    |
    v
Kubernetes Service
    |
    v
Application Pod
```

Example use: an application that needs a stable external entry point provided by a cloud or on-premises load-balancer implementation.

## 3. Comparison table

| Feature | ClusterIP | NodePort | LoadBalancer |
|---|---|---|---|
| Internal cluster access | Yes | Yes | Yes |
| Uses a ClusterIP | Yes | Normally yes | Normally yes |
| Exposes a node port | No | Yes | May allocate one |
| Requests an external load balancer | No | No | Yes |
| Requires external infrastructure for external access | Not for normal internal use | Network access to a node is required | Yes, for a functioning external load balancer |
| Typical use | Internal APIs | Testing or specific node-port designs | External application access |

The actual reachability of any Service depends on cluster networking and security policy.

## 4. Prerequisites and safety

Check your current context:

```bash
kubectl config current-context
kubectl get nodes
```

Check whether `service-lab` exists:

```bash
kubectl get namespace service-lab
```

Create it only if it does not exist:

```bash
kubectl create namespace service-lab
```

This lab creates three small Nginx Pods and three Services. It does not change any shared cluster configuration.

## 5. Step 1 — Create three test Pods

Create the ClusterIP test Pod:

```bash
kubectl run compare-clusterip \
  --image=nginx:stable \
  --labels=app=compare-clusterip \
  --restart=Never \
  -n service-lab
```

Create the NodePort test Pod:

```bash
kubectl run compare-nodeport \
  --image=nginx:stable \
  --labels=app=compare-nodeport \
  --restart=Never \
  -n service-lab
```

Create the LoadBalancer test Pod:

```bash
kubectl run compare-loadbalancer \
  --image=nginx:stable \
  --labels=app=compare-loadbalancer \
  --restart=Never \
  -n service-lab
```

Wait for the Pods:

```bash
kubectl wait --for=condition=Ready pod/compare-clusterip \
  -n service-lab --timeout=120s

kubectl wait --for=condition=Ready pod/compare-nodeport \
  -n service-lab --timeout=120s

kubectl wait --for=condition=Ready pod/compare-loadbalancer \
  -n service-lab --timeout=120s
```

Check:

```bash
kubectl get pods -n service-lab -o wide
```

## 6. Step 2 — Create a ClusterIP Service

Run:

```bash
kubectl expose pod compare-clusterip \
  --name=compare-clusterip-service \
  --type=ClusterIP \
  --port=80 \
  --target-port=80 \
  -n service-lab
```

Inspect it:

```bash
kubectl get svc compare-clusterip-service -n service-lab -o wide
```

Expected type:

```text
ClusterIP
```

This Service is intended for internal cluster access.

## 7. Step 3 — Create a NodePort Service

Run:

```bash
kubectl expose pod compare-nodeport \
  --name=compare-nodeport-service \
  --type=NodePort \
  --port=80 \
  --target-port=80 \
  -n service-lab
```

Inspect it:

```bash
kubectl get svc compare-nodeport-service -n service-lab -o wide
```

The output should show a NodePort mapping, commonly displayed like:

```text
80:30xxx/TCP
```

Read the actual assigned port rather than guessing it.

## 8. Step 4 — Create a LoadBalancer Service

Run:

```bash
kubectl expose pod compare-loadbalancer \
  --name=compare-loadbalancer-service \
  --type=LoadBalancer \
  --port=80 \
  --target-port=80 \
  -n service-lab
```

Inspect it:

```bash
kubectl get svc compare-loadbalancer-service -n service-lab -o wide
```

The external IP may remain `<pending>` if the cluster has no functioning LoadBalancer integration. That is a possible outcome in an on-premises environment.

## 9. Step 5 — Compare the three Services

Run:

```bash
kubectl get svc -n service-lab
```

Look for these three names:

```text
compare-clusterip-service
compare-nodeport-service
compare-loadbalancer-service
```

Inspect their detailed configurations:

```bash
kubectl describe svc compare-clusterip-service -n service-lab
kubectl describe svc compare-nodeport-service -n service-lab
kubectl describe svc compare-loadbalancer-service -n service-lab
```

Compare:

- Service type
- ClusterIP
- Service port
- Target port
- NodePort, if allocated
- External IP, if assigned
- Endpoints

## 10. Step 6 — Test internal access

Create a client:

```bash
kubectl run compare-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait --for=condition=Ready pod/compare-client \
  -n service-lab --timeout=120s
```

Test the ClusterIP Service:

```bash
kubectl exec compare-client -n service-lab -- \
  curl -sS http://compare-clusterip-service:80
```

Test the NodePort Service internally:

```bash
kubectl exec compare-client -n service-lab -- \
  curl -sS http://compare-nodeport-service:80
```

Test the LoadBalancer Service internally:

```bash
kubectl exec compare-client -n service-lab -- \
  curl -sS http://compare-loadbalancer-service:80
```

All three may work internally when the Pods are ready, the selectors match, DNS works, and Service networking is functioning.

The external IP status of a LoadBalancer Service does not, by itself, determine whether its internal ClusterIP can be used.

## 11. Common issues and solutions

### Issue 1: A Service has no endpoints

Check the Service and matching Pod:

```bash
kubectl get pods -n service-lab --show-labels
kubectl get endpoints -n service-lab
```

The selector must match the corresponding Pod label. Also check readiness.

### Issue 2: LoadBalancer remains pending

This may be expected on a self-managed cluster without LoadBalancer integration.

Inspect:

```bash
kubectl describe svc compare-loadbalancer-service -n service-lab
```

Do not install cluster-wide load-balancer components without approval.

### Issue 3: NodePort is not reachable externally

Check the actual NodePort and node IP:

```bash
kubectl get svc compare-nodeport-service -n service-lab -o wide
kubectl get nodes -o wide
```

Investigate routing, firewall rules, and VM networking.

### Issue 4: Service DNS does not resolve

Confirm that the Service exists:

```bash
kubectl get svc -n service-lab
```

Test using its ClusterIP from the client. If direct IP access works but DNS fails, investigate cluster DNS separately.

## 12. What did we learn?

- ClusterIP is intended for internal access.
- NodePort exposes a port on cluster nodes.
- LoadBalancer requests external load-balancer integration.
- All three types can provide internal Service access.
- An external IP is not guaranteed simply because a Service is declared as LoadBalancer.
- Choosing a Service type depends on the application's access requirements and available infrastructure.

## 13. Real-world design example

Consider a three-tier application:

```text
User
 |
 v
Frontend entry point
 |
 v
Frontend application
 |
 v
Backend API Service (ClusterIP)
 |
 v
Backend Pods
 |
 v
Database Service (ClusterIP)
 |
 v
Database Pods
```

The frontend entry point might use a LoadBalancer or an Ingress architecture. Internal backend and database communication commonly uses ClusterIP Services.

A database should not be exposed publicly without a carefully reviewed security design.

## 14. Evidence to save

```bash
kubectl get pods -n service-lab -o wide
kubectl get svc -n service-lab -o wide
kubectl get endpoints -n service-lab
```

Record the type, ports, and external-IP status of each Service.

## 15. Cleanup

Delete only the resources created by this lab:

```bash
kubectl delete pod compare-client -n service-lab

kubectl delete svc \
  compare-clusterip-service \
  compare-nodeport-service \
  compare-loadbalancer-service \
  -n service-lab

kubectl delete pod \
  compare-clusterip \
  compare-nodeport \
  compare-loadbalancer \
  -n service-lab
```

## 16. Interview questions

**Q1. Which Service type is the default?**

ClusterIP.

**Q2. Which Service type exposes a port on Kubernetes nodes?**

NodePort.

**Q3. Which Service type requests an external load balancer?**

LoadBalancer.

**Q4. Is LoadBalancer always publicly accessible?**

No. The address must be allocated and reachable, and the relevant routing and firewall rules must permit traffic.

**Q5. Which Service type is commonly used for internal APIs?**

ClusterIP.

---

**Lab 27 complete.**
