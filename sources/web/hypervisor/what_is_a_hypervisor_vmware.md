# What is a Hypervisor? | VMware

## Source URL
https://www.vmware.com/topics/glossary/content/hypervisor.html

## Domain
vmware.com

## System Layer (choose one)
hypervisor

## Summary
VMware defines a hypervisor as software that creates and runs virtual machines by abstracting a computer's hardware from its operating system. There are two types: Type-1 (bare-metal) hypervisors run directly on physical hardware without an underlying OS, and Type-2 (hosted) hypervisors run on top of an existing operating system. VMware vSphere/ESXi is a prominent Type-1 hypervisor used in enterprise data centers for server consolidation, workload isolation, and cloud infrastructure.

## Key Concepts
- Type-1 (bare-metal) hypervisor definition
- Type-2 (hosted) hypervisor definition
- VMware ESXi as proprietary Type-1 hypervisor
- Hardware abstraction and resource partitioning
- Virtual machine isolation boundaries
- Enterprise data center virtualization
- vSphere management platform

## Security Relevance
Hypervisors are the foundational layer for virtualized trusted computing. Type-1 hypervisors (like ESXi) represent the smallest possible TCB since they lack a general-purpose OS beneath them. Understanding the Type-1 vs. Type-2 distinction is essential for evaluating the attack surface of virtualized trusted execution environments.

## Relevance Tags
vmware, esxi, type-1-hypervisor, type-2-hypervisor, enterprise-virtualization, glossary, hypervisor-definition
