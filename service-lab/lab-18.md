# Lab 18 --- Restart Pods and Verify Service Connectivity

## 1. Objective

Perform a rolling restart and test that Service address remains stable.

## 2. Why this matters

Service IP normally remains stable while backend Pod IPs can change
during rollout.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get svc nginx-scale-service -n service-lab
kubectl get endpoints nginx-scale-service -n service-lab
kubectl rollout restart deployment/nginx-deployment -n service-lab
kubectl rollout status deployment/nginx-deployment -n service-lab
kubectl get pods -n service-lab -l app=nginx-scale -o wide
kubectl get endpoints nginx-scale-service -n service-lab
kubectl exec -it curl-pod -n service-lab -- curl -v http://<CLUSTER-IP>:8080
```

## 4. Expected result

Rollout completes, ready endpoints exist, and ClusterIP returns Nginx
HTML.

## 5. Common issues and resolution

Rollout stuck: describe Deployment and Pods. No endpoints: check
labels/readiness. Use current ClusterIP and port from `kubectl get svc`.

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
