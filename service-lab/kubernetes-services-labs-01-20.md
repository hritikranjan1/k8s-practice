# Kubernetes Services (SVC) --- Hands-on Labs 1--20

This pack contains a combined guide plus one Markdown file per lab. It
is written for DevOps beginners and includes purpose, commands, concept
explanations, expected results, troubleshooting, and takeaways.

## Lab index

1.  Lab 01 --- Kubernetes Service Environment Check
2.  Lab 02 --- Understand Pod IP vs Service IP
3.  Lab 03 --- Create Your First ClusterIP Service
4.  Lab 04 --- Expose an Nginx Pod Using ClusterIP
5.  Lab 05 --- Test Service Connectivity from Inside the Cluster
6.  Lab 06 --- Access Service Using ClusterIP
7.  Lab 07 --- Access Service Using Service DNS Name
8.  Lab 08 --- Understand Kubernetes Service Ports
9.  Lab 09 --- Understand port vs targetPort
10. Lab 10 --- Understand port vs targetPort vs containerPort
11. Lab 11 --- Service Automatically Finds Pods Using Labels
12. Lab 12 --- Verify Service Endpoints
13. Lab 13 --- Verify EndpointSlices
14. Lab 14 --- Test Service with Multiple Pods
15. Lab 15 --- Test Kubernetes Service Load Balancing
16. Lab 16 --- Scale Pods Behind a Service
17. Lab 17 --- Delete a Pod and Test Service Recovery
18. Lab 18 --- Restart Pods and Verify Service Connectivity
19. Lab 19 --- Change Pod Labels and Break Service Connectivity
20. Lab 20 --- Fix Service Selector Mismatch

## Safety

-   Work only in `service-lab`.
-   Confirm `kubectl config current-context` before practice.
-   Do not switch to or modify production-like contexts.
-   Do not delete the namespace to reset a single lab.
-   Replace placeholders (`<POD-IP>`, `<CLUSTER-IP>`, `<SERVICE-PORT>`,
    `<POD-NAME>`) with actual values and omit the angle brackets.
-   If a Service DNS name fails, test its ClusterIP separately before
    concluding the Service itself is broken.

## Common troubleshooting commands

``` bash
kubectl get pods -n service-lab -o wide
kubectl get svc -n service-lab
kubectl describe svc <SERVICE-NAME> -n service-lab
kubectl get endpoints <SERVICE-NAME> -n service-lab
kubectl get endpointslice -n service-lab
kubectl get pods -n service-lab --show-labels
kubectl get events -n service-lab --sort-by=.lastTimestamp
```

------------------------------------------------------------------------

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

------------------------------------------------------------------------

# Lab 02 --- Understand Pod IP vs Service IP

## 1. Objective

Compare a Pod address with the stable ClusterIP of a Service.

## 2. Why this matters

Pod IP belongs to one Pod and can change when the Pod is replaced.
ClusterIP is the stable in-cluster Service address.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl run nginx-pod --image=nginx:latest --labels=app=nginx -n service-lab
kubectl get pod nginx-pod -n service-lab -o wide
kubectl expose pod nginx-pod --name=nginx-service --type=ClusterIP --port=80 --target-port=80 -n service-lab
kubectl get pod nginx-pod -n service-lab -o wide
kubectl get svc nginx-service -n service-lab
```

## 4. Expected result

Pod IP and ClusterIP should be different addresses. Exact values vary.

## 5. Common issues and resolution

Pod already exists: inspect it instead of recreating it. Service already
exists: inspect it. Pod IP may coincidentally remain similar after
recreation; the lesson is that it is not guaranteed stable.

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

------------------------------------------------------------------------

# Lab 03 --- Create Your First ClusterIP Service

## 1. Objective

Create an internal Service that routes to Nginx.

## 2. Why this matters

`port` is the client-facing Service port; `targetPort` is the backend
Pod port. ClusterIP is for in-cluster communication.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get pod nginx-pod -n service-lab
kubectl expose pod nginx-pod --name=nginx-service --type=ClusterIP --port=80 --target-port=80 -n service-lab
kubectl get svc nginx-service -n service-lab
kubectl describe svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
```

## 4. Expected result

Service shows TYPE ClusterIP and an IP. Endpoints should point to the
selected Nginx Pod on port 80.

## 5. Common issues and resolution

AlreadyExists: inspect existing resource. No endpoints: compare Service
selector with Pod labels and readiness.

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

# Lab 05 --- Test Service Connectivity from Inside the Cluster

## 1. Objective

Use a temporary curl Pod to test direct Pod and Service connectivity.

## 2. Why this matters

Test Pod IP first, Service ClusterIP second, and DNS name third. This
isolates the failing layer.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl run curl-pod --image=curlimages/curl:latest -n service-lab --command -- sleep 3600
kubectl get pods -n service-lab -o wide
kubectl exec -it curl-pod -n service-lab -- curl -v http://<POD-IP>:80
kubectl get svc nginx-service -n service-lab
kubectl exec -it curl-pod -n service-lab -- curl -v http://<CLUSTER-IP>:<SERVICE-PORT>
```

## 4. Expected result

Successful requests return Nginx HTML.

## 5. Common issues and resolution

Could not resolve host means DNS issue; use ClusterIP. Connection
refused: check app/listening port. Timeout: check Pod status, endpoints,
network policy, and cluster networking.

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

------------------------------------------------------------------------

# Lab 06 --- Access Service Using ClusterIP

## 1. Objective

Call the Service through its virtual IP without DNS.

## 2. Why this matters

Use the Service port displayed by kubectl. If it is configured as 8080,
use 8080; if 80, use 80.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
kubectl exec -it curl-pod -n service-lab -- curl -v http://<CLUSTER-IP>:<SERVICE-PORT>
```

## 4. Expected result

Nginx HTML means the Service IP and backend path work.

## 5. Common issues and resolution

Wrong port: inspect `kubectl get svc`. No endpoints: check
selector/labels. ClusterIP fails: test Pod IP directly.

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

# Lab 08 --- Understand Kubernetes Service Ports

## 1. Objective

Inspect the Service port and backend port.

## 2. Why this matters

`PORT(S)` displays Service port. `targetPort` is the port on selected
Pods.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get svc nginx-service -n service-lab
kubectl describe svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
```

## 4. Expected result

For port 8080 and targetPort 80, clients connect to Service :8080 and
Nginx receives traffic on :80.

## 5. Common issues and resolution

Do not assume clients use targetPort. Check the Service's actual `port`
field.

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

------------------------------------------------------------------------

# Lab 09 --- Understand port vs targetPort

## 1. Objective

Expose Service port 8080 while forwarding to Nginx port 80.

## 2. Why this matters

Service port is where the client connects; targetPort is the destination
port on the Pod.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
Set ports in nginx-service.yaml:
ports:
  - port: 8080
    targetPort: 80

kubectl apply -f nginx-service.yaml
kubectl get svc nginx-service -n service-lab
kubectl describe svc nginx-service -n service-lab
kubectl exec -it curl-pod -n service-lab -- curl -v http://<CLUSTER-IP>:8080
```

## 4. Expected result

Service shows 8080/TCP and request to ClusterIP:8080 returns Nginx HTML.

## 5. Common issues and resolution

Request to Service port 80 should fail if only 8080 is exposed. If 8080
fails, check endpoint, selector, readiness, and targetPort.

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

# Lab 11 --- Service Automatically Finds Pods Using Labels

## 1. Objective

Verify that a Service finds Pods by matching labels.

## 2. Why this matters

Compare selector (e.g. app=nginx) with Pod labels. Eligible matching
Pods become backends.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get pods -n service-lab --show-labels
kubectl describe svc nginx-service -n service-lab
kubectl get endpoints nginx-service -n service-lab
```

## 4. Expected result

Endpoint list contains selected Pod IP(s) and target port.

## 5. Common issues and resolution

No endpoints: check selector spelling/case, labels, and Pod readiness.
Pod name does not determine selection.

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

------------------------------------------------------------------------

# Lab 12 --- Verify Service Endpoints

## 1. Objective

Identify backend IPs currently selected by a Service.

## 2. Why this matters

Compare Pod IP with endpoint address. Endpoints reflect eligible Pods
matching the Service selector.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get endpoints nginx-service -n service-lab
kubectl describe endpoints nginx-service -n service-lab
kubectl get pod nginx-pod -n service-lab -o wide
```

## 4. Expected result

Single-Pod Service normally shows `<POD-IP>:80`; multiple backends show
multiple addresses.

## 5. Common issues and resolution

`<none>`: inspect labels, selector, and readiness. A deprecation warning
means prefer EndpointSlices on newer Kubernetes; it does not alone mean
the Service is broken.

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

------------------------------------------------------------------------

# Lab 13 --- Verify EndpointSlices

## 1. Objective

Inspect the modern Kubernetes API representation of Service backends.

## 2. Why this matters

Use the `kubernetes.io/service-name` label instead of hard-coding
generated EndpointSlice names. Inspect addresses, ports, and readiness
conditions.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get endpointslice -n service-lab
kubectl get endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service
kubectl describe endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service
kubectl get endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service -o yaml
```

## 4. Expected result

Slice data contains backend Pod IPs and destination port 80.

## 5. Common issues and resolution

No matching slice: verify Service name/namespace. No endpoints: inspect
selector and Pod readiness.

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

------------------------------------------------------------------------

# Lab 14 --- Test Service with Multiple Pods

## 1. Objective

Create more Nginx Pods with the same label and confirm the Service
discovers them.

## 2. Why this matters

One Service can select multiple Pods with the same matching label. Ready
state matters.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl run nginx-pod-1 --image=nginx:latest --labels=app=nginx -n service-lab
kubectl run nginx-pod-2 --image=nginx:latest --labels=app=nginx -n service-lab
kubectl run nginx-pod-3 --image=nginx:latest --labels=app=nginx -n service-lab
kubectl get pods -n service-lab -l app=nginx -o wide
kubectl get endpoints nginx-service -n service-lab
kubectl get endpointslice -n service-lab -l kubernetes.io/service-name=nginx-service
```

## 4. Expected result

Multiple Pod IPs appear in endpoints.

## 5. Common issues and resolution

Only one endpoint: inspect labels/readiness. Image pull issue: describe
the Pod. AlreadyExists: inspect existing Pod.

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

# Lab 19 --- Change Pod Labels and Break Service Connectivity

## 1. Objective

Intentionally change one backend label and observe Service selection.

## 2. Why this matters

Service uses labels as routing metadata. Only Pods matching the selector
and eligible for traffic are included.

## 3. Hands-on steps

Run the following commands in order. Replace placeholders with values
from your own output.

``` bash
kubectl get pods -n service-lab -l app=nginx-scale --show-labels
kubectl label pod <POD-NAME> app=wrong-label -n service-lab --overwrite
kubectl get pod <POD-NAME> -n service-lab --show-labels
kubectl get endpoints nginx-scale-service -n service-lab
kubectl get pods -n service-lab --show-labels
```

## 4. Expected result

If the Pod remains with the changed label, its IP should disappear from
the Service endpoints. A Deployment controller may replace or reconcile
a Pod whose labels conflict with its selector.

## 5. Common issues and resolution

Pod quickly replaced: controller reconciliation may be expected.
Endpoint count changes: compare selector/labels/readiness. Never change
labels on unrelated workloads.

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

------------------------------------------------------------------------

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
