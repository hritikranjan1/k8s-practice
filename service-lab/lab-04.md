# Lab 04 --- Expose an Nginx Pod Using ClusterIP

## 1. Objective

Create Service YAML and use labels to select the Pod.

## 2. Why this matters

Service selects Pods by labels, not by Pod name. The Pod must have
app=nginx to match this selector.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
Create nginx-service.yaml:
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: service-lab
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80

kubectl get pods -n service-lab --show-labels
kubectl apply -f nginx-service.yaml
kubectl get endpoints nginx-service -n service-lab
```

## 4. Expected result

Endpoint output includes the Nginx Pod IP and :80.

## 5. Common issues and resolution

No endpoints: fix labels or selector. YAML error: check
spaces/indentation. Do not delete resources just to clear an error; read
the exact error first.

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
