# Lab 39 — Multi-Service Kubernetes Application Architecture

## 1. Objective

In this lab, we will create a small multi-Service environment with separate frontend, backend, and database-simulation components.

You will learn:

- How multiple Services can coexist in one namespace.
- How each Service selects its own Pods.
- How to access different Services using DNS names.
- How to verify endpoints for each component.
- How to think about a multi-tier application architecture.

## 2. Theory

Many applications are divided into separate components.

A common architecture contains:

- Frontend: the user-facing interface.
- Backend: the API or business-logic layer.
- Database: stores application data.

Each component may have its own Pods and Service.

```text
Client
  |
  v
Frontend Service
  |
  v
Frontend Pods

Backend Service
  |
  v
Backend Pods

Database Service
  |
  v
Database Pods
```

In a real application, the frontend calls the backend API, and the backend connects to the database.

**Important for this lab:** We will use Nginx containers for all three components. The `backend` and `database-sim` are simulations for practicing Kubernetes networking. This lab does not create a real backend API or database, and the components will not automatically communicate with one another as an application.

## 3. Safety and prerequisites

Check the current context:

```bash
kubectl config current-context
kubectl get nodes
```

Use the intended lab cluster.

Create `service-lab` only if it does not exist:

```bash
kubectl get namespace service-lab
```

If needed:

```bash
kubectl create namespace service-lab
```

This lab creates uniquely named Pods and Services. Inspect existing resources before repeating the commands.

## 4. Step 1 — Create the frontend Pod

Run:

```bash
kubectl run frontend \
  --image=nginx:stable \
  --labels=app=frontend \
  --restart=Never \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/frontend \
  -n service-lab \
  --timeout=120s
```

## 5. Step 2 — Create the backend Pod

Run:

```bash
kubectl run backend \
  --image=nginx:stable \
  --labels=app=backend \
  --restart=Never \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/backend \
  -n service-lab \
  --timeout=120s
```

This is an Nginx container used to represent a backend component. It is not a real API.

## 6. Step 3 — Create the database simulation Pod

Run:

```bash
kubectl run database-sim \
  --image=nginx:stable \
  --labels=app=database-sim \
  --restart=Never \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/database-sim \
  -n service-lab \
  --timeout=120s
```

This is also an Nginx container. It is not a database, does not store records, and does not accept database-protocol connections.

## 7. Step 4 — Create the frontend Service

Expose the frontend Pod:

```bash
kubectl expose pod frontend \
  --name=frontend-service \
  --type=ClusterIP \
  --port=80 \
  --target-port=80 \
  -n service-lab
```

Check:

```bash
kubectl get svc frontend-service -n service-lab -o wide
kubectl get endpoints frontend-service -n service-lab
```

The selector should match:

```text
app=frontend
```

## 8. Step 5 — Create the backend Service

Run:

```bash
kubectl expose pod backend \
  --name=backend-service \
  --type=ClusterIP \
  --port=8080 \
  --target-port=80 \
  -n service-lab
```

This exposes Service port `8080` and forwards traffic to port `80` on the Nginx Pod.

Check:

```bash
kubectl get svc backend-service -n service-lab -o wide
kubectl describe svc backend-service -n service-lab
kubectl get endpoints backend-service -n service-lab
```

The selector should match:

```text
app=backend
```

## 9. Step 6 — Create the database-simulation Service

Run:

```bash
kubectl expose pod database-sim \
  --name=database-service \
  --type=ClusterIP \
  --port=80 \
  --target-port=80 \
  -n service-lab
```

Check:

```bash
kubectl get svc database-service -n service-lab -o wide
kubectl get endpoints database-service -n service-lab
```

This Service only demonstrates Service discovery and routing to an Nginx container. It is not a real database endpoint.

## 10. Step 7 — Inspect the architecture

List the Pods:

```bash
kubectl get pods -n service-lab -o wide
```

List the Services:

```bash
kubectl get svc -n service-lab -o wide
```

List the endpoints:

```bash
kubectl get endpoints -n service-lab
```

Expected resources from this lab:

```text
Pods:
- frontend
- backend
- database-sim

Services:
- frontend-service
- backend-service
- database-service
```

There may be additional resources in `service-lab` from earlier labs. Do not delete those unrelated resources.

## 11. Step 8 — Create a client Pod

Create:

```bash
kubectl run architecture-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/architecture-client \
  -n service-lab \
  --timeout=120s
```

## 12. Step 9 — Test each Service

Test the frontend:

```bash
kubectl exec architecture-client -n service-lab -- \
  curl -v http://frontend-service:80
```

Test the backend simulation:

```bash
kubectl exec architecture-client -n service-lab -- \
  curl -v http://backend-service:8080
```

Test the database simulation:

```bash
kubectl exec architecture-client -n service-lab -- \
  curl -v http://database-service:80
```

Expected result: each request should return Nginx HTML when its Service and backend are configured correctly.

These tests demonstrate Kubernetes Service discovery and routing. They do not prove that a real frontend, backend API, or database integration exists.

## 13. Step 10 — Understand the real application design

In a real multi-tier application:

- Users access the frontend through a suitable external entry point.
- The frontend calls the backend API through an internal Service.
- The backend connects to the database using the database's protocol and credentials.
- The database stores application data in persistent storage where required.

A real database should use an appropriate database image and configuration, persistence, credentials stored securely, backups, monitoring, and access controls.

A real backend should implement an API. A real frontend should be configured to call that API.

This lab intentionally does not implement those application-level functions.

## 14. Common issues and solutions

### Issue 1: A Service has no endpoints

Check the Pod labels:

```bash
kubectl get pods -n service-lab --show-labels
kubectl describe svc frontend-service -n service-lab
kubectl describe svc backend-service -n service-lab
kubectl describe svc database-service -n service-lab
```

Each selector must match its intended Pod:

```text
frontend-service -> app=frontend
backend-service  -> app=backend
database-service -> app=database-sim
```

### Issue 2: A Service name does not resolve

Check:

```bash
kubectl get svc -n service-lab
kubectl exec architecture-client -n service-lab -- \
  cat /etc/resolv.conf
```

Test the ClusterIP directly to determine whether the problem is DNS or Service networking.

### Issue 3: Backend Service port confusion

The backend Service exposes port `8080`, but its target port is `80`.

Therefore, the correct URL for the test is:

```text
http://backend-service:8080
```

Do not use `http://backend-service:80` unless the Service is configured to expose port 80.

### Issue 4: The database test returns HTML

That is expected because `database-sim` is an Nginx container.

It is only a networking simulation and cannot be used as a real database.

### Issue 5: A Pod does not become Ready

Inspect:

```bash
kubectl get pods -n service-lab
kubectl describe pod <POD-NAME> -n service-lab
kubectl logs <POD-NAME> -n service-lab
```

Replace the placeholder with the actual Pod name and resolve the reported problem.

## 15. What did we learn?

- One namespace can contain multiple independent Services.
- Each Service should select the intended Pods using labels.
- Different Services can expose different ports.
- Internal DNS helps applications discover Services.
- A network simulation is not the same as a fully functioning application architecture.

## 16. Real-world use

This lab introduces the basic shape of a multi-tier system.

For production, the frontend, backend, and database would use suitable application images and configurations. The database would require persistence and secure credentials. Access controls should restrict which components can communicate.

## 17. Evidence to save

```bash
kubectl get pods -n service-lab -o wide
kubectl get svc -n service-lab -o wide
kubectl get endpoints -n service-lab
kubectl exec architecture-client -n service-lab -- \
  curl -s http://frontend-service:80
kubectl exec architecture-client -n service-lab -- \
  curl -s http://backend-service:8080
```

Record the Service names, selectors, ports, and test results.

## 18. Cleanup

Delete only the resources created by this lab:

```bash
kubectl delete pod architecture-client -n service-lab

kubectl delete svc \
  frontend-service \
  backend-service \
  database-service \
  -n service-lab

kubectl delete pod \
  frontend \
  backend \
  database-sim \
  -n service-lab
```

Do not delete the `service-lab` namespace.

## 19. Interview questions

**Q1. Why might an application use multiple Services?**

Each Service provides a stable endpoint for a different application component.

**Q2. How does the backend Service select its Pods?**

It uses a selector that matches the backend Pod labels.

**Q3. Can the frontend access a backend Service in another namespace?**

Yes, if DNS, networking, and security policies permit it. A namespace-qualified Service name can identify the target.

**Q4. Is the `database-sim` Pod a real database?**

No. It is an Nginx container used to practice Service discovery and routing.

**Q5. What should a production database require?**

Appropriate database software, secure credentials, persistence, backups, monitoring, and carefully controlled network access.

---

**Lab 39 complete.**
