# 25. Forecasting and AI governance

Separate statistical prediction, explanation and authorized action.

IBM describes baseline forecasting, on-demand forecasting, spreading and saved statistical details. The Extended Forecasting Engine announcement identifies additional methods including Holt-Winters, MSTL, Auto ARIMA, BATS and XGBoost. Select the engine and method according to the release and forecast use case, not the appeal of an algorithm name.  [R86] [R71]

| Stage | Recommended control | Evidence |
| --- | --- | --- |
| Prepare | Define time grain, missing data, exclusions, history window and the business target. | A documented training / evaluation dataset. |
| Forecast | Compare an approved baseline with eligible methods using held-out periods. | Recorded error and bias measures appropriate to the business. |
| Review | Inspect anomalies, changing drivers, confidence and unusual events. | Named reviewer and rationale for overrides. |
| Publish | Keep forecast output separate from approved targets until accepted. | Versioned scenario and an accountable approval. |
| Monitor | Track degradation and changes in business assumptions. | A retraining / review trigger and rollback plan. |

## Planning Analytics Agent and extensions

IBM positions the Agent as model-aware assistance and describes watsonx Orchestrate integration and MCP extensibility. Generated explanations, suggested actions and model writes require different controls. A fluent explanation is not proof that a forecast is valid or that an action should be executed.  [R84]

## Recommended AI deployment policy

Approve the provider, region, data flows and retention terms. Limit identities to the model slices required. Require confirmation for material write-back or external actions, maintain auditability, and test whether unauthorized questions or actions are blocked. Use representative financial and operational examples to validate output, not only generic prompts.

IBM's September update distinguishes Workspace capabilities from Excel items still described as forthcoming. Do not convert a product roadmap statement into an implemented customer feature.  [R72]

| DECISION BOUNDARY / The business owner remains responsible for planning assumptions and approvals. AI should support the control process rather than bypass it. |
| --- |

---
Source: user-supplied comprehensive guide, section 25. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
