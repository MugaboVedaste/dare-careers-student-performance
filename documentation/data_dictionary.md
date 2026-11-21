# Data Dictionary

## 1. Introduction

This document describes the main tables and fields used in the Dare Careers Student Progress and Performance Dashboard.

The data model consists of fact tables and dimension tables.

## 2. Dimension Tables

### 2.1 DimLearner

Contains learner-track information and attributes used to analyze learner performance.

| Field | Description |
|---|---|
| `email` | Learner email identifier |
| `Track` | Learning track, such as AWS Cloud or Power BI |
| `LearnerTrackKey` | Unique identifier for a learner's enrollment in a specific track |
| `Cohort` | Cohort associated with the learner |
| `Certification Type` | Certification category associated with the learner |
| `FactLearnerStatus.Graduation Status` | Learner graduation outcome |
| `FactLearnerStatus.Certification Status` | Learner certification outcome |
| `Last Qualifying Attendance Date` | Latest date the learner met the attendance threshold |
| `Dropout Status` | Calculated dropout classification |
| `Program Status` | Cohort-level program status |

### 2.2 DimDate

Contains calendar information used for date-based analysis.

| Field | Description |
|---|---|
| `Date` | Calendar date used to connect attendance and participation records |

### 2.3 DimWeek

Contains week-level information used for weekly analysis.

| Field | Description |
|---|---|
| `Week` | Week identifier used to connect lab and quiz records |

## 3. Fact Tables

### 3.1 Fact_Zoom_Attendance

Contains learner attendance records.

| Field | Description |
|---|---|
| `LearnerTrackKey` | Learner-track relationship key |
| `Attendance Date` | Date of the attendance session |
| `Duration` | Recorded attendance duration |
| `Attendance Flag` | Indicates whether attendance meets the qualification threshold |
| `Track` | Learning track, where retained in the fact table |

**Attendance Flag values:**

- `1` – Attendance duration is greater than 30 minutes.
- `0` – Attendance duration is 30 minutes or less.

### 3.2 FactParticipation

Contains learner participation records.

| Field | Description |
|---|---|
| `LearnerTrackKey` | Learner-track relationship key |
| `Date` | Date associated with the participation record |

Additional source fields should be documented after verifying the final table structure.

### 3.3 FactLabs

Contains learner lab assessment records.

| Field | Description |
|---|---|
| `LearnerTrackKey` | Learner-track relationship key |
| `Week` | Week associated with the lab record |
| `Score` | Lab assessment score |

### 3.4 FactQuizzes

Contains learner quiz assessment records.

| Field | Description |
|---|---|
| `LearnerTrackKey` | Learner-track relationship key |
| `Week` | Week associated with the quiz record |
| `Score` | Quiz assessment score |

## 4. Keys and Identifiers

| Key | Purpose |
|---|---|
| `LearnerTrackKey` | Connects learner-track records in dimensions and fact tables |
| `DimDate[Date]` | Connects calendar dates to attendance and participation records |
| `DimWeek[Week]` | Connects week identifiers to lab and quiz records |

## 5. Status Definitions

| Status Field | Values or Meaning |
|---|---|
| Graduation Status | Graduate / Non Graduate |
| Certification Status | Certified / Not Certified |
| Dropout Status | Dropout / Not Dropout |
| Program Status | Completed for the single cohort in this project |

## 6. Important Business Definitions

### Attendance

Attendance is considered qualifying when the recorded session duration is greater than 30 minutes.

### Dropout

A learner is classified as a dropout when they are a non-graduate, are not certified, and have no qualifying attendance on or after October 11, 2024.

### Program Status

Program Status describes the status of the cohort, not the individual learner's graduation status.

The cohort represented in the current dataset is Completed.