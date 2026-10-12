# Lab 35 — Troubleshoot a Kubernetes Service with No Endpoints

## 1. Objective

In this lab, we will investigate why a Kubernetes Service may have no endpoints.

You will learn:

- What Service endpoints are.
- Why a Service may exist but still not route traffic.
- How selectors and Pod labels work together.
- How Pod readiness affects backend selection.
- How to inspect EndpointSlices.
- How to identify the root cause before making changes.

## 2. Theory

A Service provides a stable endpoint, but it needs backend Pods to receive traffic.

For example:

```text
Service: web-service
Selector: app=web

Pod 1: app=web
Pod 2: app=web
Pod 3: app=other
```

The Service can select Pods 1 and 2 because their labels match the selector. Pod 3 is not selected.

If no suitable ready Pod matches the selector, the Service may have no usable endpoints.

A Service object can exist even when it has no endpoints. Therefore, seeing a Service in `kubectl get svc` does not prove that it can serve application traffic.

## 3. Safety and prerequisites

Check the current context:

```bash
kubectl config current-context
kubectl get nodes
```

Use the intended lab cluster.

This lab uses the resources from Lab 31:

- Pod: `dns-nginx`
- Service: `dns-nginx-service`
- Namespace: `service-lab`

If these resources do not exist, create them by following `lab-31.md`.

Do not troubleshoot or modify unrelated Services.

## 4. Step 1 — Inspect the Service

Run:

```bash
kubectl get svc dns-nginx-service -n service-lab -o wide
kubectl describe svc dns-nginx-service -n service-lab
```

Look for the selector and port configuration.

The selector should identify the intended application Pod.

## 5. Step 2 — Check endpoints

Run:

```bash
kubectl get endpoints dns-nginx-service -n service-lab
```

A Service with a usable backend should normally show one or more endpoint addresses.

If the output shows no endpoint addresses, continue investigating.

Check EndpointSlices:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=dns-nginx-service
```

EndpointSlices provide detailed information about the endpoints associated with the Service.

## 6. Step 3 — Inspect Pod labels

Run:

```bash
kubectl get pods -n service-lab --show-labels
```

Inspect the intended Pod:

```bash
kubectl get pod dns-nginx -n service-lab --show-labels
```

The Pod should have:

```text
app=dns-nginx
```

Inspect the Service selector:

```bash
kubectl describe svc dns-nginx-service -n service-lab
```

The selector and Pod label must match.

For example:

```text
Service selector: app=dns-nginx
Pod label:        app=dns-nginx
```

If the Service selector is `app=web` but the Pod label is `app=dns-nginx`, the Service will not select that Pod.

## 7. Step 4 — Check Pod readiness

Run:

```bash
kubectl get pods -n service-lab -o wide
```

Check the detailed Pod status:

```bash
kubectl describe pod dns-nginx -n service-lab
```

Inspect logs:

```bash
kubectl logs dns-nginx -n service-lab
```

A Pod that is not Ready may not be included as a normal ready backend endpoint.

Check the Pod's events for image-pull, scheduling, startup, or readiness problems.

## 8. Step 5 — Fix the actual problem

First identify the root cause.

If the Pod label is wrong, correct the Pod or the Service selector so they match.

For this lab, if the intended Pod label is `app=dns-nginx` and the Service selector is incorrect, the selector can be corrected using:

```bash
kubectl patch svc dns-nginx-service \
  -n service-lab \
  --type=merge \
  -p '{"spec":{"selector":{"app":"dns-nginx"}}}'
```

Only run this patch after confirming that `dns-nginx-service` belongs to this lab and that `app=dns-nginx` is the intended selector.

Recheck:

```bash
kubectl describe svc dns-nginx-service -n service-lab
kubectl get endpoints dns-nginx-service -n service-lab
```

If the selector is already correct, do not patch it blindly. Investigate the Pod's readiness and labels instead.

## 9. Step 6 — Test the Service

If the `dns-client` Pod exists, run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://dns-nginx-service:80
```

Expected result: the Nginx welcome page is returned.

If the request fails, check the Service endpoints again and inspect the exact error.

## 10. Common issues and solutions

### Issue 1: Service exists but endpoints are empty

Check:

```bash
kubectl describe svc dns-nginx-service -n service-lab
kubectl get pods -n service-lab --show-labels
kubectl get endpoints dns-nginx-service -n service-lab
```

Possible causes:

- Selector mismatch.
- No matching Pods.
- Pods are not Ready.
- Pods are being created or replaced.
- The wrong namespace is being inspected.

### Issue 2: The Pod is Running but not Ready

`Running` and `Ready` are not the same thing.

Inspect:

```bash
kubectl describe pod dns-nginx -n service-lab
```

Check readiness conditions, events, and container status.

### Issue 3: EndpointSlice exists but has no usable endpoint

Inspect:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=dns-nginx-service \
  -o yaml
```

Look at the endpoint addresses and conditions. A Slice object can exist without a ready endpoint.

### Issue 4: The Service is in another namespace

Services and Pods are namespaced resources.

Check:

```bash
kubectl get svc -A
kubectl get pods -A
```

Make sure you are checking the correct namespace.

## 11. What did we learn?

- A Service needs suitable backend Pods.
- Service selectors are matched against Pod labels.
- A running Pod is not necessarily Ready.
- Endpoints and EndpointSlices are useful for troubleshooting.
- A Service can exist without being able to serve traffic.

## 12. Real-world use

An application team may report that a Service exists but returns no responses.

Inspecting endpoints is a quick way to determine whether Kubernetes has selected backend Pods before investigating more complex network issues.

## 13. Evidence to save

```bash
kubectl describe svc dns-nginx-service -n service-lab
kubectl get pods -n service-lab --show-labels
kubectl get endpoints dns-nginx-service -n service-lab
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=dns-nginx-service
```

Record the cause of the empty endpoint list and the fix used.

## 14. Cleanup

No new resource is required for this lab if you use the Lab 31 resources.

If you changed the Service selector only for this exercise, restore its original intended selector when finished.

Do not delete shared application Pods or Services as a troubleshooting shortcut.

## 15. Interview questions

**Q1. What are Service endpoints?**

They identify backend addresses that a Service can route traffic to.

**Q2. Why can a Service have no endpoints?**

It may have no matching Pods, its selector may be wrong, or the matching Pods may not be Ready.

**Q3. How do you troubleshoot an empty endpoint list?**

Inspect the Service selector, Pod labels, Pod readiness, namespace, endpoints, and EndpointSlices.

**Q4. Is a Running Pod always a ready backend?**

No. Running describes the Pod phase; readiness indicates whether the Pod is considered ready to serve traffic.

---

**Lab 35 complete.**
