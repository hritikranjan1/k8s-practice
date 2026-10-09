# Lab 07 --- Access Service Using Service DNS Name

## 1. Objective

Use the short Service DNS name and fully qualified Service name.

## 2. Why this matters

DNS form is `<service>.<namespace>.svc.cluster.local`. Same-namespace
Pods can normally use just the Service name.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl exec -it curl-pod -n service-lab -- cat /etc/resolv.conf
kubectl exec -it curl-pod -n service-lab -- curl -v http://nginx-service:<SERVICE-PORT>
kubectl exec -it curl-pod -n service-lab -- curl -v http://nginx-service.service-lab.svc.cluster.local:<SERVICE-PORT>
```

## 4. Expected result

Both DNS forms should connect if DNS and Service networking work.

## 5. Common issues and resolution

Could not resolve host: inspect resolv.conf and CoreDNS Service/Pods;
test ClusterIP separately. DNS resolves but connection fails: inspect
ports/endpoints.

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
