# Lab 21 — Create a ClusterIP Service in Kubernetes

## 1. Objective

In this lab, we will create a Kubernetes ClusterIP Service and use it to access an Nginx application from another Pod.

By the end of this lab, you will understand:

- What a Kubernetes Service is.
- What ClusterIP means.
- Why we need a Service when Pods can be created directly.
- How a Service selects Pods using labels.
- How to check Service endpoints.
- How to access an application using its Service name.
- How to troubleshoot a Service that cannot reach its Pods.

## 2. Theory: What is a Kubernetes Service?

A Pod is the smallest deployable unit in Kubernetes. A Pod receives an IP address, but that IP address can change when the Pod is recreated.

For example:

- Today, an Nginx Pod may have IP `10.42.0.20`.
- If the Pod is deleted and recreated, it may receive IP `10.42.0.35`.
- An application using the old IP may stop working.

A Kubernetes Service provides a stable network endpoint for accessing a group of Pods.

Instead of connecting directly to a Pod IP, another application can connect to the Service.

### What is ClusterIP?

ClusterIP is the default Kubernetes Service type.

It makes an application accessible inside the Kubernetes cluster. It is not normally directly accessible from outside the cluster.

Example:

```text
Client Pod
    |
    | HTTP request
    v
ClusterIP Service
    |
    v
Nginx Pod
```

The Service forwards traffic to suitable backend Pods selected by its selector.

## 3. Prerequisites and safety

Check your current Kubernetes context:

```bash
kubectl config current-context
kubectl get nodes
```

Confirm that your intended cluster is selected and the node is Ready.

Create the lab namespace if it does not already exist:

```bash
kubectl get namespace service-lab
```

If it does not exist, create it:

```bash
kubectl create namespace service-lab
```

If it already exists, continue without recreating it.

## 4. Step 1 — Create an Nginx Pod

Create a Pod named `clusterip-nginx`:

```bash
kubectl run clusterip-nginx \
  --image=nginx:stable \
  --labels=app=clusterip-nginx \
  --restart=Never \
  -n service-lab
```

Check the Pod:

```bash
kubectl get pods -n service-lab -o wide
```

Wait for it to become Ready:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/clusterip-nginx \
  -n service-lab \
  --timeout=120s
```

Check its labels:

```bash
kubectl get pod clusterip-nginx \
  -n service-lab \
  --show-labels
```

The important label is:

```text
app=clusterip-nginx
```

The Service will use this label to find the Pod.

## 5. Step 2 — Create a ClusterIP Service

Expose the Pod through a Service:

```bash
kubectl expose pod clusterip-nginx \
  --name=clusterip-service \
  --type=ClusterIP \
  --port=80 \
  --target-port=80 \
  -n service-lab
```

Understand the options:

- `expose pod clusterip-nginx`: creates a Service for the Pod.
- `--name=clusterip-service`: sets the Service name.
- `--type=ClusterIP`: makes it internally accessible.
- `--port=80`: sets the port on the Service.
- `--target-port=80`: sends traffic to port 80 on the selected Pod.
- `-n service-lab`: creates the Service in the lab namespace.

Check the Service:

```bash
kubectl get svc -n service-lab
```

Get more details:

```bash
kubectl describe svc clusterip-service -n service-lab
```

Check the endpoint:

```bash
kubectl get endpoints clusterip-service -n service-lab
```

You can also inspect EndpointSlices:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=clusterip-service
```

The endpoint should include the IP address of the selected, ready Nginx Pod.

The ClusterIP will be assigned automatically. Do not expect it to be the same on every cluster.

## 6. Step 3 — Test the Service from another Pod

Create a temporary client Pod:

```bash
kubectl run clusterip-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for it to become Ready:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/clusterip-client \
  -n service-lab \
  --timeout=120s
```

Send a request to the Service:

```bash
kubectl exec clusterip-client -n service-lab -- \
  curl -v http://clusterip-service:80
```

Expected result: the command should return HTML containing the default Nginx welcome page.

You can also access the Service using its namespace-qualified DNS name:

```bash
kubectl exec clusterip-client -n service-lab -- \
  curl -v http://clusterip-service.service-lab:80
```

Both commands should work when cluster DNS and Service networking are functioning correctly.

## 7. How does the request work?

When the client runs:

```bash
curl http://clusterip-service:80
```

Kubernetes networking works through several components:

1. The client resolves the Service name using cluster DNS.
2. DNS returns the Service's ClusterIP.
3. The client sends an HTTP request to that IP and port.
4. Kubernetes Service networking routes the traffic to a suitable backend endpoint.
5. The Nginx Pod receives the request and returns the response.

The precise implementation of Service networking depends on the cluster's networking configuration.

## 8. Common issues and solutions

### Issue 1: The Pod is not Running

Check:

```bash
kubectl get pods -n service-lab
kubectl describe pod clusterip-nginx -n service-lab
kubectl get events -n service-lab --sort-by=.lastTimestamp
```

Possible causes include an image-pull failure, insufficient resources, or a container startup problem.

Resolve the specific error shown in the Pod events before continuing.

### Issue 2: The Service has no endpoints

Check:

```bash
kubectl get svc clusterip-service -n service-lab
kubectl get pod clusterip-nginx -n service-lab --show-labels
kubectl describe svc clusterip-service -n service-lab
kubectl get endpoints clusterip-service -n service-lab
```

The Service selector must match the Pod label:

```text
Service selector: app=clusterip-nginx
Pod label:        app=clusterip-nginx
```

If the labels do not match, correct the Service selector or Pod labels.

### Issue 3: `Could not resolve host`

This usually indicates a DNS resolution problem, but first verify that the Service exists:

```bash
kubectl get svc clusterip-service -n service-lab
```

Check the client Pod's DNS configuration:

```bash
kubectl exec clusterip-client -n service-lab -- cat /etc/resolv.conf
```

Test the Service ClusterIP directly:

```bash
kubectl get svc clusterip-service -n service-lab
```

Use the ClusterIP shown in the output:

```bash
kubectl exec clusterip-client -n service-lab -- \
  curl -v http://<CLUSTER-IP>:80
```

Replace `<CLUSTER-IP>` with the actual IP. If the IP works but the Service name does not, investigate DNS separately.

### Issue 4: Connection refused or timeout

Check the Pod's readiness, Nginx logs, Service port, target port, and endpoints:

```bash
kubectl logs clusterip-nginx -n service-lab
kubectl describe pod clusterip-nginx -n service-lab
kubectl describe svc clusterip-service -n service-lab
kubectl get endpoints clusterip-service -n service-lab
```

Do not assume every connection failure is a DNS issue.

## 9. What did we learn?

- A Service provides a stable way to reach backend Pods.
- ClusterIP is intended for internal cluster communication.
- A Service uses selectors to identify backend Pods.
- The Service port and target port are different concepts.
- Endpoints show which backend addresses can receive traffic.
- DNS allows clients to use a Service name instead of a changing IP.

## 10. Real-world use

A backend API may run in three Pods. A frontend application should not need to know the IP address of each backend Pod.

Instead, the frontend connects to a ClusterIP Service, such as:

```text
http://backend-service:8080
```

Kubernetes routes requests to suitable backend Pods.

ClusterIP is commonly used for internal APIs, internal web services, and communication between application components.

## 11. Evidence to save

Save the output of these commands in your lab notes:

```bash
kubectl get pods -n service-lab -o wide
kubectl get svc clusterip-service -n service-lab -o wide
kubectl get endpoints clusterip-service -n service-lab
kubectl exec clusterip-client -n service-lab -- \
  curl -s http://clusterip-service:80
```

## 12. Cleanup

Delete only the resources created in this lab:

```bash
kubectl delete pod clusterip-client -n service-lab
kubectl delete svc clusterip-service -n service-lab
kubectl delete pod clusterip-nginx -n service-lab
```

Do not delete the entire `service-lab` namespace because it may contain resources from other labs.

## 13. Interview questions

**Q1. What is a ClusterIP Service?**

It exposes an application through an internal cluster IP address.

**Q2. Why do we need a Service when we already have Pods?**

Pod IPs can change. A Service gives clients a stable endpoint and routes traffic to matching backend Pods.

**Q3. What is the difference between `port` and `targetPort`?**

`port` is the port exposed by the Service. `targetPort` is the port on the backend Pod to which traffic is forwarded.

**Q4. What happens when a Service has no endpoints?**

It has no suitable backend addresses to send traffic to. Check the selector, Pod labels, readiness, and EndpointSlices.

**Q5. Can a ClusterIP Service normally be accessed directly from outside the cluster?**

No. It is intended for internal cluster access. External access requires another access mechanism, such as NodePort, LoadBalancer, or an Ingress configuration.

---

**Lab 21 complete.**
