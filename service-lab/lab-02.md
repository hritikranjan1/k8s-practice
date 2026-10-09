# Lab 02 --- Understand Pod IP vs Service IP

## 1. Objective

Compare a Pod address with the stable ClusterIP of a Service.

## 2. Why this matters

Pod IP belongs to one Pod and can change when the Pod is replaced.
ClusterIP is the stable in-cluster Service address.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl run nginx-pod --image=nginx:latest --labels=app=nginx -n service-lab
kubectl get pod nginx-pod -n service-lab -o wide
kubectl expose pod nginx-pod --name=nginx-service --type=ClusterIP --port=80 --target-port=80 -n service-lab
kubectl get pod nginx-pod -n service-lab -o wide
kubectl get svc nginx-service -n service-lab
```

## 4. Expected result

Pod IP and ClusterIP should be different addresses. Exact values vary.

## 5. Common issues and resolution

Pod already exists: inspect it instead of recreating it. Service already
exists: inspect it. Pod IP may coincidentally remain similar after
recreation; the lesson is that it is not guaranteed stable.

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
