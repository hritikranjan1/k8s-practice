# Lab 09 --- Understand port vs targetPort

## 1. Objective

Expose Service port 8080 while forwarding to Nginx port 80.

## 2. Why this matters

Service port is where the client connects; targetPort is the destination
port on the Pod.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
Set ports in nginx-service.yaml:
ports:
  - port: 8080
    targetPort: 80

kubectl apply -f nginx-service.yaml
kubectl get svc nginx-service -n service-lab
kubectl describe svc nginx-service -n service-lab
kubectl exec -it curl-pod -n service-lab -- curl -v http://<CLUSTER-IP>:8080
```

## 4. Expected result

Service shows 8080/TCP and request to ClusterIP:8080 returns Nginx HTML.

## 5. Common issues and resolution

Request to Service port 80 should fail if only 8080 is exposed. If 8080
fails, check endpoint, selector, readiness, and targetPort.

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
