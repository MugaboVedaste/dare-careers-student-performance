# DAX Measures and Calculated Columns

## 1. Introduction

This document describes the main DAX measures and calculated columns used in the Dare Careers Student Progress and Performance Dashboard.

The calculations support learner enrollment analysis, graduation, certification, dropout classification, attendance, participation, and assessment performance.

Measures are stored in the `DAX_Measures` table where applicable.

## 2. Learner and Enrollment Measures

### Total Learners

Counts distinct learner email addresses.

```dax
Total Learners =
DISTINCTCOUNT(DimLearner[email])
```

### Total Learner Enrollments

Counts learner-track records.

```dax
Total Learner Enrollments =
COUNTROWS(DimLearner)
```

Expected overall count: 140.

### AWS Cloud Learners

```dax
AWS Cloud Learners =
CALCULATE(
    [Total Learner Enrollments],
    DimLearner[Track] = "AWS Cloud"
)
```

Expected count: 40.

### Power BI Learners

```dax
Power BI Learners =
CALCULATE(
    [Total Learner Enrollments],
    DimLearner[Track] = "Power BI"
)
```

Expected count: 100.

## 3. Graduation Measures

### Total Graduations

```dax
Total Graduations =
CALCULATE(
    [Total Learner Enrollments],
    DimLearner[FactLearnerStatus.Graduation Status] = "Graduate"
)
```

Expected count: 119.

### Graduation Rate

```dax
Graduation Rate =
DIVIDE(
    [Total Graduations],
    [Total Learner Enrollments],
    0
)
```

Expected overall rate: 85.00%.

## 4. Certification Measures

### Total Certifications

```dax
Total Certifications =
CALCULATE(
    [Total Learner Enrollments],
    DimLearner[FactLearnerStatus.Certification Status] = "Certified"
)
```

Expected count: 92.

### Certification Rate

```dax
Certification Rate =
DIVIDE(
    [Total Certifications],
    [Total Learner Enrollments],
    0
)
```

Expected overall rate: 65.71%.

## 5. Dropout Calculations

### Last Qualifying Attendance Date

Calculated column in `DimLearner`.

```dax
Last Qualifying Attendance Date =
VAR CurrentLearner =
    DimLearner[LearnerTrackKey]
RETURN
    CALCULATE(
        MAX(Fact_Zoom_Attendance[Attendance Date]),
        FILTER(
            ALL(Fact_Zoom_Attendance),
            Fact_Zoom_Attendance[LearnerTrackKey] = CurrentLearner
                && Fact_Zoom_Attendance[Attendance Flag] = 1
        )
    )
```

### Dropout Status

Calculated column in `DimLearner`.

```dax
Dropout Status =
VAR IsNonGraduate =
    DimLearner[FactLearnerStatus.Graduation Status] = "Non Graduate"
VAR IsNotCertified =
    DimLearner[FactLearnerStatus.Certification Status] = "Not Certified"
VAR LastAttendance =
    DimLearner[Last Qualifying Attendance Date]
VAR HasIncompleteAttendance =
    ISBLANK(LastAttendance)
        || LastAttendance < DATE(2024, 10, 11)
RETURN
    IF(
        IsNonGraduate
            && IsNotCertified
            && HasIncompleteAttendance,
        "Dropout",
        "Not Dropout"
    )
```

A learner is classified as a dropout only when all three conditions are true:

1. Graduation Status is Non Graduate.
2. Certification Status is Not Certified.
3. Last qualifying attendance is before October 11, 2024, or blank.

### Total Dropouts

```dax
Total Dropouts =
COALESCE(
    CALCULATE(
        [Total Learner Enrollments],
        DimLearner[Dropout Status] = "Dropout"
    ),
    0
)
```

Expected count: 2.

### Dropout Rate

```dax
Dropout Rate =
DIVIDE(
    [Total Dropouts],
    [Total Learner Enrollments],
    0
)
```

Expected overall rate: 1.43%.

## 6. Attendance Measures

### Total Attendance Days

```dax
Total Attendance Days =
CALCULATE(
    DISTINCTCOUNT(Fact_Zoom_Attendance[Attendance Date]),
    Fact_Zoom_Attendance[Attendance Flag] = 1
)
```

### Total Qualifying Attendance Records

```dax
Total Qualifying Attendance Records =
CALCULATE(
    COUNTROWS(Fact_Zoom_Attendance),
    Fact_Zoom_Attendance[Attendance Flag] = 1
)
```

Expected overall count: 6,585.

### Scheduled Attendance Opportunities

```dax
Scheduled Attendance Opportunities =
[Total Learner Enrollments]
    * DISTINCTCOUNT(DimDate[Date])
```

Expected overall count: 7,000.

### Attendance Rate

```dax
Attendance Rate =
DIVIDE(
    [Total Qualifying Attendance Records],
    [Scheduled Attendance Opportunities],
    0
)
```

Expected overall rate: approximately 94.07%.

### Average Attendance Rate per Learner

Calculates each learner's qualifying attendance percentage and then averages the learner-level percentages.

```dax
Average Attendance Rate per Learner =
AVERAGEX(
    VALUES(DimLearner[LearnerTrackKey]),
    VAR AttendedSessions =
        CALCULATE(
            COUNTROWS(Fact_Zoom_Attendance),
            Fact_Zoom_Attendance[Attendance Flag] = 1
        )
    VAR ScheduledSessions =
        CALCULATE(
            COUNTROWS(Fact_Zoom_Attendance),
            REMOVEFILTERS(Fact_Zoom_Attendance[Attendance Flag])
        )
    RETURN
        DIVIDE(
            AttendedSessions,
            ScheduledSessions,
            0
        )
)
```

### Total Class Hours

```dax
Total Class Hours =
CALCULATE(
    SUM(Fact_Zoom_Attendance[Duration]) * 24,
    Fact_Zoom_Attendance[Attendance Flag] = 1
)
```

The multiplication by 24 converts duration values stored as fractions of a day into hours.

## 7. Participation Measures

### Total Participation Records

```dax
Total Participation Records =
COUNTROWS(FactParticipation)
```

### Average Participation Rate

```dax
Average Participation Rate =
DIVIDE(
    [Total Participation Records],
    [Scheduled Attendance Opportunities],
    0
)
```

### Average Participation Rate per Learner

```dax
Average Participation Rate per Learner =
AVERAGEX(
    VALUES(DimLearner[LearnerTrackKey]),
    DIVIDE(
        CALCULATE(
            COUNTROWS(FactParticipation)
        ),
        CALCULATE(
            COUNTROWS(Fact_Zoom_Attendance),
            REMOVEFILTERS(Fact_Zoom_Attendance[Attendance Flag])
        )
    )
)
```

This measure calculates participation relative to the number of recorded learner attendance opportunities. Confirm the final saved measure in the Power BI model before publishing.

## 8. Assessment Measures

### Average Assessment Score

Combines lab and quiz scores while preserving the current filter context, including learner context in the learner table.

```dax
Average Assessment Score =
VAR AllScores =
    UNION(
        SELECTCOLUMNS(
            CALCULATETABLE(FactLabs),
            "Score", FactLabs[Score]
        ),
        SELECTCOLUMNS(
            CALCULATETABLE(FactQuizzes),
            "Score", FactQuizzes[Score]
        )
    )
RETURN
    AVERAGEX(
        AllScores,
        [Score]
    )
```

### Average Labs Completed

Calculates completed labs per learner and averages the result.

```dax
Average Labs Completed =
AVERAGEX(
    VALUES(DimLearner[LearnerTrackKey]),
    CALCULATE(
        COUNTROWS(FactLabs),
        FactLabs[Score] > 0
    )
)
```

### Total Labs

Counts lab records with scores greater than zero.

```dax
Total Labs =
CALCULATE(
    COUNTROWS(FactLabs),
    FactLabs[Score] > 0
)
```

## 9. Program Status

Program Status describes the status of the cohort, not the individual learner's graduation outcome.

The current dataset contains one completed cohort.

Calculated column in `DimLearner`:

```dax
Program Status = "Completed"
```

Every learner-track record associated with this cohort therefore has the Program Status Completed.

## 10. Measure Formatting

| Measure Type | Recommended Format |
|---|---|
| Graduation Rate | Percentage, 2 decimal places |
| Certification Rate | Percentage, 2 decimal places |
| Dropout Rate | Percentage, 2 decimal places |
| Attendance Rate | Percentage, 2 decimal places |
| Participation Rate | Percentage, 2 decimal places |
| Assessment Scores | Decimal number, 2 decimal places |
| Average Labs Completed | Decimal number, 2 decimal places |
| Total Class Hours | Decimal number, 2 decimal places |
| Counts | Whole number |

## 11. Validation Results

The following overall values were recorded during project development:

| Metric | Expected Value |
|---|---:|
| Total Learner Enrollments | 140 |
| AWS Cloud Learners | 40 |
| Power BI Learners | 100 |
| Total Graduations | 119 |
| Total Certifications | 92 |
| Total Dropouts | 2 |
| Graduation Rate | 85.00% |
| Certification Rate | 65.71% |
| Dropout Rate | 1.43% |
| Qualifying Attendance Records | 6,585 |
| Scheduled Attendance Opportunities | 7,000 |
| Attendance Rate | 94.07% |

These values are validation references for the overall dataset without restrictive slicer selections.