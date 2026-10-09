# Lab 13 --- Verify EndpointSlices

## 1. Objective

Inspect the modern Kubernetes API representation of Service backends.

## 2. Why this matters

Use the `kubernetes.io/service-name` label instead of hard-coding
generated EndpointSlice names. Inspect addresses, ports, and readiness
conditions.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get endpointslice -n service-lab
kubectl get endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service
kubectl describe endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service
kubectl get endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service -o yaml
```

## 4. Expected result

Slice data contains backend Pod IPs and destination port 80.

## 5. Common issues and resolution

No matching slice: verify Service name/namespace. No endpoints: inspect
selector and Pod readiness.

## 6. What you learned

-   What Kubernetes object or behavior did you inspect/create?
-   What evidence proves the lab worked?
-   Which troubleshooting command would you run first if it failed?
-   How would this skill help in a real DevOps incident?

## 7. Real-world use case

Use this skill to diagnose service discovery, backend selection,
scaling, rolling deployments, and application connectivity. Separate Pod
health, Service configuration, endpoint selection, networking, and DNS
instead of treating them as one problem.

## 8. Lab notes to record

-   Context and namespace:
-   Pod names/IPs:
-   Service ClusterIP and port:
-   Endpoint(s) before/after:
-   Error encountered:
-   Root cause:
-   Fix and verification:
