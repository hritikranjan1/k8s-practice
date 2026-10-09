# Lab 17 --- Delete a Pod and Test Service Recovery

## 1. Objective

Delete one Deployment-managed Pod and observe replacement and endpoint
updates.

## 2. Why this matters

Delete a Pod, not the Deployment or Service. The Deployment controller
should restore the desired number of replicas.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get pods -n service-lab -l app=nginx-scale -o wide
kubectl get endpoints nginx-scale-service -n service-lab
kubectl delete pod <POD-NAME> -n service-lab
kubectl get pods -n service-lab -l app=nginx-scale -o wide
kubectl get endpoints nginx-scale-service -n service-lab
```

## 4. Expected result

Replacement Pod appears; when Ready, its IP appears in the endpoints.

## 5. Common issues and resolution

Replacement takes time: use
`kubectl get pods -n service-lab -l app=nginx-scale -w`. If it never
appears, check Deployment status/events.

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
