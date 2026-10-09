# Lab 19 --- Change Pod Labels and Break Service Connectivity

## 1. Objective

Intentionally change one backend label and observe Service selection.

## 2. Why this matters

Service uses labels as routing metadata. Only Pods matching the selector
and eligible for traffic are included.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get pods -n service-lab -l app=nginx-scale --show-labels
kubectl label pod <POD-NAME> app=wrong-label -n service-lab --overwrite
kubectl get pod <POD-NAME> -n service-lab --show-labels
kubectl get endpoints nginx-scale-service -n service-lab
kubectl get pods -n service-lab --show-labels
```

## 4. Expected result

If the Pod remains with the changed label, its IP should disappear from
the Service endpoints. A Deployment controller may replace or reconcile
a Pod whose labels conflict with its selector.

## 5. Common issues and resolution

Pod quickly replaced: controller reconciliation may be expected.
Endpoint count changes: compare selector/labels/readiness. Never change
labels on unrelated workloads.

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
