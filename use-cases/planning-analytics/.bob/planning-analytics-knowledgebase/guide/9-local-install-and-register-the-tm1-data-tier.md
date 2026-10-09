# 9. Local: install and register the TM1 data tier

Apply the exact release procedure to supported Windows or Linux hosts.

The data-tier guide for 2.0.9.21 and later lists TM1 Server, Admin Server, tools, samples, core-dump support and the Administration agent. IBM changed the installer at that boundary and removed Cognos Configuration from the new data-tier installation. Older installation screenshots therefore need careful interpretation.  [R23] [R24]

## Recommended installation sequence

1. Obtain the matching IBM installation kit and read its prerequisites and upgrade notes. Confirm SPCR, platform, disk layout and service accounts.

2. For an upgrade, capture a restorable backup and the previous service definitions before uninstalling or replacing anything.

3. Keep production model data outside the product installation directory. Record separate data, log, backup and installation locations.

4. Run the supported installer, select the required components and retain the installer log.

5. Create / restore the database configuration and use the documented platform-specific service registration or startup procedure.

6. Start the Admin Server and database as applicable; verify logs and connectivity before enabling scheduled jobs.

## Windows service registration example

Illustrative commands for the newer TM1 data-tier packaging; run from an elevated Command Prompt after replacing the paths. They register services, not a complete secured deployment. Follow the selected release manual for service identities and startup.

| cd /d "C:\IBM\tm1_64\bin64"<br>tm1admsd.exe -install<br>tm1sd.exe -install -n "Finance" -z "D:\PA\Models\Finance" |
| --- |

IBM documents these registration switches and the new config.tm1admsrv.json configuration file. The transition from the older installer can require an uninstall rather than an in-place overwrite; preserve databases and custom configuration first.  [R24]

| PRODUCTION GATE / Do not enable integration schedules until the restored model, security, TLS, backup and rollback have been tested. A successfully installed binary is not yet an accepted planning service. |
| --- |

---
Source: user-supplied comprehensive guide, section 9. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
