# 5. Prerequisites and supported environments

A supported stack is a release-specific combination, not an OS name.

Use IBM Software Product Compatibility Reports to generate the exact report for the product, release and component being installed. The interactive report, not a generic hardware checklist, is the authority for supported software and prerequisites. Archive the report with the approved deployment design.  [R07] [R25]

| Check | What to record before installation |
| --- | --- |
| Product identity | Offering, entitlement, release, database generation and every selected component version. |
| Server and runtime | OS edition / version, architecture, required libraries, container runtime and approved patch level. |
| Client stack | Browser, Windows / Office version, Excel bitness, PAfE build and required framework components. |
| Capacity | Representative model size, peak users, concurrent calculations, TI workload, memory growth and recovery objectives. |
| Network and identity | FQDNs, certificates, proxy bypasses, DNS, time synchronization, authentication mode and firewall flows. |
| Operations | Service identities, directory permissions, backup storage, monitoring, maintenance ownership and rollback artifacts. |

## Practical preparation sequence

1. Generate SPCR for the exact component set; do not reuse an older project report without checking it.

2. Record a port and certificate inventory for every environment, including connector paths and management interfaces.

3. Secure approved installation media from IBM channels and retain the associated release / fix documents.

4. Provision nonproduction first, with representative data and the same authentication approach planned for production.

5. Run concurrency, integration, restore and security tests before finalizing capacity and go-live dates.

| IMPORTANT PLATFORM BOUNDARY / A WSL Ubuntu workstation can be used for administrative tooling where appropriate. It is not evidence that TM1 Server or Workspace is supported for production on WSL or Ubuntu. Workspace Local documentation identifies supported Windows Server and RHEL paths; SPCR must confirm the exact combination. |
| --- |

For Workspace Local, use the component installation guide and its platform prerequisites, not only the data-tier requirements.  [R21]

---
Source: user-supplied comprehensive guide, section 5. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
