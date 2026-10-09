# Lab 14 --- Test Service with Multiple Pods

## 1. Objective

Create more Nginx Pods with the same label and confirm the Service
discovers them.

## 2. Why this matters

One Service can select multiple Pods with the same matching label. Ready
state matters.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl run nginx-pod-1 --image=nginx:latest --labels=app=nginx -n service-lab
kubectl run nginx-pod-2 --image=nginx:latest --labels=app=nginx -n service-lab
kubectl run nginx-pod-3 --image=nginx:latest --labels=app=nginx -n service-lab
kubectl get pods -n service-lab -l app=nginx -o wide
kubectl get endpoints nginx-service -n service-lab
kubectl get endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service
```

## 4. Expected result

Multiple Pod IPs appear in endpoints.

## 5. Common issues and resolution

Only one endpoint: inspect labels/readiness. Image pull issue: describe
the Pod. AlreadyExists: inspect existing Pod.

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
