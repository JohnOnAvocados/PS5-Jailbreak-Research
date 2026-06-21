# Towards a Secure Operating System

## Source URL
https://www.microsoft.com/en-us/research/publication/towards-a-secure-operating-system/

## Domain
microsoft.com

## System Layer (choose one)
system_design

## Summary
Microsoft Research publication by Butler Lampson and colleagues discussing principles for building secure operating systems. Covers the fundamental tension between security and usability, reference monitor concepts, capability-based security, and the challenges of building trustworthy systems with a small trusted computing base.

## Key Concepts
- Reference monitor concept for mediating all access between subjects and objects
- Least privilege principle for minimizing trusted computing base
- Capability-based access control vs. access control lists
- Small trusted computing base (TCB) to reduce attack surface
- Security kernel design for enforcing mandatory access controls
- Separation of policy and mechanism in security architecture

## Security Relevance
Establishes foundational OS security design principles for trusted systems. The reference monitor concept underpins modern hypervisor and TEE security models where a small, verified layer enforces isolation between untrusted components.

## Relevance Tags
secure operating system, reference monitor, trusted computing base, capability-based security, least privilege, kernel security, mandatory access control
