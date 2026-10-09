# Planning Analytics local utilities

Run from the appliance root. Python 3.9+ standard library; no pip install. All operations are local except the expressly enabled HTTPS GET metadata probe. JSON printed by these tools is a bounded diagnostic summary, not a raw documentation/model record dump.

```bash
TOOLS=.bob/planning-analytics-tools/pa-tool.py
python3 "$TOOLS" self-check
python3 "$TOOLS" profile-check .bob/planning-analytics-profiles/deployment-profile.example.json
python3 "$TOOLS" tm1-config-check .bob/planning-analytics-templates/tm1s.cfg.example
python3 "$TOOLS" reconcile \
 .bob/planning-analytics-templates/reconciliation-source.csv \
 .bob/planning-analytics-templates/reconciliation-target.csv \
 --keys Entity,Period --value Amount --tolerance 0.01
python3 "$TOOLS" forecast-evaluate .bob/planning-analytics-templates/forecast-evaluation.csv
python3 "$TOOLS" scaffold finance-pilot --offering saas
python3 "$TOOLS" scaffold cloud-design --offering dedicated-cloud --design-only
```

Exit codes: 0 passed/completed; 1 invalid profile, mismatch or failed self-check; 2 rejected input/IO/transport error; 3 review still required. Example profiles deliberately return 3. That is not a bug or a statement of unsupported software. `profile-check` is not SPCR verification. `tm1-config-check` only inspects a Local-style fragment; no listener or server is contacted. Reconciliation requires unique business keys unless `--aggregate` is explicitly given; duplicate records are never silently removed. Default absolute tolerance is per matched key. Missing keys remain mismatches.

Forecast evaluation scores provided period/actual/predicted pairs; it does not train a forecasting model or prove held-out evaluation. Metrics: MAE, RMSE, mean signed error predicted-minus-actual, WAPE with sum of absolute actuals, and MAPE over nonzero actuals only. WAPE is null when its denominator is zero; excluded-zero count is explicit. Synthetic fixtures are not real model results.

Scaffold writes only a new named directory in this appliance's design/store area. It produces a specification, source/load and TI contracts, profile, acceptance and cutover documents; these are not importable TM1 objects or deployed applications. Bob can generate implementation artifacts on a subsequent explicit request after version/schema/authorization validation.

## Optional read-only REST probe

Resolve the exact TM1 service root and authentication contract for the selected offering first. A SaaS API key must not be guessed into a Local Basic example. The tool does not invent gateway paths or header encodings. Supply a dedicated `PA_...` variable containing the COMPLETE approved Authorization value through your secret manager. The variable name may be passed on the command line; its secret value must not be.

```bash
# PA_TM1_AUTHORIZATION must already be set securely to the correct complete header.
# Replace the placeholder with an explicitly approved nonproduction service root.
python3 .bob/planning-analytics-tools/pa-tool.py rest-probe \
  --offering saas \
  --service-root 'https://your-approved-host/your-verified-path/api/v1' \
  --authorization-env PA_TM1_AUTHORIZATION \
  --connect
```

This example is not a known SaaS endpoint. The explicit `--connect` switch authorizes a single GET to `$metadata`; no network request occurs without it. TLS verification is mandatory; use `--ca-file` for an approved trust bundle, never `-k`. Redirects are rejected so authorization is not forwarded to another endpoint. Only a capped XML metadata response is parsed; raw contents are neither printed nor cached. This probe does not change Bob task memory. Optional `--output bob-planning-analytics-store/<file>.json` records only its bounded outcome, not metadata.

For a Local endpoint where native Basic is explicitly enabled and approved, use `--offering local --local-basic-approved` with separately exported `PA_TM1_USER` and `PA_TM1_PASSWORD`; do not use this recipe for CAM or SaaS. Probe success does not prove cube permission, offering entitlement or service acceptance.

Local outputs are exclusive-create under the store, with mode 0600. Symlinks, path traversal, invalid/duplicate CSV structures and nonfinite numbers are rejected. These tools do not execute TI, change data/security, install products or invoke a shell. All live actions remain separate, explicitly scoped requests.

Numeric inputs are bounded to 38 coefficient digits, absolute value at most 1e30 and decimal exponents from -30 to 30; out-of-range values are rejected rather than silently rounded into a planning result. CLI aggregation and scoring use an 80-digit decimal context.
