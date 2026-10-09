# Lab 10 --- Understand port vs targetPort vs containerPort

## 1. Objective

Understand the three port fields.

## 2. Why this matters

`containerPort` documents the expected container port; it does not make
the application listen or publish it by itself. `targetPort` directs
Service traffic to the Pod port. `port` is the Service port.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
Pod fragment:
ports:
  - containerPort: 80

Service fragment:
ports:
  - port: 8080
    targetPort: 80

kubectl get pods,svc -n service-lab
kubectl get endpoints nginx-example-service -n service-lab
```

## 4. Expected result

Traffic path: client :8080 → Service :8080 → Pod :80 → Nginx listener
:80.

## 5. Common issues and resolution

No endpoints: label mismatch. Connection refused: app may not be
listening. Use unique example names to avoid overwriting existing lab
resources.

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
