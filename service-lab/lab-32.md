# Lab 32 — Access a Kubernetes Service from Another Namespace

## 1. Objective

In this lab, we will access a Service in one namespace from a Pod in another namespace.

You will learn:

- How namespaces organize Kubernetes resources.
- Why a short Service name may fail across namespaces.
- How to use a namespace-qualified DNS name.
- How to use a fully qualified Service DNS name.
- How to troubleshoot cross-namespace access.

## 2. Theory

Namespaces separate and organize resources in a Kubernetes cluster.

For example:

```text
Namespace: service-lab
    |
    +-- dns-nginx Pod
    +-- dns-nginx-service Service

Namespace: service-client
    |
    +-- cross-namespace-client Pod
```

A namespace does not automatically prevent a Pod from communicating with a Service in another namespace.

However, a short Service name is normally resolved relative to the client's namespace.

If a client in `service-client` tries to access:

```text
http://dns-nginx-service:80
```

Kubernetes DNS will normally search for a Service named `dns-nginx-service` in `service-client`, not in `service-lab`.

To identify the target Service, include its namespace:

```text
http://dns-nginx-service.service-lab:80
```

A common fully qualified form is:

```text
http://dns-nginx-service.service-lab.svc.cluster.local:80
```

The cluster domain may differ from `cluster.local`.

## 3. Safety and prerequisites

Check the current context:

```bash
kubectl config current-context
kubectl get nodes
```

Use the intended lab cluster.

Check whether the source Service exists:

```bash
kubectl get svc dns-nginx-service -n service-lab
```

Check the target Pod:

```bash
kubectl get pod dns-nginx -n service-lab -o wide
```

If these resources are missing, create them by following `lab-31.md`.

Create the client namespace only if it does not exist:

```bash
kubectl get namespace service-client
```

If necessary:

```bash
kubectl create namespace service-client
```

Do not delete an existing namespace just to repeat this lab.

## 4. Step 1 — Create the client Pod in another namespace

Run:

```bash
kubectl run cross-namespace-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-client
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/cross-namespace-client \
  -n service-client \
  --timeout=120s
```

Verify:

```bash
kubectl get pods -n service-client -o wide
```

## 5. Step 2 — Test the short Service name

Run:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v --connect-timeout 5 http://dns-nginx-service:80
```

This may fail because the short name is resolved relative to the client namespace.

If a Service with that name exists in `service-client`, the request might reach that Service instead. Always verify the resource in the namespace you intend to access.

The important lesson is that the short name does not automatically identify the Service in `service-lab`.

## 6. Step 3 — Test the namespace-qualified name

Run:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v http://dns-nginx-service.service-lab:80
```

Expected result: the Nginx welcome page is returned.

The name includes:

```text
Service name: dns-nginx-service
Namespace:    service-lab
```

## 7. Step 4 — Test the fully qualified DNS name

Run:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v http://dns-nginx-service.service-lab.svc.cluster.local:80
```

This commonly works when the cluster's DNS domain is `cluster.local`.

If it fails while the namespace-qualified name works, inspect the client's DNS search configuration and determine the actual cluster domain. Do not assume every Kubernetes installation uses `cluster.local`.

## 8. Step 5 — Verify the Service and endpoints

Check the source Service:

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
```

Check endpoints:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
```

Check the application Pod:

```bash
kubectl get pod dns-nginx -n service-lab -o wide
```

If DNS resolution succeeds but the request fails, verify that the Service has a ready backend and that the target port is correct.

## 9. Step 6 — Inspect the client DNS configuration

Run:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  cat /etc/resolv.conf
```

Look at the search domains. The client normally has a search suffix for its own namespace, which explains why the short name may be resolved in the wrong namespace.

The DNS search list is part of name resolution. It does not replace the need to specify the correct namespace when accessing a Service in another namespace.

## 10. Common issues and solutions

### Issue 1: Short name does not resolve

The client may be searching in its own namespace.

Use the namespace-qualified name:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v http://dns-nginx-service.service-lab:80
```

### Issue 2: `Could not resolve host` for the fully qualified name

Check:

```bash
kubectl get svc dns-nginx-service -n service-lab
kubectl exec cross-namespace-client -n service-client -- \
  cat /etc/resolv.conf
```

Verify the actual cluster DNS domain and inspect the cluster's DNS resources.

### Issue 3: Name resolves, but connection fails

Check the Service endpoints:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
kubectl get pods -n service-lab -o wide
```

If the endpoints are valid, investigate Service routing, target ports, application health, and any NetworkPolicy restrictions.

### Issue 4: NetworkPolicy blocks communication

A NetworkPolicy can restrict traffic between Pods, including traffic across namespaces, when the cluster's network plugin enforces the policy.

Inspect applicable policies:

```bash
kubectl get networkpolicy -A
```

Do not remove a policy from a shared cluster simply to make the lab work. Determine which policy applies and obtain approval before changing it.

## 11. What did we learn?

- Namespaces organize Kubernetes resources.
- A short Service name is normally resolved relative to the client's namespace.
- Use `service.namespace` to identify a Service in another namespace.
- A fully qualified name includes the Service, namespace, `svc`, and cluster domain.
- DNS resolution does not guarantee network access; policies and Service routing can still block traffic.

## 12. Real-world use

A frontend application might run in a `frontend` namespace and access a backend Service in a `backend` namespace.

For example:

```text
http://backend-api.backend:8080
```

Using an explicit namespace helps make the intended destination clear.

## 13. Evidence to save

```bash
kubectl get pods -n service-client -o wide
kubectl get svc dns-nginx-service -n service-lab -o wide
kubectl get endpoints dns-nginx-service -n service-lab
kubectl exec cross-namespace-client -n service-client -- \
  curl -s http://dns-nginx-service.service-lab:80
```

Record which DNS forms succeeded and which failed.

## 14. Cleanup

Delete only the client Pod created in this lab:

```bash
kubectl delete pod cross-namespace-client -n service-client
```

Keep the `service-client` namespace if it contains resources from other labs.

If you are finished with the Lab 31 resources, clean them up using the instructions in `lab-31.md`.

## 15. Interview questions

**Q1. Can a Pod in one namespace access a Service in another namespace?**

Yes, provided DNS, networking, and security policies permit the connection.

**Q2. Why might a short Service name fail across namespaces?**

The name is normally resolved relative to the client's namespace.

**Q3. What is the namespace-qualified name?**

It commonly has the form `<service-name>.<namespace>`.

**Q4. Does using a fully qualified DNS name bypass NetworkPolicy?**

No. DNS identifies the destination; it does not bypass network access controls.

---

**Lab 32 complete.**
