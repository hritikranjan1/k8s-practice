# Lab 05 --- Test Service Connectivity from Inside the Cluster

## 1. Objective

Use a temporary curl Pod to test direct Pod and Service connectivity.

## 2. Why this matters

Test Pod IP first, Service ClusterIP second, and DNS name third. This
isolates the failing layer.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl run curl-pod --image=curlimages/curl:latest -n service-lab --command -- sleep 3600
kubectl get pods -n service-lab -o wide
kubectl exec -it curl-pod -n service-lab -- curl -v http://<POD-IP>:80
kubectl get svc nginx-service -n service-lab
kubectl exec -it curl-pod -n service-lab -- curl -v http://<CLUSTER-IP>:<SERVICE-PORT>
```

## 4. Expected result

Successful requests return Nginx HTML.

## 5. Common issues and resolution

Could not resolve host means DNS issue; use ClusterIP. Connection
refused: check app/listening port. Timeout: check Pod status, endpoints,
network policy, and cluster networking.

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
