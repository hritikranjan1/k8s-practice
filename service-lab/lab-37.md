# Lab 37 — Troubleshoot a Kubernetes Service with the Wrong targetPort

## 1. Objective

In this lab, we will create a Service whose `targetPort` does not match the port used by Nginx, observe the connection failure, and correct the port.

You will learn:

- The difference between `port` and `targetPort`.
- Why a Service can have endpoints but still fail to connect.
- How to inspect Service ports.
- How to patch the target port.
- How to retest after fixing the configuration.

## 2. Theory

A Kubernetes Service can expose one port and forward traffic to a different port on the backend Pod.

Example:

```text
Client
  |
  | Service port 8080
  v
Service
  |
  | targetPort 80
  v
Nginx container port 80
```

The Service port is the port used by clients to access the Service. The target port is the port to which traffic is forwarded on the backend.

If the Service forwards traffic to port `8080` but Nginx is listening on port `80`, the connection may fail even if the Service has a valid endpoint.

An important distinction:

**A wrong `targetPort` does not necessarily make the endpoint list empty.** The selector can still match a ready Pod; the port configuration can simply direct traffic to the wrong destination port.

## 3. Safety and prerequisites

Check the current context:

```bash
kubectl config current-context
kubectl get nodes
```

Use the intended lab cluster.

Check the Nginx Pod:

```bash
kubectl get pod dns-nginx -n service-lab --show-labels
```

The intended label is:

```text
app=dns-nginx
```

If the Pod does not exist, create it by following `lab-31.md`.

This lab creates a separate Service named `wrong-targetport`.

## 4. Step 1 — Create a Service with the wrong targetPort

Create a ClusterIP Service:

```bash
kubectl create service clusterip wrong-targetport \
  --tcp=8080:8080 \
  -n service-lab
```

The Service initially exposes port `8080` and targets port `8080`.

Now set the selector to the intended Nginx Pod:

```bash
kubectl patch svc wrong-targetport \
  -n service-lab \
  --type=merge \
  -p '{"spec":{"selector":{"app":"dns-nginx"}}}'
```

The Service should now select the `dns-nginx` Pod, but its target port is still `8080`.

## 5. Step 2 — Inspect the configuration

Run:

```bash
kubectl describe svc wrong-targetport -n service-lab
```

Check endpoints:

```bash
kubectl get endpoints wrong-targetport -n service-lab
```

Inspect the Nginx Pod:

```bash
kubectl get pod dns-nginx -n service-lab -o wide
kubectl logs dns-nginx -n service-lab
```

The endpoint can exist even though the port is wrong. The endpoint address and port should be interpreted together.

The Nginx container normally listens on port `80`, not `8080`.

## 6. Step 3 — Test the Service with the wrong targetPort

If the `dns-client` Pod exists, run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v --connect-timeout 5 http://wrong-targetport:8080
```

Expected result: the request may fail because the Service forwards traffic to port `8080` on a Pod where Nginx normally listens on port `80`.

The exact error can vary with the networking setup. Record the actual output.

## 7. Step 4 — Fix the targetPort

Patch the Service port configuration:

```bash
kubectl patch svc wrong-targetport \
  -n service-lab \
  --type=merge \
  -p '{"spec":{"ports":[{"name":"tcp-8080","port":8080,"targetPort":80,"protocol":"TCP"}]}}'
```

This keeps the Service port at `8080` but changes the target port to `80`.

Inspect the Service:

```bash
kubectl describe svc wrong-targetport -n service-lab
```

The intended mapping is now:

```text
Service port:  8080
Target port:   80
```

## 8. Step 5 — Retest the Service

Run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://wrong-targetport:8080
```

Expected result: the Nginx welcome HTML is returned.

Check endpoints again:

```bash
kubectl get endpoints wrong-targetport -n service-lab
```

The endpoint should target port `80`.

## 9. Common issues and solutions

### Issue 1: The endpoint exists, but the connection fails

Do not assume that an endpoint guarantees that the application is listening on the configured port.

Inspect:

```bash
kubectl describe svc wrong-targetport -n service-lab
kubectl get endpoints wrong-targetport -n service-lab
kubectl logs dns-nginx -n service-lab
```

Compare `targetPort` with the actual port used by the application.

### Issue 2: The selector is wrong

Check:

```bash
kubectl get pod dns-nginx -n service-lab --show-labels
kubectl describe svc wrong-targetport -n service-lab
```

Ensure the selector is `app=dns-nginx`.

### Issue 3: The client cannot resolve the Service name

Verify the Service exists:

```bash
kubectl get svc wrong-targetport -n service-lab
```

If the name fails but direct ClusterIP access works, investigate DNS separately.

### Issue 4: The patch fails

Check the exact Service configuration:

```bash
kubectl get svc wrong-targetport -n service-lab -o yaml
```

Read the API error. Ensure the JSON is valid and that the port configuration uses the correct field names.

### Issue 5: Nginx is not running on port 80

The assumption in this lab is that the default Nginx image listens on port 80.

If you use a different image or a customized Nginx configuration, verify the application's actual listening port before changing the Service.

## 10. What did we learn?

- The Service port is not necessarily the same as the target port.
- A Service can have endpoints but still fail because it targets the wrong port.
- Port mappings must match the application's actual listening configuration.
- A controlled test before and after a fix helps confirm the root cause.

## 11. Real-world use

A backend application may listen on port `8080` while the Service exposes port `80`, or the application may use a different port than the team expects.

Verifying `port`, `targetPort`, and the actual application listener is a key troubleshooting step.

## 12. Evidence to save

```bash
kubectl describe svc wrong-targetport -n service-lab
kubectl get endpoints wrong-targetport -n service-lab
kubectl exec dns-client -n service-lab -- \
  curl -s http://wrong-targetport:8080
```

Record the failed test, the incorrect target port, the corrected mapping, and the successful retest.

## 13. Cleanup

Delete only the Service created in this lab:

```bash
kubectl delete svc wrong-targetport -n service-lab
```

Keep the shared `dns-nginx` Pod and `dns-client` if later labs need them.

## 14. Interview questions

**Q1. What is `targetPort`?**

It is the port on the backend Pod to which the Service forwards traffic.

**Q2. Can a Service have endpoints and still fail?**

Yes. The endpoint addresses may exist while the target port or application configuration is incorrect.

**Q3. How do you troubleshoot a wrong target port?**

Inspect the Service ports, endpoints, Pod health, and the actual port used by the application. Correct the mapping and retest.

**Q4. Can `port` and `targetPort` be different?**

Yes. For example, a Service can expose port `8080` and forward to port `80` on the Pod.

---

**Lab 37 complete.**
