# Lab 16 --- Scale Pods Behind a Service

## 1. Objective

Use a Deployment to scale replicas and watch the Service endpoints
adjust.

## 2. Why this matters

Deployment maintains desired replica count; Service selector matches the
Pod template labels.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
Create nginx-deployment.yaml:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: service-lab
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx-scale
  template:
    metadata:
      labels:
        app: nginx-scale
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80

Create nginx-scale-service.yaml:
apiVersion: v1
kind: Service
metadata:
  name: nginx-scale-service
  namespace: service-lab
spec:
  type: ClusterIP
  selector:
    app: nginx-scale
  ports:
    - port: 8080
      targetPort: 80

kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-scale-service.yaml
kubectl rollout status deployment/nginx-deployment -n service-lab
kubectl get endpoints nginx-scale-service -n service-lab
kubectl scale deployment nginx-deployment --replicas=5 -n service-lab
kubectl get endpoints nginx-scale-service -n service-lab
kubectl scale deployment nginx-deployment --replicas=2 -n service-lab
kubectl get endpoints nginx-scale-service -n service-lab
```

## 4. Expected result

At steady state, 3, 5, and 2 ready replicas should yield corresponding
endpoint counts.

## 5. Common issues and resolution

Fewer endpoints than replicas: wait for readiness and inspect Pod
events. Zero endpoints: compare selector and template labels. Pending
Pods: inspect resources/events.

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
