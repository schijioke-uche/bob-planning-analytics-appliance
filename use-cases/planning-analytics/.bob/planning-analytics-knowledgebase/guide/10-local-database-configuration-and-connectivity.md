# 10. Local: database configuration and connectivity

Make every database and network path explicit.

For TM1 Local, tm1s.cfg identifies the model and its connections. The REST listener is controlled by HTTPPortNumber, which is distinct from the native database port. The API metadata exposes configuration information; use the proper endpoint rather than treating all TM1 ports as equivalent.  [R37] [R38]

| Configuration concern | Implementation action |
| --- | --- |
| Identity and directories | Assign a meaningful ServerName; keep database and logging locations outside installation media and grant only the required filesystem access. |
| Ports | Reserve distinct native and REST ports for databases on the same host; record every allowed source and destination. |
| TLS | Use trusted certificates and complete chains. Check FQDN matching, expiration, private-key protection and client trust. |
| Authentication | Select and document the supported TM1 / Cognos identity configuration for the release. Do not change modes without testing existing identities and permissions. |
| Administration | Separate business administration from OS / container access and protect management endpoints. |

## Illustrative TM1 11 configuration fragment

| ServerName=Finance<br>DataBaseDirectory=D:\PA\Models\Finance\data<br>LoggingDirectory=D:\PA\Models\Finance\logs<br>PortNumber=12345<br>HTTPPortNumber=12354<br>UseSSL=T |
| --- |

The ports and paths above are examples, not IBM-required values. This fragment omits environment-specific authentication and certificate settings; it is not a complete production configuration. Apply the correct reference parameters for your selected release.  [R37] [R38]

## Recommended verification

Check service start and logs, resolve the FQDN from each client tier, validate the TLS chain, authenticate with a non-admin account, retrieve REST metadata and open a governed cube view. A successful TCP connection alone does not validate identity or data permissions.

| AVOID UNSAFE SHORTCUTS / Do not use disabled certificate verification, broad firewall openings or a shared administrator password as a permanent fix. Diagnose the failed layer and correct that layer. |
| --- |

---
Source: user-supplied comprehensive guide, section 10. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
