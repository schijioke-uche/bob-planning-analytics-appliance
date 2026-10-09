# 14. Spreadsheet Services and Cognos integration

Keep modern components separate from legacy packaging.

TM1 Web is delivered as Planning Analytics Spreadsheet Services in a separate installation kit. IBM describes its independent service and directory layout and notes that separation began with the 2.0.9.2 data-tier release. It can be installed on a different host from TM1 Server.  [R29] [R30] [R04]

## Recommended implementation sequence

1. Confirm that websheets or report features actually require this component; include it in the release matrix when they do.

2. Install the matching package on a supported host using its own installation guide, paths and service account.

3. Configure database discovery, authentication and approved TLS trust between client, web service and database.

4. Integrate the endpoint with Workspace and configure EvaluationService when the selected reporting topology requires it.

5. Test real workbook patterns: selectors, calculations, action buttons, authentication, authorized write-back and export.

6. Back up configuration and custom certificates; include this service in restart, patch and disaster-recovery procedures.

The separate installer uses the IBM Planning Analytics Spreadsheet Service rather than relying on the historical Cognos Configuration workflow. Follow the current component guide rather than mixing files from legacy TM1 Web and newer Spreadsheet Services installations.  [R29]

## Cognos Analytics integration

The Local installation documentation includes Cognos integration and security paths. Treat a Cognos-based authentication design as an end-to-end identity architecture: document the namespace, relevant gateway / dispatcher routes, certificate trust and user mapping. Test the same user across all interfaces. Do not copy another environment's CAM settings blindly.  [R04]

| HISTORICAL COMPONENTS ARE NOT REQUIRED DEFAULTS / IBM's 2.0 deprecation notices identify removed or obsolete components such as Operations Console and PMHub. The newer data-tier explanation states that TM1 Applications is not part of the 2.1 release. Inventory dependencies before upgrade; do not reinstall obsolete components merely to match an old diagram. |
| --- |

Review the exact deprecation notices for the target line.  [R90] [R24] [R28]

---
Source: user-supplied comprehensive guide, section 14. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
