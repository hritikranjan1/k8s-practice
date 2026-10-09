# Lab 11 --- Service Automatically Finds Pods Using Labels

## 1. Objective

Verify that a Service finds Pods by matching labels.

## 2. Why this matters

Compare selector (e.g. app=nginx) with Pod labels. Eligible matching
Pods become backends.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get pods -n service-lab --show-labels
kubectl describe svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
```

## 4. Expected result

Endpoint list contains selected Pod IP(s) and target port.

## 5. Common issues and resolution

No endpoints: check selector spelling/case, labels, and Pod readiness.
Pod name does not determine selection.

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
