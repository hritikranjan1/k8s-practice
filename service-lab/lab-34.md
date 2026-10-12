# Lab 34 — Troubleshoot Kubernetes Service DNS Failure

## 1. Objective

In this lab, we will learn how to troubleshoot a Service DNS resolution failure.

You will learn how to:

- Confirm that a Service exists.
- Test the Service name and ClusterIP separately.
- Inspect the DNS configuration inside a Pod.
- Inspect Kubernetes DNS resources in an RKE2 cluster.
- Identify whether the issue is DNS, Service routing, or application health.
- Avoid unnecessary changes to cluster-wide DNS components.

## 2. Theory

When an application accesses:

```text
http://dns-nginx-service:80
```

two major steps occur:

1. DNS resolves the Service name to its ClusterIP.
2. Kubernetes networking routes traffic from that Service IP to a suitable backend Pod.

If the name cannot be resolved, the request may fail before any HTTP connection is attempted.

If the name resolves but the connection fails, the problem may be the Service, endpoints, network, or application.

A useful troubleshooting rule is:

```text
Name fails, ClusterIP works
    -> Investigate DNS first.

Name and ClusterIP both fail
    -> Investigate Service routing, endpoints, ports,
       Pod health, and network policy.
```

This is a diagnostic guideline, not an absolute rule. Confirm it using the actual error and test results.

## 3. Safety and prerequisites

Check the context:

```bash
kubectl config current-context
kubectl get nodes
```

Use the intended lab cluster.

This lab uses the existing `dns-nginx-service` and `dns-client` from Lab 31. If they do not exist, recreate them by following `lab-31.md`.

Do not delete or restart system DNS components as the first troubleshooting step.

## 4. Step 1 — Confirm that the Service exists

Run:

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
```

Inspect the configuration:

```bash
kubectl describe svc dns-nginx-service -n service-lab
```

Check the endpoints:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
```

If the Service does not exist, correct the name or namespace before troubleshooting DNS.

## 5. Step 2 — Test the Service name

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v --connect-timeout 5 http://dns-nginx-service:80
```

Record the exact result.

Possible results include:

- Nginx HTML: the request succeeded.
- `Could not resolve host`: name resolution failed.
- `Connection timed out`: a connection could not complete within the timeout.
- `Connection refused`: the connection was rejected.

These errors point toward different areas of investigation.

## 6. Step 3 — Inspect the client's DNS configuration

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  cat /etc/resolv.conf
```

Check:

- The configured nameserver.
- The DNS search domains.
- Any unusual resolver options.

The nameserver address should correspond to the DNS configuration supplied to the Pod by the cluster.

## 7. Step 4 — Test the ClusterIP directly

Get the Service IP:

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
```

Use the actual ClusterIP:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v --connect-timeout 5 http://<CLUSTER-IP>:80
```

Replace `<CLUSTER-IP>` with the actual value.

Interpretation:

- If the IP works and the name fails, DNS is a strong candidate.
- If the IP and name both fail, inspect endpoints, ports, Pod health, and network policy.
- If both work, the original failure may have been temporary or may involve a different name.

## 8. Step 5 — Inspect DNS resources in RKE2

List system Services:

```bash
kubectl get svc -n kube-system -o wide
```

List system Pods:

```bash
kubectl get pods -n kube-system -o wide
```

List EndpointSlices:

```bash
kubectl get endpointslice -n kube-system
```

Identify the DNS Service and its backing Pods using the actual output.

**Important:** Do not assume the Service is named `kube-dns`. RKE2 installations can use names such as an RKE2 CoreDNS Service.

If you have identified the DNS Service, inspect it:

```bash
kubectl describe svc <DNS-SERVICE-NAME> -n kube-system
```

Replace the placeholder with the actual name.

## 9. Step 6 — Inspect DNS Pod logs if needed

First identify the DNS Pod:

```bash
kubectl get pods -n kube-system -o wide
```

Then inspect the actual Pod's details:

```bash
kubectl describe pod <DNS-POD-NAME> -n kube-system
```

If appropriate, inspect its logs:

```bash
kubectl logs <DNS-POD-NAME> -n kube-system
```

Replace the placeholder with the actual DNS Pod name.

Look for errors that explain DNS request failures. A healthy-looking Pod alone does not prove that every DNS query works.

## 10. Step 7 — Check the Service backend

Run:

```bash
kubectl get pods -n service-lab --show-labels
kubectl get endpoints dns-nginx-service -n service-lab
kubectl describe svc dns-nginx-service -n service-lab
```

Ensure:

- The Service exists.
- Its selector matches the intended Pod.
- The Pod is Ready.
- The target port is correct.

If the Service has no endpoints, resolve that problem separately from DNS.

## 11. Common issues and solutions

### Issue 1: The Service name is incorrect

Check:

```bash
kubectl get svc -n service-lab
```

Use the exact Service name and namespace.

### Issue 2: The Service exists, but DNS fails

Inspect the Pod's `/etc/resolv.conf`, DNS Service, DNS Pods, and DNS endpoints.

Do not immediately restart CoreDNS. First gather evidence showing which component is unhealthy.

### Issue 3: ClusterIP works but DNS fails

This points toward a name-resolution issue.

Investigate:

- The client's DNS configuration.
- The DNS Service and its endpoints.
- DNS Pod health and logs.
- The actual cluster domain.
- Any network policies affecting DNS traffic.

### Issue 4: ClusterIP and DNS both fail

Investigate the Service's endpoints, Pod readiness, port mapping, and cluster networking.

### Issue 5: The DNS Service name is not `kube-dns`

Use:

```bash
kubectl get svc -n kube-system -o wide
```

Find the actual DNS Service name in the output. Do not use a guessed name.

### Issue 6: A DNS Pod appears unhealthy

Inspect its events and logs. Follow the cluster administrator's procedure before restarting or replacing any system DNS component.

## 12. What did we learn?

- DNS and Service routing are separate steps.
- The exact error message is important evidence.
- A direct ClusterIP test helps isolate DNS.
- RKE2 resource names may differ from those in other distributions.
- DNS troubleshooting should be evidence-based and should avoid unnecessary changes to shared system components.

## 13. Real-world use

A production application may report errors such as “host not found” or “temporary failure in name resolution.”

The correct response is to check DNS and the intended Service name before restarting application Pods or changing unrelated network settings.

## 14. Evidence to save

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
kubectl get endpoints dns-nginx-service -n service-lab
kubectl exec dns-client -n service-lab -- cat /etc/resolv.conf
kubectl get svc -n kube-system -o wide
kubectl get pods -n kube-system -o wide
```

Record the exact failure and the result of testing the ClusterIP directly.

## 15. Cleanup

No new cluster-wide resource is required for this troubleshooting lab.

If you created a temporary client Pod solely for this lab, delete that specific Pod. Keep the DNS Service and Pod if later labs depend on them.

## 16. Interview questions

**Q1. How do you troubleshoot a Service DNS failure?**

Verify the Service name, inspect the client's DNS configuration, test the ClusterIP directly, and inspect the cluster's DNS resources and logs.

**Q2. What does `Could not resolve host` suggest?**

The client could not resolve the supplied host name. Verify the name and investigate DNS.

**Q3. If the ClusterIP works but the name fails, what should you investigate?**

DNS configuration and DNS infrastructure.

**Q4. Should you restart CoreDNS immediately?**

No. Gather evidence first, identify the actual DNS resources, and follow the approved recovery process.

---

**Lab 34 complete.**
