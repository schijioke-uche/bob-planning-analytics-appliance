# 15. Model design: dimensions, cubes and drivers

Illustrative model design - adapt to approved business definitions.

TM1 models organize values across dimensions such as time, accounts, organizational units, products and scenarios. Cubes hold multidimensional intersections; calculations and write-back turn those intersections into a planning model. Business definitions, not the number of source columns, should drive the design.  [R81]

| Model element | Illustrative finance design | Design control |
| --- | --- | --- |
| Time | Month and year, with an approved fiscal calendar. | Define how partial periods, actuals and forecast horizons are handled. |
| Organization | Entity and cost center with reporting hierarchies. | Assign an owner to reorganizations and effective-date decisions. |
| Scenario | Actual, Budget and Forecast versions. | Lock approved actuals / baselines and document copy-forward policy. |
| Measures | Units, price, revenue, cost and margin. | Distinguish additive values from percentages and ratios. |
| Drivers | Headcount, compensation assumptions, capacity or price changes. | Keep input assumptions distinct from calculated results. |
| Attributes and aliases | Descriptions, classification and display names. | Preserve stable identifiers when labels change. |

## Recommended modeling workflow

1. Agree the grain of each cube and document what one cell means.

2. Define dimensions, hierarchies, element types and naming conventions before loading facts.

3. Build a small model with known totals; prove consolidations, calculations and access rules.

4. Separate transaction staging from planning assumptions and published results where that improves clarity.

5. Test reorganization, new members, missing data, zero values, currency assumptions and read-only history.

6. Record the owner and test cases for every material calculation and integration.

| ILLUSTRATIVE BUSINESS RULE / Revenue = Units x Price. Gross Margin = Revenue - Cost. Margin % must be recomputed from consolidated Revenue and Cost, not summed across products. These are example requirements, not a packaged IBM financial model. |
| --- |

---
Source: user-supplied comprehensive guide, section 15. Citation IDs R01-R90 resolve in ../reference-catalog.md and ../references.json. This is source-derived material, not a new IBM support certification.
