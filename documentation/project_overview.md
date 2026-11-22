# Dare Careers – Student Progress and Performance Dashboard

## 1. Project Overview

The Dare Careers Student Progress and Performance Dashboard is a Business Intelligence project developed using Microsoft Power BI. The project focuses on analyzing learner performance, attendance, participation, assessments, certifications, and graduation outcomes.

The dashboard transforms raw training data into meaningful insights that help program managers and trainers monitor learner progress, evaluate program performance, and make data-driven decisions.

The project covers two learning tracks:
- AWS Cloud
- Power BI

The dataset represents one completed training cohort.

## 2. Project Objectives

The main objectives of this project are to:

- Monitor overall learner progress and performance.
- Analyze graduation, certification, and dropout rates.
- Evaluate learner attendance and participation.
- Track completed labs and assessment performance.
- Compare performance across learning tracks.
- Provide detailed insights into individual learner performance.
- Support data-driven decision-making through interactive dashboards.

## 3. Project Scope

The project focuses on the following areas:

### 3.1 Overall Performance Metrics

This section provides a high-level overview of the training program through:

- Total number of learners.
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

This section provides a more detailed view of individual learner performance, including:

- Learner identification and learning track.
- Attendance rate.
- Participation rate.
- Assessment scores.
- Number of completed labs.
- Average labs completed.
- Total class attendance hours.
- Program and learner status analysis.

## 4. Data Sources

The project uses training-related datasets covering the following areas:

| Data Area | Description |
|---|---|
| Zoom Attendance | Learner attendance records and session durations |
| Participation | Learner participation and engagement records |
| Labs | Learner lab completion and scores |
| Quizzes | Learner quiz assessment scores |
| Learner Status | Graduation and certification information |

The datasets include records for the AWS Cloud and Power BI learning tracks.

## 5. Tools and Technologies

The following tools and technologies are used:

- **Microsoft Power BI Desktop:** Data modeling, DAX calculations, and dashboard development.
- **Power Query:** Data extraction, cleaning, transformation, and preparation.
- **DAX (Data Analysis Expressions):** Creation of calculated columns and measures.
- **Git and GitHub:** Source control and project version management.
- **Markdown:** Technical documentation.

## 6. Data Preparation and Modeling

The data preparation process involves:

1. Importing the available datasets.
2. Cleaning and transforming the source data using Power Query.
3. Standardizing learner information across datasets.
4. Preparing fact and dimension tables.
5. Creating relationships between the tables.
6. Developing DAX measures for dashboard calculations.

The data model uses a dimensional modeling approach, with learner, date, and week dimensions connected to the relevant fact tables. Labs and quizzes connect to `DimDate` through a week-end date, so the Week and Month slicers affect every fact table. See [data_model.md](data_model.md).

### Main Fact Tables

- `Fact_Zoom_Attendance`
- `FactParticipation`
- `FactLabs`
- `FactQuizzes`

### Main Dimension Tables

- `DimLearner`
- `DimDate`
- `DimWeek`

## 7. Dashboard Structure

The dashboard consists of two main pages:

### Page 1: Overall Performance Metrics

Provides an overview of the overall training program performance, including KPI cards, performance charts, and interactive slicers.

### Page 2: Detailed Learner Insights

Provides learner-level performance information through summary cards, a detailed learner table, and interactive slicers.

## 8. Key Performance Indicators

The project uses the following key performance indicators:

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

The completed dashboard is intended to:

- Provide a clear overview of learner and program performance.
- Identify attendance and participation patterns.
- Highlight learner achievements and areas requiring attention.
- Enable comparisons between AWS Cloud and Power BI tracks.
- Help trainers and program managers monitor learner progress.
- Improve reporting through interactive and centralized visualizations.

## 10. Project Repository Structure

The project documentation and Power BI files are organized as follows:

```text
dare-careers-student-performance/
│
├── data/
│   └── raw/                      # source files, never edited (aws_cloud/, power_bi/)
│
├── documentation/
│   ├── dashboard_guide.md
│   ├── data_cleaning.md
│   ├── data_dictionary.md
│   ├── data_model.md
│   ├── dax_measures.md
│   └── project_overview.md
│
├── power_bi/
│   ├── dare_careers_dashboard.pbix
│   ├── power_query/              # Power Query (M) definitions of every query
│   └── screenshots/              # one image per dashboard page
│
├── scripts/                      # data profiling and quality-check scripts
└── README.md
```

---

**Project:** Dare Careers – Student Progress and Performance Dashboard  
**Platform:** Microsoft Power BI  
**Focus:** Learner Performance and Training Program Analytics