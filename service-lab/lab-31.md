# Lab 31 — Kubernetes Service DNS Resolution

## 1. Objective

In this lab, we will access an Nginx application using its Kubernetes Service DNS name instead of using a Pod IP or ClusterIP.

You will learn:

- What Kubernetes DNS does.
- How Service names are resolved.
- Why a Service name is easier to use than a Pod IP.
- How to test DNS from inside a Pod.
- How to separate DNS problems from Service networking problems.

## 2. Theory: What is Kubernetes DNS?

Kubernetes provides cluster DNS so that applications can discover Services using names.

For example, a Service named `dns-nginx-service` in namespace `service-lab` can normally be accessed by another Pod in the same namespace using:

```text
http://dns-nginx-service:80
```

A fully qualified Service DNS name commonly has this format:

```text
<service-name>.<namespace>.svc.cluster.local
```

For this lab:

```text
dns-nginx-service.service-lab.svc.cluster.local
```

The cluster domain is often `cluster.local`, but it can be configured differently.

DNS resolves a Service name to the Service's ClusterIP. Kubernetes networking then routes traffic to suitable backend Pods.

## 3. Safety and prerequisites

Check your current context:

```bash
kubectl config current-context
kubectl get nodes
```

Use the intended lab cluster.

Create the namespace only if it does not exist:

```bash
kubectl get namespace service-lab
```

If needed:

```bash
kubectl create namespace service-lab
```

This lab uses unique resource names: `dns-nginx`, `dns-nginx-service`, and `dns-client`.

If these resources already exist, inspect and reuse the resources that belong to this lab instead of creating duplicates.

## 4. Step 1 — Create an Nginx Pod

Run:

```bash
kubectl run dns-nginx \
  --image=nginx:stable \
  --labels=app=dns-nginx \
  --restart=Never \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/dns-nginx \
  -n service-lab \
  --timeout=120s
```

Check the Pod:

```bash
kubectl get pod dns-nginx -n service-lab -o wide
kubectl get pod dns-nginx -n service-lab --show-labels
```

The Pod label should be:

```text
app=dns-nginx
```

## 5. Step 2 — Create a Service

Expose the Pod:

```bash
kubectl expose pod dns-nginx \
  --name=dns-nginx-service \
  --type=ClusterIP \
  --port=80 \
  --target-port=80 \
  -n service-lab
```

Check the Service:

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
```

Check the endpoints:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
```

The ready Pod should appear as a backend endpoint.

## 6. Step 3 — Create a DNS client Pod

Create a client with `curl`:

```bash
kubectl run dns-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for it:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/dns-client \
  -n service-lab \
  --timeout=120s
```

Check both Pods:

```bash
kubectl get pods -n service-lab -o wide
```

## 7. Step 4 — Access the Service using its short DNS name

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://dns-nginx-service:80
```

Expected result: the Nginx welcome HTML is returned.

The short name works because the client and Service are in the same namespace, and the Pod's DNS search configuration normally includes that namespace.

## 8. Step 5 — Access the Service using a namespace-qualified name

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://dns-nginx-service.service-lab:80
```

This includes both the Service name and namespace.

It should work when cluster DNS and Service networking are configured correctly.

## 9. Step 6 — Inspect the DNS configuration

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  cat /etc/resolv.conf
```

The file commonly contains:

- A DNS nameserver address.
- A search list containing namespace and cluster-domain suffixes.
- DNS options.

Do not assume the nameserver address will be identical in every cluster.

If you need to investigate the DNS Service, inspect the actual resources:

```bash
kubectl get svc -n kube-system -o wide
kubectl get pods -n kube-system -o wide
kubectl get endpointslice -n kube-system
```

RKE2 installations may use resource names that differ from those in other Kubernetes distributions.

## 10. Step 7 — Separate DNS from Service networking

Get the Service IP:

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
```

Use the actual ClusterIP in this command:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://<CLUSTER-IP>:80
```

Replace `<CLUSTER-IP>` with the IP returned by Kubernetes.

Interpret the result:

- Service name fails but ClusterIP works: DNS is a likely problem.
- Service name and ClusterIP both fail: investigate the Service, endpoints, Pod, ports, and networking.
- Both work: name resolution and internal Service access are functioning for this test.

## 11. Common issues and solutions

### Issue 1: `Could not resolve host`

Check:

```bash
kubectl get svc dns-nginx-service -n service-lab
kubectl exec dns-client -n service-lab -- cat /etc/resolv.conf
```

Then test the ClusterIP directly.

If the IP works but the name fails, inspect the cluster's DNS resources and logs using their actual names. Do not assume the DNS Service is named `kube-dns`.

### Issue 2: Service name resolves but the request times out

DNS may be working while Service routing or the application is not.

Check:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
kubectl get pods -n service-lab -o wide
kubectl logs dns-nginx -n service-lab
```

### Issue 3: The Service has no endpoints

Check the selector and labels:

```bash
kubectl describe svc dns-nginx-service -n service-lab
kubectl get pod dns-nginx -n service-lab --show-labels
```

Ensure that the Pod is Ready and its label matches the Service selector.

### Issue 4: DNS resources appear missing

Inspect actual resources:

```bash
kubectl get svc -n kube-system -o wide
kubectl get pods -n kube-system -o wide
kubectl get endpointslice -n kube-system
```

Use the names shown by your cluster. Avoid deleting or restarting DNS components as a first troubleshooting step.

## 12. What did we learn?

- Kubernetes DNS allows applications to use Service names.
- A short Service name normally works within the same namespace.
- A Service's DNS name resolves to its ClusterIP.
- DNS resolution and traffic routing are separate steps.
- Testing the ClusterIP directly helps isolate DNS problems.

## 13. Real-world use

A frontend application can call:

```text
http://backend-service:8080
```

instead of storing a backend Pod IP address.

This is more reliable because Pods can be replaced and their IPs can change.

## 14. Evidence to save

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
kubectl get endpoints dns-nginx-service -n service-lab
kubectl exec dns-client -n service-lab -- \
  cat /etc/resolv.conf
kubectl exec dns-client -n service-lab -- \
  curl -s http://dns-nginx-service:80
```

Record whether the short name and namespace-qualified name worked.

## 15. Cleanup

Delete only the resources created in this lab:

```bash
kubectl delete pod dns-client -n service-lab
kubectl delete svc dns-nginx-service -n service-lab
kubectl delete pod dns-nginx -n service-lab
```

If later labs depend on these resources, keep them until those labs are complete or recreate them as needed.

## 16. Interview questions

**Q1. What is Kubernetes DNS used for?**

It allows Pods to discover Services using names rather than fixed IP addresses.

**Q2. What is the DNS name of a Service?**

A common full name is `<service>.<namespace>.svc.cluster.local`, assuming the cluster domain is `cluster.local`.

**Q3. What is the difference between DNS and a Service?**

DNS resolves the Service name to an address. The Service provides the stable endpoint and routes traffic to backend Pods.

**Q4. How do you distinguish a DNS problem from a Service problem?**

Test the Service by name and by its ClusterIP. If the IP works but the name does not, DNS is a likely cause.

---

**Lab 31 complete.**
