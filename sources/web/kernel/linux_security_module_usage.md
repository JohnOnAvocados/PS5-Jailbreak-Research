# Linux Security Module Usage

## Source URL
https://www.kernel.org/doc/html/latest/admin-guide/LSM/index.html

## Domain
kernel.org

## System Layer (choose one)
kernel

## Summary
Overview of the Linux Security Module (LSM) framework which provides hook-based security checks via kernel extensions. Covers major LSMs: SELinux, AppArmor, Smack, Tomoyo, Yama, LoadPin, SafeSetID, IPE, and Landlock.

## Key Concepts
- LSM framework for mandatory access control (MAC)
- Build-time selection via CONFIG_DEFAULT_SECURITY
- Boot-time override via security= kernel parameter
- Major vs minor security modules
- /proc/.../attr interface for security attributes
- Capability module always included first in evaluation chain
- /sys/kernel/security/lsm lists active modules

## Security Relevance
LSM is the core extensible access control framework in Linux. In a trusted system model, LSMs enforce mandatory security policies that mediate all kernel operations, forming the reference monitor layer.

## Relevance Tags
linux, kernel, lsm, selinux, apparmor, smack, tomoyo, mac, access control, security framework
