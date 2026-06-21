# AWS Nitro System

## Source URL
https://aws.amazon.com/ec2/nitro/

## Domain
aws.amazon.com

## System Layer (choose one)
system_design

## Summary
AWS Nitro System is the virtualization infrastructure for EC2 instances. Composed of dedicated Nitro Cards (offloading VPC, EBS, instance storage), Nitro Security Chip, a lightweight Nitro Hypervisor, and Nitro Enclaves for isolated compute environments. Delivers near bare-metal performance by offloading virtualization functions to dedicated hardware.

## Key Concepts
- Nitro Cards offload and accelerate network (VPC), storage (EBS), and I/O functions
- Nitro Security Chip locks down administrative access (including Amazon employees)
- Nitro Hypervisor provides CPU/memory isolation with near bare-metal performance
- Nitro Enclaves create isolated compute environments for sensitive data processing
- NitroTPM provides TPM 2.0 functionality for attestation and key storage
- Isolation Engine enforces mathematical guarantees of instance separation
- Supports bare metal instances allowing customer-owned hypervisors

## Security Relevance
Represents a major commercial hypervisor security architecture. Nitro's dedicated hardware approach minimizes attack surface by removing software virtualization layers. The locked-down administrative model (no human access) is a significant trust architecture pattern applicable to any system where the platform owner must be excluded from the trusted computing base.

## Relevance Tags
aws, nitro, hypervisor, hardware isolation, virtualization security, trusted execution, enclave, tpm
