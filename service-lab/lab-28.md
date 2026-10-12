# Lab 28 — Change a Kubernetes Service Type

## 1. Objective

In this lab, we will change an existing Service from ClusterIP to NodePort and then change it back to ClusterIP.

You will learn:

- How to inspect an existing Service.
- How to patch a Service using `kubectl`.
- How Kubernetes assigns a NodePort.
- How to verify the result after a change.
- Why changes should be limited to lab resources.

## 2. Theory

A Service's `type` controls how the Service is exposed.

For example:

```yaml
spec:
  type: ClusterIP
```

means internal cluster access.

Changing it to:

```yaml
spec:
  type: NodePort
```

requests node-level access through a NodePort.

When a ClusterIP Service is changed to NodePort, Kubernetes normally allocates a NodePort automatically unless a valid one is specified.

Changing the type does not create a new application Pod. The Service continues to select Pods using its selector.

## 3. Safety and prerequisites

Check the active context:

```bash
kubectl config current-context
kubectl get nodes
```

This lab uses a Service named `clusterip-service` in namespace `service-lab`, created in Lab 21.

Check that it exists:

```bash
kubectl get svc clusterip-service -n service-lab
```

If it does not exist, recreate the Lab 21 Pod and Service by following `lab-21.md`.

**Important:** Patch only this lab Service. Do not change the type of an existing application or production Service.

## 4. Step 1 — Inspect the current Service

Run:

```bash
kubectl get svc clusterip-service -n service-lab -o wide
```

Inspect details:

```bash
kubectl describe svc clusterip-service -n service-lab
```

Expected current type:

```text
ClusterIP
```

Record its ClusterIP and endpoints before changing it.

## 5. Step 2 — Change ClusterIP to NodePort

Run:

```bash
kubectl patch svc clusterip-service \
  -n service-lab \
  -p '{"spec":{"type":"NodePort"}}'
```

Check the updated Service:

```bash
kubectl get svc clusterip-service -n service-lab -o wide
```

The type should now be `NodePort`.

The port display may resemble:

```text
80:30xxx/TCP
```

The actual NodePort is assigned by Kubernetes and may vary.

## 6. Step 3 — Read the assigned NodePort

Run:

```bash
kubectl get svc clusterip-service \
  -n service-lab \
  -o jsonpath='{.spec.ports[0].nodePort}'

echo
```

Inspect the Service:

```bash
kubectl describe svc clusterip-service -n service-lab
```

Verify that the Service still selects the intended Pod:

```bash
kubectl get pod clusterip-nginx -n service-lab --show-labels
kubectl get endpoints clusterip-service -n service-lab
```

The Service should continue to route traffic to the selected backend.

## 7. Step 4 — Test internal access

If the Lab 21 client Pod still exists, run:

```bash
kubectl exec clusterip-client -n service-lab -- \
  curl -v http://clusterip-service:80
```

If the client Pod was deleted, create one:

```bash
kubectl run clusterip-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait --for=condition=Ready pod/clusterip-client \
  -n service-lab --timeout=120s
```

Repeat the `curl` test.

Expected result: the Nginx welcome page is returned.

## 8. Step 5 — Change NodePort back to ClusterIP

To restore the original Service type, run:

```bash
kubectl patch svc clusterip-service \
  -n service-lab \
  -p '{"spec":{"type":"ClusterIP"}}'
```

Check:

```bash
kubectl get svc clusterip-service -n service-lab -o wide
```

The Service should now show type `ClusterIP`.

The NodePort field should no longer be present in the Service configuration.

## 9. Common issues and solutions

### Issue 1: `NotFound`

Kubernetes cannot find the Service in the specified namespace.

Check:

```bash
kubectl get svc -n service-lab
```

Use the exact name and namespace. Do not create a new Service with the same name until you have confirmed what already exists.

### Issue 2: The Service type did not change

Inspect:

```bash
kubectl describe svc clusterip-service -n service-lab
kubectl get svc clusterip-service -n service-lab -o yaml
```

Read the API response and any error message. Ensure you patched the correct namespace and resource.

### Issue 3: Internal requests fail after changing the type

Check:

```bash
kubectl get endpoints clusterip-service -n service-lab
kubectl get pods -n service-lab -o wide
kubectl describe svc clusterip-service -n service-lab
```

Changing the type should not require changing the Pod labels or target port. Investigate the actual error before changing other settings.

### Issue 4: External access still fails

Changing the type to NodePort does not automatically make the node reachable.

Check the assigned NodePort, node IP, firewall, VM networking, and routing. Test internal access first.

## 10. What did we learn?

- A Service type can be changed using `kubectl patch`.
- Changing a Service type does not recreate the backend Pod.
- Kubernetes can allocate a NodePort automatically.
- A type change should be verified by inspecting the updated Service.
- Restoring the original type is important when the change was only for practice.

## 11. Real-world use

An administrator may change a Service type when the application's access requirements change.

Such a change should be reviewed because exposing a Service through a node port can change the network paths available to clients.

## 12. Evidence to save

```bash
kubectl get svc clusterip-service -n service-lab -o wide
kubectl describe svc clusterip-service -n service-lab
kubectl get endpoints clusterip-service -n service-lab
```

Record the Service type before and after the patch.

## 13. Cleanup and restoration

This lab's cleanup is to restore the Service to ClusterIP.

```bash
kubectl patch svc clusterip-service \
  -n service-lab \
  -p '{"spec":{"type":"ClusterIP"}}'
```

If you created a new client Pod specifically for this lab, remove it:

```bash
kubectl delete pod clusterip-client -n service-lab
```

Do not delete the Lab 21 Pod or Service if you want to keep using them in your practice.

## 14. Interview questions

**Q1. Can you change ClusterIP to NodePort?**

Yes, a Service can generally be changed to NodePort using a patch or manifest update.

**Q2. Does changing the Service type recreate the Pod?**

No. It changes how the Service is exposed, not the backend Pod itself.

**Q3. How do you check the assigned NodePort?**

Use `kubectl get svc` or query `.spec.ports[0].nodePort`.

**Q4. Does NodePort guarantee external connectivity?**

No. The node IP must be reachable and network rules must permit traffic.

---

**Lab 28 complete.**
