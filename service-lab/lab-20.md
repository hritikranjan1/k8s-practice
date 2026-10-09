# Lab 20 --- Fix Service Selector Mismatch

## 1. Objective

Restore connectivity by correcting the source of truth for
labels/selectors.

## 2. Why this matters

For Deployment-managed Pods, fix the Deployment Pod template and let the
controller reconcile it. For a standalone Pod, restore its label with
`kubectl label pod <POD-NAME> app=nginx-scale -n service-lab --overwrite`.
Change the Service selector only when the intended backend label truly
differs.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl describe svc nginx-scale-service -n service-lab
kubectl get pods -n service-lab --show-labels
kubectl get endpoints nginx-scale-service -n service-lab
kubectl get deployment nginx-deployment -n service-lab -o yaml
kubectl rollout status deployment/nginx-deployment -n service-lab
kubectl get pods -n service-lab -l app=nginx-scale --show-labels
kubectl get endpoints nginx-scale-service -n service-lab
```

## 4. Expected result

Endpoints again contain Ready Pods that match the Service selector. Test
ClusterIP and port after the endpoints return.

## 5. Common issues and resolution

Endpoints still empty: check exact label spelling/case, namespace,
selector, and readiness. Manual Pod label may be lost after recreation;
fix the Deployment template. If ClusterIP works but DNS fails,
troubleshoot DNS separately.

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
