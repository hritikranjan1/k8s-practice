# Lab 08 --- Understand Kubernetes Service Ports

## 1. Objective

Inspect the Service port and backend port.

## 2. Why this matters

`PORT(S)` displays Service port. `targetPort` is the port on selected
Pods.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get svc nginx-service -n service-lab
kubectl describe svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
```

## 4. Expected result

For port 8080 and targetPort 80, clients connect to Service :8080 and
Nginx receives traffic on :80.

## 5. Common issues and resolution

Do not assume clients use targetPort. Check the Service's actual `port`
field.

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
