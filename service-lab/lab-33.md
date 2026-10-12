# Lab 33 — Kubernetes Short DNS Name vs Fully Qualified DNS Name

## 1. Objective

In this lab, we will compare short Service names, namespace-qualified names, and fully qualified Service DNS names.

You will learn:

- How Kubernetes resolves short Service names.
- Why namespace matters.
- What a fully qualified domain name (FQDN) is.
- How DNS search domains affect name resolution.
- Which name format is useful for communication between namespaces.

## 2. Theory

A Kubernetes Service can be reached by its DNS name.

Suppose the Service is:

```text
Name:      dns-nginx-service
Namespace: service-lab
```

There are three useful name formats.

### Short Service name

```text
dns-nginx-service
```

This is convenient when the client is in the same namespace as the Service.

### Namespace-qualified name

```text
dns-nginx-service.service-lab
```

This identifies the Service and its namespace. It is useful when the client is in another namespace.

### Fully qualified Service DNS name

```text
dns-nginx-service.service-lab.svc.cluster.local
```

This includes the Service name, namespace, Service DNS subdomain, and cluster domain.

`cluster.local` is common but not guaranteed. Use the actual cluster domain if yours differs.

## 3. Example of name resolution

A Pod in `service-lab` may have a DNS search list similar to:

```text
service-lab.svc.cluster.local
svc.cluster.local
cluster.local
```

The exact configuration depends on the cluster.

When the client requests a short name, the resolver may try names formed by appending these search suffixes.

For a client in another namespace, the short name can resolve relative to that namespace rather than the namespace containing the target Service.

## 4. Safety and prerequisites

Check the context:

```bash
kubectl config current-context
kubectl get nodes
```

Check the Service from Lab 31:

```bash
kubectl get svc dns-nginx-service -n service-lab
```

Check whether both namespaces exist:

```bash
kubectl get namespace service-lab
kubectl get namespace service-client
```

If the Service or client Pod is missing, follow `lab-31.md` and `lab-32.md` to create them.

Do not delete namespaces to repeat the exercise.

## 5. Step 1 — Test names from the same namespace

Make sure the client Pod exists in `service-lab`:

```bash
kubectl get pod dns-client -n service-lab
```

Test the short name:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://dns-nginx-service:80
```

Test the namespace-qualified name:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://dns-nginx-service.service-lab:80
```

Test the fully qualified name:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://dns-nginx-service.service-lab.svc.cluster.local:80
```

All three may work when DNS is configured correctly and the cluster domain is `cluster.local`.

## 6. Step 2 — Inspect DNS search configuration

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  cat /etc/resolv.conf
```

Inspect the `search` line and identify the namespace and cluster-domain suffixes.

This configuration helps explain why a short name works inside the same namespace.

Do not edit the file inside the running Pod as a permanent DNS fix. Kubernetes normally generates this configuration for the Pod.

## 7. Step 3 — Test names from another namespace

Check that the client exists in `service-client`:

```bash
kubectl get pod cross-namespace-client -n service-client
```

Test the short name:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v --connect-timeout 5 http://dns-nginx-service:80
```

This may fail because the client searches for a Service with that name in its own namespace.

Now test the namespace-qualified name:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v http://dns-nginx-service.service-lab:80
```

Test the fully qualified name:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v http://dns-nginx-service.service-lab.svc.cluster.local:80
```

If the cluster uses another DNS domain, the last command must use that domain instead.

## 8. Step 4 — Understand the output

If `curl` returns Nginx HTML, the request reached the application.

If you see:

```text
Could not resolve host
```

the client could not resolve the supplied name. Check the Service name, namespace, cluster DNS, and cluster domain.

If you see:

```text
Connection timed out
```

the name may have resolved, but traffic did not complete. Investigate endpoints, networking, application health, and NetworkPolicy.

If you see:

```text
Connection refused
```

check the destination port, Pod health, and Service target port.

The exact error text may differ by client and network conditions.

## 9. Common issues and solutions

### Issue 1: Short name works in one namespace but not another

This is expected when the target Service exists only in the original namespace.

Use:

```text
dns-nginx-service.service-lab
```

### Issue 2: FQDN does not resolve

Verify that the Service exists:

```bash
kubectl get svc dns-nginx-service -n service-lab
```

Inspect the client's DNS configuration:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  cat /etc/resolv.conf
```

Check the actual cluster domain. Do not assume `cluster.local` if the installation uses a custom domain.

### Issue 3: DNS resolves but HTTP fails

Check the backend:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
kubectl get pods -n service-lab -o wide
```

Test the Service ClusterIP directly to separate DNS from routing.

### Issue 4: The target Service is missing

A DNS name cannot provide access to a Service that does not exist under that name and namespace.

Check:

```bash
kubectl get svc -n service-lab
kubectl get svc -n service-client
```

Use the actual resource name and namespace.

## 10. What did we learn?

- A short Service name is convenient inside the same namespace.
- A namespace-qualified name identifies the intended namespace.
- A fully qualified name includes the cluster DNS domain.
- DNS search paths explain how short names are expanded.
- DNS failures and connection failures are different problems.

## 11. Real-world use

Use short names for simple communication within one namespace.

Use namespace-qualified names for cross-namespace communication to make the destination explicit and reduce confusion.

For example:

```text
http://backend-api.backend:8080
```

A fully qualified form can be useful when the caller needs to specify the complete Service DNS name.

## 12. Evidence to save

```bash
kubectl exec dns-client -n service-lab -- cat /etc/resolv.conf
kubectl exec cross-namespace-client -n service-client -- \
  cat /etc/resolv.conf
kubectl get svc dns-nginx-service -n service-lab -o wide
```

Record which names worked from each namespace.

## 13. Cleanup

This lab does not require creating new resources if you already completed Labs 31 and 32.

If you created any temporary client Pod solely for this lab, delete that specific Pod. Do not delete the shared namespaces.

## 14. Interview questions

**Q1. What is an FQDN?**

A fully qualified domain name identifies a DNS name using its complete domain path.

**Q2. Why does a short Service name normally work in the same namespace?**

The Pod's DNS search configuration includes its namespace.

**Q3. What is the usual full DNS format for a Kubernetes Service?**

`<service>.<namespace>.svc.<cluster-domain>`.

**Q4. Is `cluster.local` always the cluster domain?**

No. It is common, but a cluster can use a different domain.

---

**Lab 33 complete.**
