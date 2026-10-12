# Lab 26 — LoadBalancer Behavior in RKE2 and On-Premises Kubernetes

## 1. Objective

In this lab, we will investigate how a LoadBalancer Service behaves in a self-managed RKE2 cluster.

We will learn:

- Why LoadBalancer Services may stay pending on-premises.
- How to inspect Service status and events.
- How to distinguish application problems from infrastructure integration problems.
- How to inspect nodes and system components safely.
- Why load-balancer software must be planned before installation.

## 2. Theory

Kubernetes defines the Service type `LoadBalancer`, but the actual external load balancer must be provided by an implementation integrated with the cluster.

In a managed cloud environment, the Kubernetes integration may create or configure a cloud load balancer.

In an on-premises RKE2 environment, Kubernetes may not have an external load-balancer implementation configured by default.

For example:

```text
External client
      |
      v
Load balancer or network appliance
      |
      v
RKE2 node / Service
      |
      v
Application Pod
```

Possible solutions include:

- A compatible load-balancer implementation such as MetalLB, if approved and configured for the network.
- An external hardware or software load balancer.
- An approved ingress architecture with a suitable external entry point.

These solutions are not interchangeable without considering IP address allocation, routing, firewall rules, failure handling, and the cluster network.

## 3. Safety first

This lab is primarily an inspection exercise.

Check the context:

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Use the intended lab cluster. Do not install, upgrade, or remove cluster-wide components during this lab.

If Lab 25's `loadbalancer-service` still exists, use it for inspection. If it does not exist, you may recreate the Service and Pod by following `lab-25.md`.

Do not delete or restart CoreDNS, kube-proxy-related components, CNI components, or other system workloads as part of this lab.

## 4. Step 1 — Inspect the LoadBalancer Service

Run:

```bash
kubectl get svc loadbalancer-service -n service-lab -o wide
```

Inspect details:

```bash
kubectl describe svc loadbalancer-service -n service-lab
```

Look for:

- `Type: LoadBalancer`
- `ClusterIP`
- `Port`
- `TargetPort`
- `NodePort`, if allocated
- `LoadBalancer Ingress`, if assigned
- Events related to provisioning or address allocation

If `EXTERNAL-IP` is `<pending>`, record that observation. It does not by itself mean that the Nginx Pod is broken.

## 5. Step 2 — Check the application endpoints

Run:

```bash
kubectl get pods -n service-lab -o wide
kubectl get endpoints loadbalancer-service -n service-lab
```

Inspect EndpointSlices:

```bash
kubectl get endpointslice -n service-lab \
  -l kubernetes.io/service-name=loadbalancer-service
```

Interpret the result:

- Ready endpoint present: the Service has a backend address to route to.
- No endpoint: investigate the selector, Pod labels, and readiness.
- Endpoint present but external IP pending: investigate LoadBalancer infrastructure integration separately.

This distinction prevents wasting time troubleshooting the application when the actual problem is the lack of a load-balancer implementation.

## 6. Step 3 — Inspect Kubernetes system components

List Services in the system namespace:

```bash
kubectl get svc -n kube-system -o wide
```

List system Pods:

```bash
kubectl get pods -n kube-system -o wide
```

Look for components related to the cluster's networking or load-balancer configuration.

Do not assume that a component is absent just because it has a different name than expected. RKE2 distributions and installations can use different resource names and configurations.

If your organization has a documented load-balancer implementation, inspect its relevant namespace and resources using the approved procedure.

## 7. Step 4 — Inspect node and network information

Run:

```bash
kubectl get nodes -o wide
```

Record the node addresses and determine which networks they belong to.

Questions to investigate:

- Is there a free address range for load-balancer IPs?
- Can clients route to those addresses?
- Is that range configured in the approved network plan?
- Are required firewall rules in place?
- Does the implementation support the cluster's network environment?
- What happens if a node becomes unavailable?

These questions must be answered before using an external IP range in a real environment.

## 8. Step 5 — Test internal access separately

If the lab Service has endpoints, create a client if necessary:

```bash
kubectl run lb26-client \
  --image=curlimages/curl \
  --restart=Never \
  --command -- sleep 3600 \
  -n service-lab
```

Wait for readiness:

```bash
kubectl wait \
  --for=condition=Ready \
  pod/lb26-client \
  -n service-lab \
  --timeout=120s
```

Test internal access:

```bash
kubectl exec lb26-client -n service-lab -- \
  curl -v http://loadbalancer-service:80
```

If this works while the external IP is pending, the application and internal Service path are likely working. Continue investigating the external integration.

If it fails, investigate endpoints, DNS, ports, and Pod health before drawing conclusions about the load balancer.

## 9. Common issues and solutions

### Issue 1: External IP is pending

Cause: there may be no configured implementation to allocate and advertise an external IP, or the implementation may be unable to allocate one.

Resolution:

1. Inspect `kubectl describe svc`.
2. Review the Service events.
3. Confirm the cluster's approved LoadBalancer design.
4. Check address-pool and network configuration with the cluster administrator.
5. Retest only after the integration has been configured.

### Issue 2: No endpoints

Cause: the Service selector may not match the Pod, or the Pod may not be Ready.

Check:

```bash
kubectl describe svc loadbalancer-service -n service-lab
kubectl get pods -n service-lab --show-labels
kubectl get endpoints loadbalancer-service -n service-lab
```

Correct the Service selector or application health problem.

### Issue 3: A load-balancer controller appears unhealthy

Inspect the controller's own namespace and logs according to the documented installation.

For example, once you know the actual namespace and Pod name:

```bash
kubectl get pods -n <CONTROLLER-NAMESPACE>
kubectl describe pod <CONTROLLER-POD> -n <CONTROLLER-NAMESPACE>
kubectl logs <CONTROLLER-POD> -n <CONTROLLER-NAMESPACE>
```

Replace the placeholders with actual values.

Do not guess resource names, and do not restart or delete shared infrastructure components without authorization.

### Issue 4: External IP is assigned but unreachable

An assigned IP can still fail if the network does not route it, the address is not advertised correctly, the firewall blocks traffic, or the load balancer has no healthy backends.

Check routing, address allocation, firewall policy, backend health, and the Service's endpoints.

## 10. What did we learn?

- RKE2 does not guarantee that every installation has external LoadBalancer integration.
- A LoadBalancer Service object and an external load balancer are different things.
- Endpoint health and external IP allocation are separate troubleshooting areas.
- Network address planning is required for an on-premises load balancer.
- Shared cluster networking components should not be modified casually.

## 11. Real-world use

In a data center, teams may use MetalLB or an external load-balancing appliance to provide stable IP addresses for applications.

The chosen solution must match the data center's routing, address management, security rules, and operational procedures.

## 12. Evidence to save

```bash
kubectl get svc loadbalancer-service -n service-lab -o wide
kubectl describe svc loadbalancer-service -n service-lab
kubectl get endpoints loadbalancer-service -n service-lab
kubectl get nodes -o wide
kubectl get svc -n kube-system -o wide
```

Record whether the external IP was assigned, whether endpoints existed, and whether internal testing succeeded.

## 13. Cleanup

If you created the client Pod for this lab:

```bash
kubectl delete pod lb26-client -n service-lab
```

Do not remove shared networking components. If you are finished with the Lab 25 resources, use the specific cleanup commands in `lab-25.md`.

## 14. Interview questions

**Q1. Why might LoadBalancer remain pending on an on-premises cluster?**

The cluster may not have a compatible, configured load-balancer implementation or may be unable to allocate an external address.

**Q2. What is MetalLB?**

It is a load-balancer implementation designed to provide external IP allocation and advertisement for Kubernetes environments that do not receive this functionality from a cloud provider.

**Q3. How do you distinguish an application problem from a LoadBalancer provisioning problem?**

Check the Pod readiness, Service selector, endpoints, and internal connectivity. If these work but the external address remains pending, investigate infrastructure integration.

**Q4. Should you install a load-balancer controller just to fix a lab?**

Not on a shared or production-like cluster without approval and network planning.

---

**Lab 26 complete.**
