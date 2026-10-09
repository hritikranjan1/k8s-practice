# Lab 01 --- Kubernetes Service Environment Check

## 1. Objective

Inspect cluster context, nodes, namespace, Services, and DNS components
before creating resources.

## 2. Why this matters

Check context first so commands go to the intended lab cluster. DNS
Service names differ by Kubernetes distribution; inspect actual Services
instead of assuming the name is kube-dns.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl config current-context
kubectl get nodes -o wide
kubectl get ns service-lab
kubectl get svc -A
kubectl get svc -n service-lab
kubectl get pods -n kube-system -o wide
kubectl get svc -n kube-system -o wide
```

## 4. Expected result

Cluster/nodes are visible and service-lab exists. The namespace may be
empty at the start.

## 5. Common issues and resolution

Namespace missing: kubectl create namespace service-lab. Wrong context:
stop and verify before doing anything. kube-dns not found: list Services
in kube-system and identify the actual CoreDNS Service.

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
