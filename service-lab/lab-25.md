# Lab 25 — Create a LoadBalancer Service in Kubernetes

## 1. Objective

In this lab, we will create a Service of type `LoadBalancer` and observe how Kubernetes handles a request for an external load balancer.

You will learn:

- What a LoadBalancer Service is.
- How it differs from ClusterIP and NodePort.
- How to create a LoadBalancer Service using YAML.
- Why `EXTERNAL-IP` may remain `<pending>`.
- How to troubleshoot a LoadBalancer Service in a self-managed RKE2 cluster.

## 2. Theory: What is a LoadBalancer Service?

A LoadBalancer Service requests an external load balancer from infrastructure that supports Kubernetes LoadBalancer integration.

The general traffic path is:

```text
External client
      |
      v
External load balancer
      |
      v
Kubernetes Service
      |
      v
Application Pod
```

In a supported cloud environment, Kubernetes integration may provision or configure a load balancer and report its address through the Service status.

In an on-premises cluster, such as a self-managed RKE2 environment, a LoadBalancer Service usually needs additional infrastructure or software integration.

Creating the Service object does not, by itself, guarantee that an external load balancer will be provisioned.

## 3. Prerequisites and safety

Check your Kubernetes context:

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Make sure the intended lab cluster is selected.

Check whether `service-lab` exists:

```bash
kubectl get namespace service-lab
```

Create it only if necessary:

```bash
kubectl create namespace service-lab
```

This lab creates resources with unique names. It does not install or change cluster-wide load-balancer components.

## 4. Step 1 — Create an Nginx Pod

Create the Pod:

```bash
kubectl run lb-nginx \
  --image=nginx:stable \
  --labels=app=lb-nginx \
  --restart=Never \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/lb-nginx \
  -n service-lab \
  --timeout=120s
```

Inspect the Pod:

```bash
kubectl get pod lb-nginx -n service-lab -o wide
kubectl get pod lb-nginx -n service-lab --show-labels
```

The expected label is:

```text
app=lb-nginx
```

## 5. Step 2 — Create the LoadBalancer Service manifest

Create a YAML file:

```bash
vim loadbalancer-service.yaml
```

Paste:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: loadbalancer-service
  namespace: service-lab
spec:
  type: LoadBalancer
  selector:
    app: lb-nginx
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
```

Understand the important fields:

- `type: LoadBalancer`: requests external load-balancer integration.
- `selector`: identifies the application Pod.
- `port: 80`: the Service port.
- `targetPort: 80`: the port on the Nginx Pod.

We have not specified a fixed `nodePort`. Depending on the cluster and Service configuration, Kubernetes may allocate a NodePort as part of LoadBalancer handling.

## 6. Step 3 — Validate and apply

Validate the manifest:

```bash
kubectl apply --dry-run=client -f loadbalancer-service.yaml
```

Apply it:

```bash
kubectl apply -f loadbalancer-service.yaml
```

Inspect the Service:

```bash
kubectl get svc loadbalancer-service -n service-lab -o wide
```

Inspect details and events:

```bash
kubectl describe svc loadbalancer-service -n service-lab
kubectl get events -n service-lab --sort-by=.lastTimestamp
```

Possible output:

```text
NAME                    TYPE           CLUSTER-IP     EXTERNAL-IP
loadbalancer-service    LoadBalancer   <assigned-IP> <pending>
```

This is a possible result in a cluster without a functioning LoadBalancer implementation. It is not necessarily an application error.

## 7. Step 4 — Check endpoints

Run:

```bash
kubectl get endpoints loadbalancer-service -n service-lab
```

Also check EndpointSlices:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=loadbalancer-service
```

If the Pod is ready and its labels match the Service selector, a backend endpoint should appear.

The presence of endpoints indicates that the Service has backend addresses. It does not prove that an external load balancer has been provisioned.

## 8. Step 5 — Test internal access

Create a temporary client:

```bash
kubectl run lb-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for it:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/lb-client \
  -n service-lab \
  --timeout=120s
```

Test the Service:

```bash
kubectl exec lb-client -n service-lab -- \
  curl -v http://loadbalancer-service:80
```

Expected result: Nginx HTML is returned.

This proves internal access works. It does not prove that external load-balancer access works.

## 9. Step 6 — Understand the external IP

Run:

```bash
kubectl get svc loadbalancer-service -n service-lab -o wide
```

If an external address appears, determine whether it is actually reachable from your network before testing it.

If the address is still `<pending>`, inspect the events:

```bash
kubectl describe svc loadbalancer-service -n service-lab
kubectl get events -n service-lab --sort-by=.lastTimestamp
```

Then investigate whether the cluster has a supported LoadBalancer integration.

Do not assume that every Kubernetes cluster automatically creates a cloud or on-premises load balancer.

## 10. Common issues and solutions

### Issue 1: `EXTERNAL-IP` stays `<pending>`

Possible causes:

- No LoadBalancer implementation is installed or configured.
- The infrastructure integration is unavailable.
- The integration cannot allocate an address.
- The network or address pool is incorrectly configured.

Resolution:

1. Confirm that the Service exists.
2. Check its events and status.
3. Check whether the environment supports LoadBalancer Services.
4. Ask the cluster administrator about the configured integration.
5. For an on-premises lab, study the approved network design before adding any component.

Do not install a load-balancer implementation on a shared cluster without approval.

### Issue 2: No endpoints

Check:

```bash
kubectl get pod lb-nginx -n service-lab --show-labels
kubectl describe svc loadbalancer-service -n service-lab
kubectl get endpoints loadbalancer-service -n service-lab
```

Ensure the selector and labels match:

```text
app=lb-nginx
```

Make sure the Pod is Ready.

### Issue 3: Internal access fails

Check the Pod, Service, endpoints, and DNS:

```bash
kubectl get pods -n service-lab -o wide
kubectl get svc loadbalancer-service -n service-lab
kubectl get endpoints loadbalancer-service -n service-lab
```

Try direct ClusterIP access from the client to distinguish DNS from Service routing issues.

### Issue 4: External IP exists but access fails

An external IP alone is not sufficient evidence that the application is reachable.

Check:

- Whether the IP is routed from your client network.
- Whether firewall rules allow the Service port.
- Whether the load balancer has healthy backends.
- Whether the Service has ready endpoints.
- Whether the network integration is functioning correctly.

## 11. What did we learn?

- A LoadBalancer Service requests integration with an external load balancer.
- Kubernetes does not necessarily provide the load balancer by itself.
- An external IP may remain `<pending>` if no working implementation is available.
- Internal Service access and external load-balancer access are different.
- Endpoint health and load-balancer provisioning must be checked separately.

## 12. Real-world use

A public web application may use a cloud load balancer to accept traffic from the internet and distribute it to application Pods.

For an on-premises cluster, a compatible load-balancer implementation or network appliance must be configured to provide equivalent functionality.

## 13. Evidence to save

```bash
kubectl get svc loadbalancer-service -n service-lab -o wide
kubectl describe svc loadbalancer-service -n service-lab
kubectl get endpoints loadbalancer-service -n service-lab
kubectl exec lb-client -n service-lab -- \
  curl -s http://loadbalancer-service:80
```

Record whether the external IP was assigned or remained pending.

## 14. Cleanup

Delete only the resources created in this lab:

```bash
kubectl delete pod lb-client -n service-lab
kubectl delete svc loadbalancer-service -n service-lab
kubectl delete pod lb-nginx -n service-lab
```

## 15. Interview questions

**Q1. What is a LoadBalancer Service?**

It requests an external load balancer through supported infrastructure integration.

**Q2. Why can its external IP remain pending?**

The cluster may not have a functioning LoadBalancer implementation or may be unable to allocate an address.

**Q3. Does `type: LoadBalancer` automatically make an application public?**

No. The infrastructure, routing, address allocation, and firewall configuration must also support access.

**Q4. What is the difference between NodePort and LoadBalancer?**

NodePort exposes a port on Kubernetes nodes. LoadBalancer requests an external load-balancing endpoint and may also use NodePort internally.

---

**Lab 25 complete.**
