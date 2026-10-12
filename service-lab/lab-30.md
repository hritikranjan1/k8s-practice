# Lab 30 — Complete Kubernetes Deployment and NodePort Application

## 1. Objective

In this lab, we will build a complete small Kubernetes application using a Deployment and a NodePort Service.

You will learn how to:

- Create resources using YAML.
- Run multiple Nginx replicas.
- Expose the Deployment using NodePort.
- Verify Service endpoints.
- Test internal and node-level access.
- Scale a Deployment.
- Observe how Kubernetes replaces a deleted Pod.
- Clean up only the resources belonging to this lab.

## 2. Theory

A Deployment maintains the desired number of Pods. A Service provides a stable network endpoint for reaching those Pods.

In this lab, the traffic path is:

```text
External client
      |
      | Node IP : NodePort
      v
NodePort Service
      |
      v
Nginx Pods managed by a Deployment
```

Inside the cluster, a client can also access the application through the Service's ClusterIP or DNS name.

A NodePort Service normally also has a ClusterIP.

## 3. Safety and prerequisites

Check the context:

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Use the intended lab cluster.

Check whether `service-lab` exists:

```bash
kubectl get namespace service-lab
```

Create it only if necessary:

```bash
kubectl create namespace service-lab
```

This lab uses a unique manifest called `service-project.yaml` and the resources `complete-web` and `complete-web-service`.

**NodePort safety:** The manifest below requests port `30090`. Before applying it, check that the port is within the configured NodePort range and is not already allocated. If it is unavailable, use an unused port and update the manifest.

## 4. Step 1 — Create the YAML manifest

Create the file:

```bash
vim service-project.yaml
```

Paste the following complete manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: complete-web
  namespace: service-lab
spec:
  replicas: 3
  selector:
    matchLabels:
      app: complete-web
  template:
    metadata:
      labels:
        app: complete-web
    spec:
      containers:
        - name: nginx
          image: nginx:stable
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: complete-web-service
  namespace: service-lab
spec:
  type: NodePort
  selector:
    app: complete-web
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30090
```

Save the file.

## 5. Step 2 — Understand the manifest

### Deployment section

- `kind: Deployment`: creates a Deployment.
- `replicas: 3`: requests three Pods.
- `selector.matchLabels`: identifies the Pods managed by this Deployment.
- `template.metadata.labels`: sets the labels on each new Pod.
- `image: nginx:stable`: uses the Nginx container image.
- `containerPort: 80`: documents the port used by the container.

The container port declaration does not, by itself, publish the application outside Kubernetes.

### Service section

- `kind: Service`: creates a Service.
- `type: NodePort`: requests node-level access.
- `selector.app: complete-web`: selects Pods with the matching label.
- `port: 80`: the Service port.
- `targetPort: 80`: the application port on the Pods.
- `nodePort: 30090`: the requested node port.

The Deployment labels and Service selector must match:

```text
Deployment Pod label: app=complete-web
Service selector:     app=complete-web
```

## 6. Step 3 — Check for a NodePort conflict

Check existing Services:

```bash
kubectl get svc -A
```

Inspect the `PORT(S)` column and look for a Service already using `30090`.

If the port is already allocated, edit the manifest:

```bash
vim service-project.yaml
```

Choose an unused port within the cluster's configured NodePort range, then save the file.

The default range is commonly `30000–32767`, but your cluster may be configured differently.

## 7. Step 4 — Validate and apply the manifest

Validate:

```bash
kubectl apply --dry-run=client -f service-project.yaml
```

Apply:

```bash
kubectl apply -f service-project.yaml
```

Wait for the Deployment rollout:

```bash
kubectl rollout status deployment/complete-web \
  -n service-lab \
  --timeout=120s
```

Check the Deployment:

```bash
kubectl get deployment complete-web -n service-lab
```

Check the Pods:

```bash
kubectl get pods -n service-lab -o wide
```

You should see three Pods managed by the Deployment if all replicas become Ready.

## 8. Step 5 — Verify the Service and endpoints

Run:

```bash
kubectl get svc complete-web-service -n service-lab -o wide
```

Inspect:

```bash
kubectl describe svc complete-web-service -n service-lab
```

Check endpoints:

```bash
kubectl get endpoints complete-web-service -n service-lab
```

Inspect EndpointSlices:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=complete-web-service
```

The Service should have backend addresses for ready Pods matching `app=complete-web`.

## 9. Step 6 — Test the application inside the cluster

Create a temporary client:

```bash
kubectl run complete-web-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/complete-web-client \
  -n service-lab \
  --timeout=120s
```

Test:

```bash
kubectl exec complete-web-client -n service-lab -- \
  curl -v http://complete-web-service:80
```

Expected result: the default Nginx HTML is returned.

## 10. Step 7 — Test through a node IP and NodePort

Get node addresses:

```bash
kubectl get nodes -o wide
```

Read the actual NodePort:

```bash
kubectl get svc complete-web-service \
  -n service-lab \
  -o jsonpath='{.spec.ports[0].nodePort}'

echo
```

From a client that can reach the node, test:

```bash
curl -v http://<NODE-IP>:30090
```

Replace `<NODE-IP>` with the actual reachable node address. If you changed the NodePort in the manifest, use the actual assigned port instead of `30090`.

If external access fails, do not immediately assume the application is broken. First confirm that the internal Service test succeeds, then check the node's reachability, firewall, and VM networking.

## 11. Step 8 — Scale from three replicas to five

Run:

```bash
kubectl scale deployment complete-web \
  --replicas=5 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl rollout status deployment/complete-web \
  -n service-lab \
  --timeout=120s
```

Check:

```bash
kubectl get deployment complete-web -n service-lab
kubectl get pods -n service-lab -o wide
kubectl get endpoints complete-web-service -n service-lab
```

When all five Pods are Ready and selected, the Service should have five backend addresses.

## 12. Step 9 — Observe Pod self-healing

List the Pods belonging to this Deployment:

```bash
kubectl get pods -n service-lab -l app=complete-web
```

Choose one Pod name from the output and delete only that Pod:

```bash
kubectl delete pod <POD-NAME> -n service-lab
```

Replace `<POD-NAME>` with an actual Pod name returned by the previous command.

Watch the Pods:

```bash
kubectl get pods -n service-lab -l app=complete-web -w
```

Press `Ctrl+C` to stop watching.

The Deployment should create a replacement Pod to maintain the desired replica count.

Do not delete the Deployment or the Service for this test.

## 13. Common issues and solutions

### Issue 1: YAML validation fails

Run:

```bash
kubectl apply --dry-run=client -f service-project.yaml
```

Check indentation, spelling, the `---` separator, and the nesting of `metadata`, `spec`, `selector`, and `ports`.

### Issue 2: NodePort is already allocated

Kubernetes will reject a conflicting fixed NodePort.

Check:

```bash
kubectl get svc -A
```

Select an unused valid port and update the manifest.

### Issue 3: Deployment Pods are not Ready

Check:

```bash
kubectl describe deployment complete-web -n service-lab
kubectl get pods -n service-lab
kubectl get events -n service-lab --sort-by=.lastTimestamp
```

Inspect individual Pod details and logs as necessary.

### Issue 4: Service has no endpoints

Check:

```bash
kubectl get pods -n service-lab --show-labels
kubectl describe svc complete-web-service -n service-lab
kubectl get endpoints complete-web-service -n service-lab
```

The Service selector and Pod labels must both use:

```text
app=complete-web
```

Also confirm the Pods are Ready.

### Issue 5: Internal access works but NodePort access fails

Check the actual NodePort, node IP, firewall rules, and VM networking.

```bash
kubectl get svc complete-web-service -n service-lab -o wide
kubectl get nodes -o wide
```

Use an IP address reachable from your test client.

### Issue 6: A deleted Pod does not immediately appear replaced

Watch the Deployment's Pods and events:

```bash
kubectl get pods -n service-lab -l app=complete-web -w
kubectl describe deployment complete-web -n service-lab
```

The replacement may need time to schedule, pull its image, and become Ready. Investigate events if it remains pending or fails to start.

## 14. What did we learn?

- A single YAML manifest can define multiple Kubernetes resources.
- A Deployment maintains the desired number of Pods.
- A NodePort Service provides node-level access when networking permits it.
- Service endpoints show which backend addresses are available.
- Scaling changes the desired replica count.
- A Deployment replaces a deleted managed Pod to maintain the replica count.

## 15. Real-world use

This pattern is useful for learning how an application is deployed, exposed, scaled, and maintained.

In production, teams also need resource requests and limits, health probes, image version control, security configuration, observability, and a suitable external entry point.

## 16. Evidence to save

```bash
kubectl get deployment complete-web -n service-lab
kubectl get pods -n service-lab -o wide
kubectl get svc complete-web-service -n service-lab -o wide
kubectl get endpoints complete-web-service -n service-lab
kubectl exec complete-web-client -n service-lab -- \
  curl -s http://complete-web-service:80
```

Record the replica count before and after scaling and what happened after deleting one Pod.

## 17. Cleanup

Delete the test client:

```bash
kubectl delete pod complete-web-client -n service-lab
```

Delete the resources created by this lab:

```bash
kubectl delete -f service-project.yaml
```

This manifest contains only the Deployment and Service created for this lab. Do not delete the whole namespace.

## 18. Interview questions

**Q1. What is the relationship between a Deployment and a Service?**

The Deployment manages Pods. The Service selects matching Pods and provides a stable endpoint to reach them.

**Q2. What happens when one Pod managed by a Deployment is deleted?**

The Deployment's controller attempts to create a replacement Pod to maintain the desired replica count.

**Q3. Why must the Service selector match the Pod labels?**

The selector determines which Pods are selected as backends.

**Q4. Does declaring `containerPort: 80` expose the application externally?**

No. The container port declaration documents the port. External access requires a suitable Service and network configuration.

---

**Lab 30 complete.**
