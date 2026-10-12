# Lab 40 — Final Kubernetes Services Project

## 1. Objective

This is the final practical project for Kubernetes Services Labs 21–40.

We will deploy a small Nginx application with multiple replicas and expose it using:

- A Deployment.
- An internal ClusterIP Service.
- A NodePort Service.
- DNS-based access.
- Cross-namespace access.
- Scaling and self-healing tests.

You will learn how to combine the concepts from the earlier labs into one project and troubleshoot the complete request path.

## 2. Project architecture

The application will have three Nginx replicas.

```text
External test client
        |
        | Node IP : NodePort
        v
service-project-nodeport
        |
        v
service-project-web Pods

Internal client Pod
        |
        | Service DNS
        v
service-project-internal
        |
        v
service-project-web Pods
```

The two Services select the same application Pods.

- `service-project-internal`: ClusterIP Service for internal cluster access.
- `service-project-nodeport`: NodePort Service for access through a reachable node address.

The NodePort path depends on node reachability and network rules.

## 3. Safety and prerequisites

Check your context before making changes:

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Use the intended lab cluster.

Check whether the namespace exists:

```bash
kubectl get namespace service-lab
```

Create it only if necessary:

```bash
kubectl create namespace service-lab
```

This project creates resources with the names `service-project-web`, `service-project-internal`, and `service-project-nodeport`.

If any of these names already exist, inspect the resources before applying the manifest. Do not overwrite unrelated resources.

### NodePort safety

This manifest requests NodePort `30091`. Before applying it:

```bash
kubectl get svc -A
```

Check whether the port is already allocated. The port must also be within the configured NodePort range. The common default is `30000–32767`, but your cluster may differ.

If `30091` is unavailable, change it to an unused valid port in the manifest before applying.

## 4. Step 1 — Create the project manifest

Create:

```bash
vim service-project-final.yaml
```

Paste the following complete YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service-project-web
  namespace: service-lab
spec:
  replicas: 3
  selector:
    matchLabels:
      app: service-project-web
  template:
    metadata:
      labels:
        app: service-project-web
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
  name: service-project-internal
  namespace: service-lab
spec:
  type: ClusterIP
  selector:
    app: service-project-web
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: service-project-nodeport
  namespace: service-lab
spec:
  type: NodePort
  selector:
    app: service-project-web
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30091
```

Save the file.

## 5. Step 2 — Understand the manifest

### Deployment

The Deployment requests three Nginx replicas.

Its Pod template labels every Pod with:

```text
app=service-project-web
```

The Deployment selector matches the same label.

### ClusterIP Service

The internal Service selects:

```text
app=service-project-web
```

It exposes Service port 80 and forwards to target port 80.

### NodePort Service

The NodePort Service uses the same selector and target port, but it also requests node port `30091`.

Both Services route to the Pods matching their selectors. They do not need separate copies of the application.

## 6. Step 3 — Validate the YAML

Run:

```bash
kubectl apply --dry-run=client -f service-project-final.yaml
```

If validation succeeds, continue.

If it fails, inspect the file:

```bash
vim service-project-final.yaml
```

Check indentation, field names, and the `---` separators.

## 7. Step 4 — Apply the project

Run:

```bash
kubectl apply -f service-project-final.yaml
```

Wait for the Deployment:

```bash
kubectl rollout status deployment/service-project-web \
  -n service-lab \
  --timeout=120s
```

Check:

```bash
kubectl get deployment service-project-web -n service-lab
kubectl get pods -n service-lab -l app=service-project-web -o wide
```

The Deployment should eventually show three ready replicas.

## 8. Step 5 — Verify both Services

Run:

```bash
kubectl get svc \
  service-project-internal \
  service-project-nodeport \
  -n service-lab \
  -o wide
```

Inspect each Service:

```bash
kubectl describe svc service-project-internal -n service-lab
kubectl describe svc service-project-nodeport -n service-lab
```

Check endpoints:

```bash
kubectl get endpoints service-project-internal -n service-lab
kubectl get endpoints service-project-nodeport -n service-lab
```

Both Services should select the ready Pods matching `app=service-project-web`.

## 9. Step 6 — Test internal access using DNS

Create a temporary client Pod:

```bash
kubectl run service-project-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/service-project-client \
  -n service-lab \
  --timeout=120s
```

Test the ClusterIP Service by its short name:

```bash
kubectl exec service-project-client -n service-lab -- \
  curl -v http://service-project-internal:80
```

Expected result: the default Nginx welcome HTML is returned.

Test the NodePort Service internally by its Service name:

```bash
kubectl exec service-project-client -n service-lab -- \
  curl -v http://service-project-nodeport:80
```

This internal test uses the Service port, not the node port.

## 10. Step 7 — Test cross-namespace access

Check whether `service-client` exists:

```bash
kubectl get namespace service-client
```

Create it only if it does not exist:

```bash
kubectl create namespace service-client
```

Check whether the cross-namespace client exists:

```bash
kubectl get pod cross-namespace-client -n service-client
```

If needed, create it:

```bash
kubectl run cross-namespace-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-client
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/cross-namespace-client \
  -n service-client \
  --timeout=120s
```

Test the internal Service using its namespace-qualified name:

```bash
kubectl exec cross-namespace-client -n service-client -- \
  curl -v http://service-project-internal.service-lab:80
```

Expected result: Nginx HTML is returned if DNS and cross-namespace network access are working.

This test uses the ClusterIP Service. It does not require a NodePort or external load balancer.

## 11. Step 8 — Test NodePort access

Get the node IPs:

```bash
kubectl get nodes -o wide
```

Read the actual NodePort:

```bash
kubectl get svc service-project-nodeport \
  -n service-lab \
  -o jsonpath='{.spec.ports[0].nodePort}'

echo
```

From a machine that can reach the node, run:

```bash
curl -v http://<NODE-IP>:30091
```

Replace `<NODE-IP>` with a reachable node address. If you changed the manifest, use the actual NodePort shown by Kubernetes.

If the request fails, first verify internal access. Then check the node address, network routes, VM networking, and firewall rules.

## 12. Step 9 — Scale the application

Scale from three replicas to five:

```bash
kubectl scale deployment service-project-web \
  --replicas=5 \
  -n service-lab
```

Wait for the Deployment:

```bash
kubectl rollout status deployment/service-project-web \
  -n service-lab \
  --timeout=120s
```

Check:

```bash
kubectl get deployment service-project-web -n service-lab
kubectl get pods -n service-lab -l app=service-project-web -o wide
kubectl get endpoints service-project-internal -n service-lab
```

When all five replicas are Ready, the Service should have five suitable backend addresses.

## 13. Step 10 — Test self-healing

List the project Pods:

```bash
kubectl get pods -n service-lab -l app=service-project-web
```

Choose one Pod from the output and delete it:

```bash
kubectl delete pod <POD-NAME> -n service-lab
```

Replace `<POD-NAME>` with an actual Pod name from the previous command.

Watch the replacement:

```bash
kubectl get pods -n service-lab -l app=service-project-web -w
```

Press `Ctrl+C` to stop watching.

The Deployment should create a replacement Pod to maintain five replicas.

## 14. Step 11 — Final verification

Run:

```bash
kubectl get deployment service-project-web -n service-lab
kubectl get pods -n service-lab -l app=service-project-web -o wide
kubectl get svc service-project-internal service-project-nodeport -n service-lab -o wide
kubectl get endpoints service-project-internal -n service-lab
kubectl get endpoints service-project-nodeport -n service-lab
```

Test internal access again:

```bash
kubectl exec service-project-client -n service-lab -- \
  curl -s http://service-project-internal:80
```

Confirm that the application remains reachable after scaling and Pod replacement.

## 15. Common issues and solutions

### Issue 1: The manifest fails validation

Check the YAML indentation, field names, and separators.

```bash
kubectl apply --dry-run=client -f service-project-final.yaml
```

Fix the reported syntax or schema issue before applying again.

### Issue 2: NodePort is already allocated

Check:

```bash
kubectl get svc -A
```

Select an unused valid port and update the manifest. Do not change cluster-wide NodePort configuration for this lab.

### Issue 3: The Deployment does not reach three or five Ready replicas

Check:

```bash
kubectl describe deployment service-project-web -n service-lab
kubectl get pods -n service-lab -l app=service-project-web
kubectl get events -n service-lab --sort-by=.lastTimestamp
```

Resolve image-pull, scheduling, or container startup issues.

### Issue 4: One or both Services have no endpoints

Check:

```bash
kubectl get pods -n service-lab -l app=service-project-web --show-labels
kubectl describe svc service-project-internal -n service-lab
kubectl describe svc service-project-nodeport -n service-lab
kubectl get endpoints service-project-internal -n service-lab
kubectl get endpoints service-project-nodeport -n service-lab
```

The Service selectors must match `app=service-project-web`, and the Pods must be Ready.

### Issue 5: DNS access fails

Check the Service:

```bash
kubectl get svc service-project-internal -n service-lab
```

Inspect the client DNS configuration:

```bash
kubectl exec service-project-client -n service-lab -- \
  cat /etc/resolv.conf
```

Test the ClusterIP directly. If direct IP access works but the name fails, investigate DNS.

### Issue 6: Cross-namespace access fails

Use the namespace-qualified name:

```text
service-project-internal.service-lab
```

Check the client Pod, target Service, endpoints, DNS, and applicable NetworkPolicies.

### Issue 7: Internal access works but NodePort access fails

Check:

```bash
kubectl get svc service-project-nodeport -n service-lab -o wide
kubectl get nodes -o wide
```

Verify the node address is reachable and that the actual NodePort is permitted by the network and firewall configuration.

## 16. What did we learn?

- How to combine a Deployment and multiple Services in one project.
- How a ClusterIP Service provides internal access.
- How a NodePort Service provides node-level access when the network permits it.
- How DNS supports same-namespace and cross-namespace access.
- How endpoints help verify backend selection.
- How scaling changes the desired replica count.
- How a Deployment replaces a deleted Pod.
- How to troubleshoot the application, Service, DNS, and network path independently.

## 17. Real-world improvements

This project uses Nginx as a simple example. A production application should also consider:

- Readiness and liveness probes.
- CPU and memory requests and limits.
- Versioned container images.
- Secure configuration and secrets management.
- Monitoring, logs, and alerts.
- Ingress or LoadBalancer architecture for external access.
- NetworkPolicies where appropriate.
- TLS and application authentication.
- Deployment rollout and rollback strategies.

Do not expose internal APIs or databases publicly without an approved security design.

## 18. Evidence to save

Save the outputs of:

```bash
kubectl get deployment service-project-web -n service-lab
kubectl get pods -n service-lab -l app=service-project-web -o wide
kubectl get svc service-project-internal service-project-nodeport -n service-lab -o wide
kubectl get endpoints service-project-internal -n service-lab
kubectl get endpoints service-project-nodeport -n service-lab
```

Record:

- Initial replica count.
- Replica count after scaling.
- Service names and ports.
- Internal DNS test result.
- Cross-namespace test result.
- NodePort test result.
- What happened after deleting one Pod.

## 19. Cleanup

First delete the client Pods created for testing, if they exist:

```bash
kubectl delete pod service-project-client -n service-lab
kubectl delete pod cross-namespace-client -n service-client
```

If a client Pod does not exist, Kubernetes may report `NotFound`; that is harmless.

Delete only the project's Deployment and Services:

```bash
kubectl delete -f service-project-final.yaml
```

The manifest contains only the resources created by this capstone.

Do not delete the `service-lab` or `service-client` namespace because other labs may use them.

## 20. Interview questions

**Q1. What is the difference between ClusterIP and NodePort?**

ClusterIP is intended for internal cluster access. NodePort exposes the Service through a port on Kubernetes nodes.

**Q2. Can two Services select the same Pods?**

Yes. Multiple Services can select the same Pods while providing different access methods or ports.

**Q3. What are endpoints used for?**

They identify backend addresses that a Service can route traffic to.

**Q4. How does Kubernetes maintain five replicas after one Pod is deleted?**

The Deployment controller observes the difference between the desired and actual replica counts and attempts to create a replacement Pod.

**Q5. How would you troubleshoot a Service that cannot be accessed?**

Check Pod readiness, Service selectors, endpoints, ports, DNS, and then the relevant network path. Use the results to identify the failing layer.

---

**Lab 40 complete. You have now completed the Kubernetes Services Labs 21–40 practice sequence.**
