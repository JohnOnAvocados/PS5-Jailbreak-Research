# Understanding virtualization

## Source URL
https://www.redhat.com/en/topics/virtualization

## Domain
redhat.com

## System Layer (choose one)
hypervisor

## Summary
Red Hat's virtualization overview explains virtualization as technology that creates multiple simulated environments from a single physical hardware system using a hypervisor. It covers virtual machines (VMs), the Kernel-based Virtual Machine (KVM) hypervisor built into Linux, virtualization management, live migration, network functions virtualization (NFV), and container-native virtualization via OpenShift Virtualization. Red Hat promotes KVM as the open-source industry standard and offers OpenShift Virtualization for running VMs alongside containers in Kubernetes.

## Key Concepts
- Hypervisor abstraction of physical hardware
- Kernel-based Virtual Machine (KVM) as open-source Type-1 hypervisor
- Live migration of running VMs
- Container-native virtualization (KubeVirt)
- Network Functions Virtualization (NFV) and vRAN
- Virtualization management and orchestration
- Hyperconverged infrastructure (HCI)
- OpenShift Virtualization for hybrid cloud

## Security Relevance
Red Hat's virtualization approach emphasizes KVM as a security-hardened Type-1 hypervisor integrated into the Linux kernel. OpenShift Virtualization combines VM isolation with container orchestration, which creates a unified security model where SELinux, cgroups, and namespace isolation protect both VM and container workloads. Red Hat provides security guidance for virtualized deployments including PCI-DSS and FedRAMP compliance.

## Relevance Tags
red-hat, kvm, open-source-virtualization, opeshift-virtualization, live-migration, nfv, kubevirt, container-native-virtualization
