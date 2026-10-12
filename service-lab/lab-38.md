# Lab 38 — Kubernetes Service Port Connectivity Troubleshooting

## 1. Objective

In this lab, we will troubleshoot common Service connectivity failures by checking DNS, Service IPs, endpoints, Pod IPs, ports, and application health.

You will learn:

- A step-by-step troubleshooting sequence.
- How to identify where a connection is failing.
- How to compare DNS, ClusterIP, and Pod IP access.
- How to interpret timeout, connection-refused, and name-resolution errors.
- How to troubleshoot without randomly restarting Pods or cluster components.

## 2. Theory

A request to an application can fail at different stages.

```text
Client
  |
  v
DNS resolution
  |
  v
Service ClusterIP and port
  |
  v
Service backend endpoint
  |
  v
Application port
  |
  v
HTTP response
```

Each stage has different possible causes.

### Common error meanings

**`Could not resolve host`**

The client could not resolve the supplied hostname. Check the Service name, namespace, and DNS.

**`Connection refused`**

The connection was rejected. The destination port, application listener, or network path may be wrong.

**`Connection timed out`**

The connection did not complete within the timeout. Possible causes include routing, packet filtering, an unavailable destination, or a network problem.

These errors are clues, not absolute diagnoses. Always verify the actual configuration.

## 3. Safety and prerequisites

Check the context:

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Use the intended lab cluster.

This lab uses `dns-nginx`, `dns-nginx-service`, and `dns-client` from Lab 31. Recreate them by following `lab-31.md` if needed.

Do not change firewall rules or shared cluster networking configuration until you have evidence that the problem is in that area.

## 4. Step 1 — Check the application Pod

Run:

```bash
kubectl get pods -n service-lab -o wide
kubectl describe pod dns-nginx -n service-lab
kubectl logs dns-nginx -n service-lab
```

Confirm:

- The Pod is running.
- The Pod is Ready.
- The application starts without obvious errors.
- The Pod IP is assigned.

If the Pod is not Ready, investigate its events and container status before troubleshooting the Service.

## 5. Step 2 — Check the Service configuration

Run:

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
kubectl describe svc dns-nginx-service -n service-lab
```

Confirm:

- The Service exists in the correct namespace.
- Its selector matches the Pod labels.
- Its port is correct.
- Its target port matches the application.
- The expected Service type is configured.

Check the Pod labels:

```bash
kubectl get pod dns-nginx -n service-lab --show-labels
```

## 6. Step 3 — Check endpoints

Run:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
```

Inspect EndpointSlices:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=dns-nginx-service
```

If no suitable endpoints exist, check the selector, labels, and Pod readiness.

If the endpoint exists, compare its address and port with the actual Pod configuration.

## 7. Step 4 — Test using the Service DNS name

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v --connect-timeout 5 http://dns-nginx-service:80
```

Record the exact result.

If name resolution fails, inspect the DNS configuration:

```bash
kubectl exec dns-client -n service-lab -- cat /etc/resolv.conf
```

Check the actual DNS Service and Pods in the cluster rather than assuming their names.

## 8. Step 5 — Test using the ClusterIP

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

- Name fails, IP works: investigate DNS.
- Name and IP both fail: inspect endpoints, ports, application health, and networking.
- Both work: the internal request path is functioning for this test.

## 9. Step 6 — Test using the Pod IP

Get the Pod IP:

```bash
kubectl get pod dns-nginx -n service-lab -o wide
```

Use the actual Pod IP:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v --connect-timeout 5 http://<POD-IP>:80
```

Replace `<POD-IP>` with the current address of `dns-nginx`.

This direct test can help distinguish problems with the Service from problems with the application or Pod network.

However, Pod-to-Pod access can itself be affected by network policies and cluster networking.

## 10. Step 7 — Compare the test results

Use this diagnostic guide:

| DNS name | ClusterIP | Pod IP | Likely area to investigate |
|---|---|---|---|
| Fails | Works | Not required | DNS, Service name, namespace, cluster domain |
| Fails | Fails | Works | DNS plus Service routing, selector, or port configuration |
| Works | Fails | Works | Check whether the tests used the same port and whether Service routing is correct |
| Fails | Fails | Fails | Pod health, application listener, network policy, or cluster networking |
| Works | Works | Works | The tested path is working; investigate any different client or network path |

This table is a guide, not a guarantee. Confirm the root cause using the actual errors and configuration.

## 11. Common issues and solutions

### Issue 1: DNS failure

Check:

```bash
kubectl get svc dns-nginx-service -n service-lab
kubectl exec dns-client -n service-lab -- cat /etc/resolv.conf
```

Test the ClusterIP directly. If the IP works, investigate DNS.

### Issue 2: Empty endpoints

Check:

```bash
kubectl describe svc dns-nginx-service -n service-lab
kubectl get pods -n service-lab --show-labels
kubectl get endpoints dns-nginx-service -n service-lab
```

Correct the selector or resolve the Pod readiness problem.

### Issue 3: Wrong port

Inspect:

```bash
kubectl describe svc dns-nginx-service -n service-lab
kubectl get endpoints dns-nginx-service -n service-lab
```

Compare the Service port and target port with the application listener.

### Issue 4: Direct Pod IP works, but Service IP fails

Investigate the Service selector, endpoint addresses, Service ports, and cluster networking.

Do not recreate the Pod without evidence that the Pod is the problem.

### Issue 5: Internal access works, but NodePort access fails

Check the node IP, assigned NodePort, VM networking, routing, and firewall rules.

An internally working Service does not guarantee external node-level reachability.

## 12. What did we learn?

- Troubleshooting should follow the actual traffic path.
- DNS, ClusterIP, endpoints, Pod IP, and application ports can be tested separately.
- Error messages help identify where to investigate.
- A Service may be healthy internally while an external network path is broken.
- Evidence-based troubleshooting is safer than restarting resources at random.

## 13. Real-world use

When a user reports that an application is unavailable, DevOps engineers need to identify whether the failure is caused by DNS, Kubernetes Service configuration, application health, or network access.

Testing each layer independently helps reduce recovery time and avoids unnecessary changes.

## 14. Evidence to save

```bash
kubectl get pods -n service-lab -o wide
kubectl get svc dns-nginx-service -n service-lab -o wide
kubectl get endpoints dns-nginx-service -n service-lab
kubectl exec dns-client -n service-lab -- \
  curl -v --connect-timeout 5 http://dns-nginx-service:80
```

Record the exact output of each failed test and the successful test that isolated the problem.

## 15. Cleanup

No new Kubernetes resource is required if you use the Lab 31 resources.

If you created a temporary client Pod specifically for this lab, delete only that Pod. Keep shared resources until later labs no longer need them.

## 16. Interview questions

**Q1. What is your first step when a Service is not reachable?**

Check the application Pod, Service configuration, and endpoints before investigating more complex networking.

**Q2. How do you isolate a DNS issue?**

Compare access using the Service name with access using its ClusterIP.

**Q3. Why is direct Pod IP testing useful?**

It can help distinguish Service routing problems from application or Pod network problems.

**Q4. Why should you not restart all cluster networking components immediately?**

That can disrupt unrelated applications and hide the actual root cause. Inspect the evidence and follow the approved recovery procedure.

---

**Lab 38 complete.**
