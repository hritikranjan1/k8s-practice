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
