# Lab 36 — Troubleshoot a Kubernetes Service Selector Mismatch

## 1. Objective

In this lab, we will intentionally create a Service with the wrong selector, observe the missing endpoints, and fix the selector.

You will learn:

- How Service selectors work.
- How to compare selectors with Pod labels.
- How to create a controlled troubleshooting problem.
- How to use `kubectl patch` to fix a selector.
- How to retest the application after the fix.

## 2. Theory

A Service does not select a Pod simply because the Pod has a similar name.

It selects Pods by matching labels.

For example:

```text
Pod label:
app=dns-nginx

Correct Service selector:
app=dns-nginx

Incorrect Service selector:
app=wrong-label
```

The correct selector matches the Pod. The incorrect selector does not.

The result is that the Service may exist, but its endpoint list is empty.

This is one of the most common Kubernetes Service troubleshooting problems.

## 3. Safety and prerequisites

Check your current context:

```bash
kubectl config current-context
kubectl get nodes
```

Use the intended lab cluster.

This lab uses the existing Nginx Pod from Lab 31:

```text
Pod: dns-nginx
Namespace: service-lab
Label: app=dns-nginx
```

Check it:

```bash
kubectl get pod dns-nginx -n service-lab --show-labels
```

If the Pod does not exist, recreate it using `lab-31.md`.

This lab creates a separate Service named `selector-mismatch`. It does not intentionally break `dns-nginx-service`.

## 4. Step 1 — Create a Service with the wrong selector

Run:

```bash
kubectl create service clusterip selector-mismatch \
  --tcp=80:80 \
  -n service-lab
```

This command creates a ClusterIP Service.

Check it:

```bash
kubectl get svc selector-mismatch -n service-lab
```

Now set its selector to a label that the intended Pod does not have:

```bash
kubectl patch svc selector-mismatch \
  -n service-lab \
  --type=merge \
  -p '{"spec":{"selector":{"app":"wrong-label"}}}'
```

We are deliberately creating a selector mismatch for learning purposes.

## 5. Step 2 — Inspect the selector and endpoints

Run:

```bash
kubectl describe svc selector-mismatch -n service-lab
```

Check the endpoints:

```bash
kubectl get endpoints selector-mismatch -n service-lab
```

Inspect the Pod labels:

```bash
kubectl get pod dns-nginx -n service-lab --show-labels
```

The Service selector is:

```text
app=wrong-label
```

The intended Pod label is:

```text
app=dns-nginx
```

These values do not match.

The Service should therefore have no backend endpoint for this Pod.

## 6. Step 3 — Fix the selector

Correct the selector:

```bash
kubectl patch svc selector-mismatch \
  -n service-lab \
  --type=merge \
  -p '{"spec":{"selector":{"app":"dns-nginx"}}}'
```

Check the Service:

```bash
kubectl describe svc selector-mismatch -n service-lab
```

Check endpoints:

```bash
kubectl get endpoints selector-mismatch -n service-lab
```

If `dns-nginx` is Ready, the endpoint list should now contain its address.

## 7. Step 4 — Test the Service

If `dns-client` from Lab 31 exists, run:

```bash
kubectl exec dns-client -n service-lab -- \
  curl -v http://selector-mismatch:80
```

Expected result: Nginx HTML is returned.

If the request fails, inspect the endpoints again and confirm that the Pod is Ready.

## 8. Step 5 — Observe the difference

Run:

```bash
kubectl get svc selector-mismatch -n service-lab
kubectl get endpoints selector-mismatch -n service-lab
kubectl get pod dns-nginx -n service-lab --show-labels
```

Compare the results from before and after fixing the selector.

The Service object existed both before and after the fix. What changed was which Pods the Service could select.

## 9. Common issues and solutions

### Issue 1: Endpoints are still empty after fixing the selector

Check:

```bash
kubectl describe svc selector-mismatch -n service-lab
kubectl get pods -n service-lab --show-labels
kubectl get endpoints selector-mismatch -n service-lab
```

Possible causes:

- The patch used the wrong label.
- The Pod is not Ready.
- The Pod is in another namespace.
- The Pod was deleted or replaced.
- The Service is selecting a different set of labels than expected.

### Issue 2: The patch command returns an error

Check the Service name and namespace:

```bash
kubectl get svc -n service-lab
```

Read the full error message. Ensure that the patch JSON is quoted correctly.

### Issue 3: The Service exists but `curl` fails

Check the endpoint list first.

If an endpoint exists, inspect the Service port, target port, Pod health, and exact connection error.

### Issue 4: You accidentally patched the wrong Service

Inspect the target before patching:

```bash
kubectl get svc -n service-lab
kubectl describe svc <SERVICE-NAME> -n service-lab
```

Only modify the intended lab resource. If an unrelated Service was changed, stop and restore it according to its original configuration or the cluster administrator's procedure.

## 10. What did we learn?

- Service selectors match Pod labels.
- Pod names are not used to select backends.
- A selector mismatch can produce an empty endpoint list.
- Fixing the selector can restore endpoint selection without recreating the Pod.
- Verifying endpoints is an essential step in troubleshooting.

## 11. Real-world use

A developer may update an application's labels while a Service still uses the old selector.

The Service remains visible, but it stops selecting the intended Pods. Comparing the selector with actual Pod labels quickly identifies the problem.

## 12. Evidence to save

```bash
kubectl describe svc selector-mismatch -n service-lab
kubectl get pod dns-nginx -n service-lab --show-labels
kubectl get endpoints selector-mismatch -n service-lab
kubectl exec dns-client -n service-lab -- \
  curl -s http://selector-mismatch:80
```

Record the wrong selector, the empty endpoint result, the corrected selector, and the successful retest.

## 13. Cleanup

Delete only the Service created by this lab:

```bash
kubectl delete svc selector-mismatch -n service-lab
```

Keep the shared `dns-nginx` Pod and `dns-nginx-service` if later labs need them.

## 14. Interview questions

**Q1. How does a Service select Pods?**

It uses label selectors.

**Q2. Does a Service select Pods based on their names?**

No. It selects Pods using matching labels.

**Q3. What happens if the selector does not match any Pod?**

The Service may have no backend endpoints.

**Q4. How can you fix a selector mismatch?**

Compare the Service selector with the actual Pod labels, correct the selector or labels, and verify the endpoints again.

---

**Lab 36 complete.**
