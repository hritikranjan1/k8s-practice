# Lab 12 --- Verify Service Endpoints

## 1. Objective

Identify backend IPs currently selected by a Service.

## 2. Why this matters

Compare Pod IP with endpoint address. Endpoints reflect eligible Pods
matching the Service selector.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get endpoints nginx-service -n service-lab
kubectl describe endpoints nginx-service -n service-lab
kubectl get pod nginx-pod -n service-lab -o wide
```

## 4. Expected result

Single-Pod Service normally shows `<POD-IP>:80`; multiple backends show
multiple addresses.

## 5. Common issues and resolution

`<none>`: inspect labels, selector, and readiness. A deprecation warning
means prefer EndpointSlices on newer Kubernetes; it does not alone mean
the Service is broken.

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
