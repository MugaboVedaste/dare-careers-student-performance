# Data Model

## 1. Overview

The Dare Careers Student Progress and Performance Dashboard uses a dimensional data model.

The model separates descriptive information into dimension tables and measurable business events into fact tables.

This structure supports filtering, aggregation, and analysis across learners, dates, weeks, and learning tracks.

## 2. Dimension Tables

The model contains three main dimension tables:

1. `DimLearner`
2. `DimDate`
3. `DimWeek`

### DimLearner

Contains learner-track information, including:

- Learner email
- Learning track
- LearnerTrackKey
- Cohort
- Certification Type
- Graduation Status
- Certification Status
- Dropout Status
- Program Status

### DimDate

Provides calendar information for date-based analysis.

### DimWeek

Provides week-level information for lab and quiz analysis.

## 3. Fact Tables

The model contains four fact tables.

| Fact Table | Description |
|---|---|
| `Fact_Zoom_Attendance` | Learner attendance records |
| `FactParticipation` | Learner participation records |
| `FactLabs` | Learner lab assessment records |
| `FactQuizzes` | Learner quiz assessment records |

## 4. Relationships

The model uses one-to-many relationships with single-direction filtering from dimensions to fact tables.

### Learner Relationships

| One Side | Many Side | Relationship Key |
|---|---|---|
| `DimLearner[LearnerTrackKey]` | `Fact_Zoom_Attendance[LearnerTrackKey]` | LearnerTrackKey |
| `DimLearner[LearnerTrackKey]` | `FactParticipation[LearnerTrackKey]` | LearnerTrackKey |
| `DimLearner[LearnerTrackKey]` | `FactLabs[LearnerTrackKey]` | LearnerTrackKey |
| `DimLearner[LearnerTrackKey]` | `FactQuizzes[LearnerTrackKey]` | LearnerTrackKey |

### Date Relationships

| One Side | Many Side | Relationship Key |
|---|---|---|
| `DimDate[Date]` | `Fact_Zoom_Attendance[Attendance Date]` | Date |
| `DimDate[Date]` | `FactParticipation[Date]` | Date |

### Week Relationships

| One Side | Many Side | Relationship Key |
|---|---|---|
| `DimWeek[Week]` | `FactLabs[Week]` | Week |
| `DimWeek[Week]` | `FactQuizzes[Week]` | Week |

## 5. Model Design Principles

### Learner Dimension

`DimLearner` uses `LearnerTrackKey` to distinguish learner enrollments across different tracks.

This is important because one learner may be associated with more than one learning track.

### Date Dimension

`DimDate` supports filtering and analyzing attendance and participation by calendar date.

### Week Dimension

`DimWeek` supports weekly filtering and analysis of lab and quiz performance.

### Fact Tables

Each fact table represents a specific business process:

- Attendance events.
- Participation records.
- Lab assessment results.
- Quiz assessment results.

## 6. Filtering Direction

The intended filtering direction is from dimension tables to fact tables.

- `DimLearner` filters all four fact tables.
- `DimDate` filters attendance and participation.
- `DimWeek` filters labs and quizzes.

There are no direct relationships between fact tables.

## 7. Model Validation

The following checks should be performed:

1. Confirm dimension keys are unique on the one side.
2. Confirm fact tables contain matching foreign keys.
3. Confirm relationships are active.
4. Confirm relationships use one-to-many cardinality.
5. Confirm cross-filter direction is single.
6. Test slicers against the relevant visuals.
7. Confirm learner-level measures respond correctly to learner filters.

## 8. Model Benefits

The dimensional model supports:

- Consistent learner-level analysis.
- Track-level performance comparisons.
- Date and week filtering.
- Reusable DAX measures.
- Easier maintenance and future expansion.