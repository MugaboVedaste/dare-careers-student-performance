# Dare Careers – Student Progress and Performance Dashboard

## 1. Project Overview

The Dare Careers Student Progress and Performance Dashboard is a Business Intelligence project developed using Microsoft Power BI.

The project focuses on analyzing learner attendance, participation, assessments, certifications, graduation outcomes, and overall training performance.

The dashboard transforms raw training data into meaningful insights that help trainers and program managers monitor learner progress, evaluate program performance, and make data-driven decisions.

The project covers two learning tracks:
- AWS Cloud
- Power BI

The available dataset represents one completed cohort.

## 2. Project Objectives

The main objectives are to:

- Monitor learner progress and performance.
- Analyze graduation, certification, and dropout rates.
- Evaluate learner attendance and participation.
- Track completed labs and assessment performance.
- Compare performance across learning tracks.
- Provide detailed insights into individual learner performance.
- Support data-driven decision-making.

## 3. Project Scope

### 3.1 Overall Performance Metrics

The first dashboard page provides an overview of:

- Total learner enrollments.
- Total graduations.
- Total certifications.
- Total dropouts.
- Graduation rate.
- Certification rate.
- Dropout rate.
- Average attendance rate.
- Average participation rate.
- Average assessment scores.

### 3.2 Detailed Learner Insights

The second dashboard page focuses on:

- Individual learner information.
- Learning tracks.
- Attendance rates.
- Participation rates.
- Assessment scores.
- Total labs completed.
- Average labs completed.
- Total class attendance hours.
- Learner and program status.

## 4. Data Sources

The project uses training-related datasets covering:

| Data Area | Description |
|---|---|
| Zoom Attendance | Learner attendance records and session durations |
| Participation | Learner participation records |
| Labs | Learner lab assessment records and scores |
| Quizzes | Learner quiz assessment records and scores |
| Learner Status | Graduation and certification information |

The datasets include AWS Cloud and Power BI learning tracks.

## 5. Tools and Technologies

- **Microsoft Power BI Desktop:** Data modeling, DAX calculations, and dashboard development.
- **Power Query:** Data extraction, cleaning, transformation, and preparation.
- **DAX:** Creation of calculated columns and measures.
- **Git and GitHub:** Source control and project version management.
- **Markdown:** Technical documentation.

## 6. Data Model

The project uses a dimensional modeling approach.

### Fact Tables
- `Fact_Zoom_Attendance`
- `FactParticipation`
- `FactLabs`
- `FactQuizzes`

### Dimension Tables
- `DimLearner`
- `DimDate`
- `DimWeek`

Learner status attributes are merged into `DimLearner`.

See [data_model.md](data_model.md) for the detailed model structure.

## 7. Dashboard Structure

The dashboard consists of two main pages.

### Page 1: Overall Performance Metrics

Provides a high-level overview of training program performance through KPI cards, bar charts, and interactive slicers.

### Page 2: Detailed Learner Insights

Provides detailed learner-level performance information through summary cards, a learner table, and interactive slicers.

## 8. Key Performance Indicators

| KPI | Description |
|---|---|
| Graduation Rate | Percentage of learner-track enrollments that graduated |
| Certification Rate | Percentage of learner-track enrollments that achieved certification |
| Dropout Rate | Percentage of learner-track enrollments classified as dropouts |
| Average Attendance Rate | Average attendance percentage across learners |
| Average Participation Rate | Average participation rate across learners |
| Average Assessment Score | Average score across lab and quiz assessments |
| Average Labs Completed | Average number of completed labs per learner |
| Total Class Hours | Total qualifying class attendance hours |

## 9. Expected Outcomes

The dashboard is intended to:

- Provide a clear overview of learner and program performance.
- Identify attendance and participation patterns.
- Highlight learner achievements and areas requiring attention.
- Enable comparisons between AWS Cloud and Power BI.
- Help trainers and program managers monitor learner progress.
- Improve reporting through interactive visualizations.

## 10. Documentation Structure

The documentation folder contains:

- `project_overview.md` – Project purpose, objectives, scope, and technologies.
- `dashboard_guide.md` – Dashboard pages, visuals, and slicers.
- `data_cleaning.md` – Data preparation and validation.
- `data_dictionary.md` – Descriptions of tables and fields.
- `data_model.md` – Data model and relationships.
- `dax_measures.md` – DAX measures and calculated columns.