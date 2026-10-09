# Lab 06 --- Access Service Using ClusterIP

## 1. Objective

Call the Service through its virtual IP without DNS.

## 2. Why this matters

Use the Service port displayed by kubectl. If it is configured as 8080,
use 8080; if 80, use 80.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
kubectl exec -it curl-pod -n service-lab -- curl -v http://<CLUSTER-IP>:<SERVICE-PORT>
```

## 4. Expected result

Nginx HTML means the Service IP and backend path work.

## 5. Common issues and resolution

Wrong port: inspect `kubectl get svc`. No endpoints: check
selector/labels. ClusterIP fails: test Pod IP directly.

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
