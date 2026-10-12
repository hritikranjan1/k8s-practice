# Kubernetes Hands-on Labs — DevOps Learning Repository

A beginner-friendly collection of **80 hands-on Kubernetes labs** covering PersistentVolumes (PV), PersistentVolumeClaims (PVC), and Services (SVC).

This repository is designed to help DevOps beginners learn Kubernetes through practical exercises, configuration files, troubleshooting scenarios, and real-world application examples.

## Repository Overview

| Topic | Labs | What You Will Learn |
|---|---:|---|
| Kubernetes PV & PVC | 40 | Persistent storage, volume binding, storage classes, data persistence, and storage troubleshooting |
| Kubernetes Services | 40 | ClusterIP, NodePort, LoadBalancer, networking, DNS, endpoints, and connectivity troubleshooting |
| **Total** | **80** | **Kubernetes storage and networking fundamentals** |

## Learning Objectives

By completing these labs, you will learn how to:

- Understand Kubernetes storage and networking fundamentals.
- Create and configure PVs, PVCs, and Services.
- Deploy applications that use persistent storage.
- Expose applications inside and outside a Kubernetes cluster.
- Troubleshoot Pending PVCs, missing endpoints, DNS failures, and connectivity problems.
- Understand Kubernetes resource relationships and inspect them using `kubectl`.
- Practice common tasks performed by DevOps and Kubernetes engineers.

---

# Part 1 — Kubernetes PersistentVolumes & PersistentVolumeClaims

**Folder:** `kubernetes-pv-pvc/`

This section contains 40 practical labs focused on Kubernetes persistent storage, volume management, storage troubleshooting, and real-world application storage.

## Beginner Level — Storage Fundamentals

| Lab | Name | Short Description |
|---:|---|---|
| 1 | Kubernetes Storage Environment Check | Inspect the cluster, nodes, PVs, PVCs, and StorageClasses before starting storage practicals. |
| 2 | Create Your First PersistentVolume (PV) | Understand and create a PersistentVolume representing available storage. |
| 3 | Create Your First PersistentVolumeClaim (PVC) | Request storage using a PVC and inspect its status. |
| 4 | Understand PV ↔ PVC Binding | Learn how Kubernetes matches a storage claim with a suitable volume. |
| 5 | Mount PVC to an Nginx Pod | Attach persistent storage to an Nginx container. |
| 6 | Access and Inspect Mounted PVC Inside Pod | Explore a mounted volume from inside a running container. |
| 7 | Write Data to Persistent Storage | Write files to a mounted volume and verify the data. |
| 8 | Verify Persistent Data from Kubernetes Node | Understand how the underlying storage maps to the node, depending on the storage driver. |
| 9 | Delete Pod and Verify Data Persistence | Test whether data survives Pod deletion. |
| 10 | Recreate Pod and Verify Persistent Data | Mount the same claim in a replacement Pod and inspect existing data. |

## Intermediate Level — Persistence and Capacity

| Lab | Name | Short Description |
|---:|---|---|
| 11 | Complete PVC Data Persistence Test | Perform an end-to-end test of storage persistence across Pod replacement. |
| 12 | PVC Smaller Than PV | Understand how a smaller storage request can bind to a larger suitable volume. |
| 13 | PVC Larger Than PV — Pending Scenario | Observe why a claim can remain Pending when no suitable volume is available. |
| 14 | Troubleshoot Pending PVC | Investigate PVC events, volume capacity, access modes, and provisioning. |
| 15 | PVC with Wrong StorageClass | Learn how StorageClass mismatches can prevent volume binding or provisioning. |
| 16 | Reclaim Policy: Retain | Understand how storage is handled after a claim is released when the PV uses Retain. |
| 17 | Reclaim Policy: Delete | Explore Delete reclaim behavior and the effect on underlying storage, depending on the provisioner. |
| 18 | Multiple Pods Using One PVC | Explore how multiple Pods can use a claim and the limitations imposed by the storage backend. |
| 19 | ReadWriteOnce (RWO) Practical | Understand RWO access-mode behavior and its relationship to volume attachment. |
| 20 | Deployment with PVC | Deploy an application that mounts persistent storage. |

## Advanced Level — Deployment and Resource Inspection

| Lab | Name | Short Description |
|---:|---|---|
| 21 | Deployment Restart and Data Persistence | Restart or replace application Pods and verify whether stored data remains available. |
| 22 | Scale Deployment with PVC | Explore multiple replicas using a claim and understand access-mode and scheduling limitations. |
| 23 | PV, PVC and Pod Inspection & Troubleshooting Commands | Practice commands for inspecting storage resources and diagnosing problems. |
| 24 | Find Which Pod Is Using a PVC | Identify Pods that reference a particular claim. |
| 25 | Find Which PV Is Bound to a PVC | Trace a PVC to its associated PersistentVolume. |
| 26 | Find Which PVC Is Using a PV | Identify the claim associated with a volume. |
| 27 | PVC Capacity Mismatch Troubleshooting | Diagnose capacity-related binding problems. |
| 28 | Access Mode Mismatch Troubleshooting | Investigate cases where available storage does not satisfy the requested access mode. |
| 29 | StorageClass Mismatch Troubleshooting | Inspect and resolve claim and StorageClass configuration mismatches. |
| 30 | Dynamic Provisioning with StorageClass | Explore automatic volume provisioning through a configured StorageClass. |

## Real-world Storage and Troubleshooting

| Lab | Name | Short Description |
|---:|---|---|
| 31 | Understand Dynamic Provisioning Flow | Follow the process from PVC creation to dynamically provisioned storage. |
| 32 | PVC Storage Expansion | Learn how PVC expansion works when the StorageClass and storage driver support it. |
| 33 | Persistent Storage for Real-world Applications | Understand storage requirements for stateful applications and persistent application files. |
| 34 | MySQL + PV/PVC Practical | Practice connecting a database workload to persistent storage. |
| 35 | PV/PVC Failure Simulation | Study controlled storage failure scenarios and their symptoms. |
| 36 | Troubleshooting Challenge: PVC Pending | Diagnose a Pending claim using resource inspection and event messages. |
| 37 | Troubleshooting Challenge: StorageClass Mismatch | Find and correct a StorageClass configuration issue. |
| 38 | Troubleshooting Challenge: Access Mode Mismatch | Diagnose a claim that cannot find compatible storage. |
| 39 | Troubleshooting Challenge: Pod Cannot Mount PVC | Investigate Pod events, claim binding, scheduling, and volume-mount problems. |
| 40 | Final Real-world PV/PVC Mini Project | Combine storage concepts in a practical Kubernetes project. |

### Skills Covered — PV/PVC

- Persistent storage fundamentals
- PV and PVC lifecycle
- Static and dynamic provisioning
- StorageClass configuration
- Storage capacity and access modes
- Reclaim policies
- Pod and Deployment storage integration
- Database persistence
- Storage inspection and troubleshooting
- Data persistence verification

---

# Part 2 — Kubernetes Services (SVC)

**Folder:** `kubernetes-services/`

This section contains 40 hands-on labs covering Kubernetes networking, Service types, application connectivity, Service discovery, DNS, and troubleshooting.

## Beginner Level — Service Fundamentals

| Lab | Name | Short Description |
|---:|---|---|
| 1 | Kubernetes Service Environment Check | Inspect the cluster, namespaces, Pods, Services, endpoints, and DNS resources. |
| 2 | Understand Pod IP vs Service IP | Compare Pod addresses with stable Service addresses. |
| 3 | Create Your First ClusterIP Service | Create an internal Service for accessing an application. |
| 4 | Expose an Nginx Pod Using ClusterIP | Connect an Nginx Pod to a ClusterIP Service. |
| 5 | Test Service Connectivity from Inside the Cluster | Use a client Pod to test internal application connectivity. |
| 6 | Access Service Using ClusterIP | Access an application using its Service IP address. |
| 7 | Access Service Using Service DNS Name | Use Kubernetes DNS to access an application by Service name. |
| 8 | Understand Kubernetes Service Ports | Learn how the Service exposes a port for client connections. |
| 9 | Understand `port` vs `targetPort` | Compare the Service port with the destination port on the backend. |
| 10 | Understand `port` vs `targetPort` vs `containerPort` | Understand the difference between Service ports and container port declarations. |

## Intermediate Level — Pod Connectivity and Load Balancing

| Lab | Name | Short Description |
|---:|---|---|
| 11 | Service Automatically Finds Pods Using Labels | Learn how Service selectors identify matching Pods. |
| 12 | Verify Service Endpoints | Inspect the backend addresses associated with a Service. |
| 13 | Verify EndpointSlices | Explore EndpointSlices and their role in tracking Service backends. |
| 14 | Test Service with Multiple Pods | Connect a Service to multiple application Pods. |
| 15 | Test Kubernetes Service Load Balancing | Observe traffic distribution across eligible backends. |
| 16 | Scale Pods Behind a Service | Increase replicas and inspect the Service's backend endpoints. |
| 17 | Delete a Pod and Test Service Recovery | Observe how a Deployment replaces a deleted Pod and how Service backends update. |
| 18 | Restart Pods and Verify Service Connectivity | Verify connectivity as application Pods restart or are replaced. |
| 19 | Change Pod Labels and Break Service Connectivity | See how an incorrect label can cause a Service to lose its matching backends. |
| 20 | Fix Service Selector Mismatch | Correct a Service selector so that it matches the intended Pods. |

## Advanced Level — Service Types and Deployment

| Lab | Name | Short Description |
|---:|---|---|
| 21 | Create ClusterIP Service | Create and verify an internal-only Service. |
| 22 | Create NodePort Service | Expose a Service on a port of the Kubernetes nodes. |
| 23 | Access Application Using NodePort | Test an application using a reachable node IP and assigned NodePort. |
| 24 | Understand NodePort Port Range | Explore automatic NodePort allocation and the configured port range. |
| 25 | Create LoadBalancer Service | Create a Service that requests external load-balancer integration. |
| 26 | Understand LoadBalancer Behavior in RKE2/On-Prem | Investigate LoadBalancer behavior in self-managed and on-premises clusters. |
| 27 | Compare ClusterIP vs NodePort vs LoadBalancer | Understand the differences and typical use cases of the three Service types. |
| 28 | Change Service Type | Change a lab Service type and verify the result. |
| 29 | Expose an Existing Deployment Using a Service | Expose a Deployment without manually creating individual backend connections. |
| 30 | Service + Deployment Complete Application | Combine a Deployment and NodePort Service in an end-to-end exercise. |

## DNS and Internal Communication

| Lab | Name | Short Description |
|---:|---|---|
| 31 | Kubernetes Service DNS Resolution | Test Service-name resolution and application access from a client Pod. |
| 32 | Access Service from Another Namespace | Connect to a Service in a different namespace using a namespace-qualified DNS name. |
| 33 | Understand Short DNS Name vs FQDN | Compare short Service names with fully qualified Service DNS names. |
| 34 | Troubleshoot Service DNS Failure | Inspect DNS configuration and distinguish DNS issues from Service connectivity issues. |
| 35 | Troubleshoot Service with No Endpoints | Diagnose Services that have no eligible backend Pods. |

## Real-world Architecture and Troubleshooting

| Lab | Name | Short Description |
|---:|---|---|
| 36 | Service Selector Mismatch Troubleshooting | Identify and correct incorrect Service selectors. |
| 37 | Wrong `targetPort` Troubleshooting | Diagnose traffic failures caused by an incorrect backend port. |
| 38 | Service Port Connectivity Troubleshooting | Investigate failures involving DNS, Service IPs, Pod IPs, ports, and node networking. |
| 39 | Multi-Service Application Architecture | Explore how multiple application components can communicate through separate Services. |
| 40 | Final Real-world Kubernetes Service Project | Build and test an application exposed through internal and NodePort Services. |

### Skills Covered — Services

- ClusterIP, NodePort, and LoadBalancer
- Pod IP versus Service IP
- Service selectors and labels
- Service ports and target ports
- Endpoints and EndpointSlices
- Kubernetes DNS and namespace-based discovery
- Application connectivity testing
- Deployment scaling and Pod replacement
- On-premises networking concepts
- Service troubleshooting and multi-Service architecture

---

# Suggested Repository Structure

```text
kubernetes-labs/
├── README.md
│
├── kubernetes-pv-pvc/
│   ├── lab-01-storage-environment-check.md
│   ├── lab-02-create-first-pv.md
│   ├── lab-03-create-first-pvc.md
│   ├── ...
│   └── lab-40-final-pv-pvc-project.md
│
└── kubernetes-services/
    ├── lab-01-service-environment-check.md
    ├── lab-02-pod-ip-vs-service-ip.md
    ├── lab-03-create-clusterip-service.md
    ├── ...
    └── lab-40-final-service-project.md
```

**Note:** The filenames above are examples to illustrate the folder layout. Keep the actual filenames already present in your repository, and update the paths or links in this README to match them.

## Recommended Learning Order

1. Complete PV/PVC Labs 1–10 to understand storage fundamentals.
2. Complete PV/PVC Labs 11–22 to practice persistence and Deployment integration.
3. Complete PV/PVC Labs 23–40 to develop troubleshooting and real-world storage skills.
4. Complete Services Labs 1–10 to understand basic networking and ports.
5. Complete Services Labs 11–30 to practice Service backends and Service types.
6. Complete Services Labs 31–40 to learn DNS, connectivity troubleshooting, and application architecture.

## Safety Notes

- Verify `kubectl config current-context` before making changes.
- Use only the Kubernetes cluster approved for practice.
- Inspect existing resources before creating or deleting resources.
- Avoid deleting shared namespaces or production application resources.
- Test LoadBalancer behavior according to the cluster's actual infrastructure.
- Remember that storage access modes and persistence behavior depend on the storage driver and backend.

## About This Repository

This repository documents hands-on Kubernetes learning for DevOps practice. It is intended for beginners who want to understand Kubernetes concepts by running commands, inspecting resources, troubleshooting common failures, and building practical projects.

The goal is to develop practical skills that can be applied to real DevOps environments and used as a reference during revision and interview preparation.

