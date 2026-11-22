# Dashboard Guide

## 1. Introduction

This guide explains the two pages of the Dare Careers Student Progress and Performance Dashboard and how to read them. Screenshots are in `power_bi/screenshots/`.

**Attendance rule used everywhere:** a learner counts as *Attended* for a class only if they spent **more than 30 minutes** in the Zoom session.

## 2. Page 1: Overall Performance Metrics

**Objective:** a high-level view of learner outcomes and programme performance for stakeholders.

### Summary cards

| Card | Meaning |
|---|---|
| Total Learners | Learner enrollments across all selected cohorts and tracks (a learner on two tracks would count twice; today none do) |
| Total Graduations | Learners with Graduation Status = Graduate |
| Total Certifications | Learners with Certification Status = Certified |
| Total Dropouts | Learners classified as Dropout (see §5) |

### Bar charts

Each chart compares the two tracks (AWS Cloud, Power BI), split by cohort:

1. Graduation Rate
2. Certification Rate
3. Dropout Rate
4. Average Attendance Rate — mean of each learner's share of class days attended
5. Average Participation Rate — mean of each learner's share of class days participated
6. Average Assessment Score — mean of weekly lab and quiz scores

### Slicers

Cohort · Track · Certification Type · Learner Status (Certified / Not Certified)

`Certification Type` mirrors the track (AWS / Power BI), because each track awards one certification.

## 3. Page 2: Detailed Learner Insights

**Objective:** learner-level progress and engagement for trainers and programme managers.

### Summary cards

| Card | Meaning |
|---|---|
| Total Labs | Labs completed (score above 0) by all selected learners |
| Average Labs Completed | Labs completed per learner |
| Total Class Hours | Hours in qualifying sessions (more than 30 minutes) for all selected learners |
| Average Attendance Rate | Mean learner attendance rate |
| Average Participation Rate | Mean learner participation rate |
| Average Assessment Score | Mean of lab and quiz scores |

### Learner table

| Column | Description |
|---|---|
| Learner | Learner e-mail |
| Track | AWS Cloud / Power BI |
| Cohort | Cohort name |
| Participation | Learner's participation rate |
| Attendance | Learner's attendance rate |
| Assessment Scores | Learner's average lab and quiz score |

Every row shows that learner's own values; the Total row shows the average for the selected learners.

### Slicers

Cohort · Track · **Month** · **Week** · Learner Status · Program Status

- Month and Week both filter **every** card and the table (attendance, participation, class hours, labs and assessments).
- A week belongs to the month of its Friday, so Week 9 (30 Sep – 4 Oct) is in October.
- Selecting a Month and a Week that do not belong together (for example August and Week 10) returns no data. Clear one of them.
- Program Status describes the cohort as a whole, not an individual learner.

## 4. Using slicers

1. Select a value in a slicer; every visual on the page updates.
2. Use Ctrl+click for several values; click the selected value again (or the eraser icon) to clear it.
3. Slicers combine: Track = AWS Cloud with Learner Status = Not Certified shows non-certified AWS Cloud learners.
4. Slicer selections are saved with the report, so set every slicer to **All** before saving or publishing.

## 5. Understanding the metrics

| Metric | How it is calculated |
|---|---|
| Graduation / certification / dropout rate | Learners in the group ÷ all learners in the current selection |
| Dropout | Non Graduate **and** Not Certified **and** last qualifying attendance before the final class day (or none). This is a project definition — the source data has no dropout field. |
| Attendance rate | Class days attended (> 30 minutes) ÷ scheduled class days in the selected period, averaged over learners |
| Participation rate | Class days participated ÷ scheduled class days in the selected period, averaged over learners |
| Assessment score | Average of every weekly lab and quiz score; a score of 0 counts as 0 |
| Labs completed | Weekly labs with a score above 0 |

Reference values for checking the dashboard are in [dax_measures.md](dax_measures.md#10-validation-reference-values).

## 6. Notes

- The data covers one completed cohort, so the Cohort slicer has one value and Program Status is `Completed`.
- Power BI-track learners show 100% attendance in the source data.
