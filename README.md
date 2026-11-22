# Dare Careers – Student Progress and Performance Dashboard

A Power BI dashboard that tracks learner attendance, participation, lab and quiz scores, graduation, certification and dropout for Dare Careers' two training tracks, **Power BI** and **AWS Cloud** (140 learners, 10 weeks, 50 class days).

| Page | Purpose |
|---|---|
| **Overall Performance Metrics** | Programme-level cards and six bar charts: graduation, certification and dropout rates, average attendance, participation and assessment score. Slicers: Cohort, Track, Certification Type, Learner Status. |
| **Detailed Learner Insights** | Learner table plus six summary cards (labs, class hours, attendance, participation, assessment). Slicers: Cohort, Track, Month, Week, Learner Status, Program Status. |

![Overall Performance Metrics](power_bi/screenshots/Overall%20Performance%20Metrics.png)

![Detailed Learner Insights](power_bi/screenshots/Detailed%20Learner%20Insights.png)

The data model is shown in [`power_bi/screenshots/Model.png`](power_bi/screenshots/Model.png).

## Key rule

A learner is **Attended** for a class only if they spent **more than 30 minutes** in the Zoom session. Every attendance figure on both pages uses this rule.

## Repository layout

```text
data/raw/                 Source files (Zoom CSVs, participation, labs & quizzes, status) per track
power_bi/                 dare_careers_dashboard.pbix, Power Query (M) code, screenshots
documentation/            Model, DAX, data dictionary, cleaning notes, dashboard guide
reports/dashboard_exports/ PDF export of the dashboard
scripts/                  Data profiling and quality-check scripts
```

## Getting started

1. Open `power_bi/dare_careers_dashboard.pbix` in Power BI Desktop.
2. The queries read the raw files from `D:\AmaliTech\dare-careers-student-performance\data\raw`. If the project is stored elsewhere, update the source paths in Power Query (Transform data → each query's *Source* step), then **Refresh**.

## Validating the dashboard

Data quality can be re-checked from the raw files (needs `openpyxl`):

```bash
python scripts/check_data_quality.py aws_cloud     # also: power_bi
python scripts/check_assessment_quality.py aws_cloud
```

Headline values with no slicers selected:

| Metric | Value |
|---|---|
| Learners / graduations / certifications / dropouts | 140 / 119 / 92 / 2 |
| Graduation / certification / dropout rate | 85.00% / 65.71% / 1.43% |
| Average attendance (AWS Cloud / Power BI) | 79.25% / 100.00% |
| Average assessment score | 50.81 |

The full table, with per-track and per-week checks, is in [documentation/dax_measures.md](documentation/dax_measures.md#10-validation-reference-values).

## Documentation

| File | Contents |
|---|---|
| [project_overview.md](documentation/project_overview.md) | Purpose, scope, KPIs |
| [dashboard_guide.md](documentation/dashboard_guide.md) | Pages, visuals, slicers, how to read the metrics |
| [data_model.md](documentation/data_model.md) | Tables, relationships, sort settings, validation steps |
| [data_dictionary.md](documentation/data_dictionary.md) | Every table and field and the source files |
| [dax_measures.md](documentation/dax_measures.md) | Business rules, every measure, validation values |
| [data_cleaning.md](documentation/data_cleaning.md) | Power Query steps, quality checks, findings, assumptions |

## Assumptions to confirm with programme owners

- **Dropout** has no field in the source data; it is defined as *Non Graduate + Not Certified + no qualifying attendance on the final class day* (2 learners). See [data_cleaning.md](documentation/data_cleaning.md#5-assumptions-and-open-questions).
- The Power BI attendance export shows 100% attendance for all learners on all days.
- The data holds a single cohort (`Cohort 1`).

## Tools

Power BI Desktop, Power Query (M), DAX, Python 3 with `openpyxl` (quality scripts), Git.
