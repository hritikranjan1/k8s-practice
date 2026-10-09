# Lab 03 --- Create Your First ClusterIP Service

## 1. Objective

Create an internal Service that routes to Nginx.

## 2. Why this matters

`port` is the client-facing Service port; `targetPort` is the backend
Pod port. ClusterIP is for in-cluster communication.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get pod nginx-pod -n service-lab
kubectl expose pod nginx-pod --name=nginx-service --type=ClusterIP --port=80 --target-port=80 -n service-lab
kubectl get svc nginx-service -n service-lab
kubectl describe svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
```

## 4. Expected result

Service shows TYPE ClusterIP and an IP. Endpoints should point to the
selected Nginx Pod on port 80.

## 5. Common issues and resolution

AlreadyExists: inspect existing resource. No endpoints: compare Service
selector with Pod labels and readiness.

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
