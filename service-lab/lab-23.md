# Lab 23 — Access an Application Using NodePort

## 1. Objective

In this lab, we will access an Nginx application through a Kubernetes node IP and a NodePort.

We will verify both internal and external access and understand why a NodePort Service can work inside Kubernetes but fail from a laptop or another machine.

## 2. Theory

A NodePort Service makes an application accessible through a node's IP address and an assigned port.

For example:

```text
Client machine
      |
      | HTTP request to NODE-IP:30080
      v
Kubernetes node
      |
      v
NodePort Service
      |
      v
Nginx Pod
```

The complete URL has this format:

```text
http://<NODE-IP>:<NODEPORT>
```

The NodePort is not necessarily the same as the Service port or the container port.

Example:

```text
Service port:   80
Target port:    80
NodePort:       30080
```

The external client uses port `30080`, while the application listens on port `80`.

## 3. Prerequisites and safety

Check the current context:

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Use the intended lab cluster.

This lab uses the resources from Lab 22. If they were deleted, create them again using the instructions in `lab-22.md`.

Check the resources:

```bash
kubectl get pod nodeport-nginx -n service-lab -o wide
kubectl get svc nodeport-service -n service-lab -o wide
kubectl get endpoints nodeport-service -n service-lab
```

If you did not create the resources in Lab 22, stop and create the Pod and Service first. Do not create duplicate resources with conflicting names.

## 4. Step 1 — Confirm the Service configuration

Run:

```bash
kubectl describe svc nodeport-service -n service-lab
```

Look for:

- Type: `NodePort`
- Port: `80`
- TargetPort: `80`
- NodePort: `30080`, or the actual port assigned to your Service
- Endpoints: an address and port for the Nginx Pod

Get the actual NodePort:

```bash
kubectl get svc nodeport-service \
  -n service-lab \
  -o jsonpath='{.spec.ports[0].nodePort}'

echo
```

Always use the port shown by the command. If the manifest used automatic allocation or was changed, it might not be `30080`.

## 5. Step 2 — Get the node IP address

Run:

```bash
kubectl get nodes -o wide
```

Example output:

```text
NAME       STATUS   ROLES           INTERNAL-IP
server-1   Ready    control-plane   192.168.1.50
```

The IP above is an example only. Your node may have a different address.

Understand the address types:

- `INTERNAL-IP`: the node's internal address.
- `EXTERNAL-IP`: an externally reachable address, if configured.
- A VM may have a private address that is not reachable from your host machine.

Choose an address that is reachable from the machine where you will run `curl`.

## 6. Step 3 — Test access from inside the cluster

If a client Pod exists from Lab 22, use it:

```bash
kubectl exec nodeport-client -n service-lab -- \
  curl -v http://nodeport-service:80
```

Expected result: Nginx returns its HTML welcome page.

This verifies that the Service can route requests internally.

If the client Pod does not exist, create one:

```bash
kubectl run nodeport-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for it:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/nodeport-client \
  -n service-lab \
  --timeout=120s
```

Then repeat the internal test.

## 7. Step 4 — Test access using the node IP

From a machine that can reach the node, run:

```bash
curl -v http://<NODE-IP>:30080
```

Replace `<NODE-IP>` with the actual reachable node IP.

Replace `30080` if your Service uses a different NodePort.

If the request succeeds, the response should contain Nginx HTML.

You can also test using a browser:

```text
http://<NODE-IP>:30080
```

Use the same reachable node IP and actual NodePort.

## 8. Step 5 — Test network reachability

If `curl` fails, first check whether the node can be reached from your client machine.

On a Linux client with `nc` installed:

```bash
nc -vz <NODE-IP> 30080
```

This tests whether a TCP connection can be established. A successful TCP connection does not by itself prove that Nginx returns the correct HTTP response.

If `nc` is not installed, use the existing network diagnostic tools available on your machine.

Check the Kubernetes resources again:

```bash
kubectl get nodes -o wide
kubectl get svc nodeport-service -n service-lab -o wide
kubectl get endpoints nodeport-service -n service-lab
kubectl get pods -n service-lab -o wide
```

## 9. Common issues and fixes

### Issue 1: `Connection timed out`

Possible causes:

- The node IP is not reachable from the client.
- The VM uses NAT and does not expose the node port to the host.
- A firewall or network ACL blocks the traffic.
- The node is not reachable through the selected network interface.

Resolution:

1. Verify the node IP using `kubectl get nodes -o wide`.
2. Verify the NodePort using `kubectl get svc`.
3. Test the Service from a client Pod.
4. Check VM networking and the relevant firewall rules.
5. Ask the network administrator before changing shared network rules.

Do not turn off all firewall protection to solve a single connectivity issue.

### Issue 2: `Connection refused`

Possible causes include the wrong node address or port, no working backend, or a node-level networking problem.

Check:

```bash
kubectl describe svc nodeport-service -n service-lab
kubectl get endpoints nodeport-service -n service-lab
kubectl logs nodeport-nginx -n service-lab
```

Use the exact NodePort shown by Kubernetes.

### Issue 3: Internal access works but host access fails

This is an important troubleshooting case.

If this works:

```bash
kubectl exec nodeport-client -n service-lab -- \
  curl -v http://nodeport-service:80
```

but the external `curl` fails, the application and internal Service path may be working. Investigate node reachability, firewall rules, VM networking, and NodePort configuration.

### Issue 4: The endpoint list is empty

Check the Service selector and the Pod's labels:

```bash
kubectl get pod nodeport-nginx -n service-lab --show-labels
kubectl describe svc nodeport-service -n service-lab
kubectl get endpoints nodeport-service -n service-lab
```

The Service selector must match the Pod label, and the Pod must be ready to receive traffic.

## 10. What did we learn?

- A NodePort is accessed using a node IP and a port.
- The actual NodePort should be read from Kubernetes, not guessed.
- Internal access and external access are separate tests.
- VM NAT and firewalls can prevent access even when Kubernetes resources are correct.
- Troubleshooting should start with the application, Service, endpoints, and actual network path.

## 11. Real-world use

A NodePort may be useful when testing an application on a small cluster or when a network appliance is configured to forward traffic to node ports.

For production applications, a managed or properly configured load balancer or ingress solution is often easier to maintain.

## 12. Evidence to save

```bash
kubectl get nodes -o wide
kubectl get svc nodeport-service -n service-lab -o wide
kubectl get endpoints nodeport-service -n service-lab
```

Record whether internal and external requests worked and, if they did not, the exact error message.

## 13. Cleanup

If this lab created the client Pod, remove only that Pod:

```bash
kubectl delete pod nodeport-client -n service-lab
```

Keep the NodePort Service and Nginx Pod if you need them for the next lab. If you want to clean up the complete Lab 22 setup, follow the cleanup section in `lab-22.md`.

## 14. Interview questions

**Q1. How do you access a NodePort Service?**

Use `http://<NODE-IP>:<NODEPORT>` from a network that can reach the node.

**Q2. Why can the NodePort work from one machine but not another?**

The machines may have different routes, firewall permissions, NAT paths, or network access.

**Q3. What does an empty endpoint list mean?**

The Service has no usable backend addresses. Check selectors, labels, and Pod readiness.

**Q4. Is NodePort the same as the container port?**

No. The NodePort is exposed on the node; the target port is where the application receives traffic inside the Pod.

---

**Lab 23 complete.**
