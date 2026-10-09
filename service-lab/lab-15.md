# Lab 15 --- Test Kubernetes Service Load Balancing

## 1. Objective

Give each backend a unique response and send requests through the
Service.

## 2. Why this matters

Unique content identifies which Pod replied. Use the actual Service
port. The original nginx-pod may also be a backend and return the
default page.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl exec nginx-pod-1 -n service-lab -- sh -c 'echo "Response from nginx-pod-1" > /usr/share/nginx/html/index.html'
kubectl exec nginx-pod-2 -n service-lab -- sh -c 'echo "Response from nginx-pod-2" > /usr/share/nginx/html/index.html'
kubectl exec nginx-pod-3 -n service-lab -- sh -c 'echo "Response from nginx-pod-3" > /usr/share/nginx/html/index.html'
kubectl get endpoints nginx-service -n service-lab
kubectl exec curl-pod -n service-lab -- curl -s http://<CLUSTER-IP>:8080
kubectl exec curl-pod -n service-lab -- curl -s http://<CLUSTER-IP>:8080
kubectl exec curl-pod -n service-lab -- curl -s http://<CLUSTER-IP>:8080
```

## 4. Expected result

Repeated requests may show different backend responses. A strict
round-robin sequence is not guaranteed because connection reuse and
networking implementation affect observed distribution.

## 5. Common issues and resolution

Only one endpoint: check labels. Same content: verify each file. Service
failure: test Pod IPs and inspect endpoints.

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
