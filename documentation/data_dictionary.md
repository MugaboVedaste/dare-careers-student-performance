# Data Dictionary

Describes every table and field in the Power BI model. For how the tables connect, see [data_model.md](data_model.md); for the measures, see [dax_measures.md](dax_measures.md).

## 1. Source data

| Source | Location | Format | Notes |
|---|---|---|---|
| Zoom attendance | `data/raw/<track>/Zoom Attendance/Week N/DD-Mon-YYYY.csv` | CSV, one file per class day | 10 weeks × 5 days. **AWS Cloud** `Duration` is in minutes (`66`); **Power BI** `Duration` is `h:mm:ss` (`1:46:00`). Times are 24-hour in AWS (`18:09`) and 12-hour in Power BI (`06:02 PM`). |
| Participation | `data/raw/<track>/Participation/*.xlsx` | One row per day: `Date`, `Participants` | `Participants` is a comma-separated list of **names** (no e-mail). |
| Labs and quizzes | `data/raw/<track>/Labs & Quizes/*.xlsx` | Sheets `Labs` and `Quizzes`: `email`, `Week 1` … `Week 10` | Scores 0–100, one value per learner per week. |
| Learner status | `data/raw/<track>/Status of Learners/*.xlsx` | `email`, `Graduation Status`, `Certification Status` | One row per learner. |

Tracks: `aws_cloud` (40 learners) and `power_bi` (100 learners). Programme: 5 Aug – 11 Oct 2024, 50 class days.

## 2. Dimension tables

### 2.1 DimLearner — one row per learner per track

| Field | Type | Description |
|---|---|---|
| `email` | Text | Learner e-mail |
| `Track` | Text | `AWS Cloud` or `Power BI` |
| `LearnerTrackKey` | Text | `lower(trim(email)) \| Track` — primary key |
| `FactLearnerStatus.Graduation Status` | Text | `Graduate` / `Non Graduate` |
| `FactLearnerStatus.Certification Status` | Text | `Certified` / `Not Certified` (the **Learner Status** slicer) |
| `Cohort` | Text | Cohort name — fixed value `Cohort 1` (the data holds one cohort) |
| `Certification Type` | Text | `AWS` or `Power BI`, derived from the track |
| `Program Status` | Text | *Calculated column.* Cohort-level status; `Completed` for the single cohort in this project |
| `Last Qualifying Attendance Date` | Date | *Calculated column.* Latest class day with an attendance flag of 1 |
| `Dropout Status` | Text | *Calculated column.* `Dropout` / `Not Dropout` (rule in dax_measures.md §5) |

### 2.2 DimDate — one row per class day

| Field | Type | Description |
|---|---|---|
| `Date` | Date | Class day — primary key |
| `Week Number` | Whole number | 1–10, counted from the programme start (5 Aug 2024); sort column for `Training Week` |
| `Training Week` | Text | `Week 1` … `Week 10` (the **Week** slicer) |
| `Year` | Whole number | – |
| `Month Number` | Whole number | Sort column for `Month Name` |
| `Month Name` | Text | Calendar month of the date (the **Month** slicer) |
| `Day` | Whole number | Day of month |

### 2.3 DimWeek — one row per training week

A week lookup for labs and quizzes. The Week and Month slicers use `DimDate`, not `DimWeek`.

| Field | Type | Description |
|---|---|---|
| `Week` | Text | `Week 1` … `Week 10` — primary key |
| `Week Number` | Whole number | 1–10 |
| `Week Start` | Date | Monday of the week |
| `Month Number` | Whole number | Month of the week's Wednesday |
| `Month Name` | Text | Month of the week's Wednesday |

## 3. Fact tables

### 3.1 Fact_Zoom_Attendance — one row per learner per class day

| Field | Type | Description |
|---|---|---|
| `Source.Name` | Text | Source file name (the date) |
| `Name` | Text | Display name in Zoom |
| `Email` | Text | Learner e-mail |
| `Join Time`, `Leave Time` | Time | Session start / end |
| `Duration` | Duration | Time in the session |
| `Role` | Text | Zoom role (all `Participant`) |
| `Attendance Date` | Date | Class day — foreign key to `DimDate[Date]` |
| `Attendance Flag` | Whole number | `1` if `Duration` > 30 minutes, otherwise `0` |
| `Training Week` | Text | `Week N` |
| `Track` | Text | Learning track |
| `LearnerTrackKey` | Text | Foreign key to `DimLearner` |

### 3.2 FactParticipation — one row per learner per day participated

| Field | Type | Description |
|---|---|---|
| `Date` | Date | Class day — foreign key to `DimDate[Date]` |
| `Participants` | Text | Learner name as written in the source list |
| `Track` | Text | Learning track |
| `Email` | Text | E-mail found by matching `Participants` to the attendance names **within the same track** |
| `LearnerTrackKey` | Text | Foreign key to `DimLearner`; blank if the name could not be matched (should never happen — see the quality scripts) |

### 3.3 FactLabs — one row per learner per week

| Field | Type | Description |
|---|---|---|
| `email` | Text | Learner e-mail |
| `Week` | Text | `Week N` — foreign key to `DimWeek[Week]` |
| `Week End Date` | Date | Friday of that week — foreign key to `DimDate[Date]` |
| `Score` | Whole number | Lab score, 0–100 (0 = lab not completed) |
| `Track` | Text | Learning track |
| `LearnerTrackKey` | Text | Foreign key to `DimLearner` |

### 3.4 FactQuizzes — one row per learner per week

Same columns as `FactLabs` (including `Week End Date`); `Score` is the quiz score, 0–100.

## 4. Status definitions

| Field | Values |
|---|---|
| Graduation Status | `Graduate`, `Non Graduate` |
| Certification Status | `Certified`, `Not Certified` |
| Dropout Status | `Dropout`, `Not Dropout` |
| Program Status | `Completed` (single cohort) |

## 5. Known data characteristics

- Every learner has one attendance row for every class day, so *scheduled* and *recorded* sessions are equal (7,000).
- All 100 Power BI learners have a session of more than 30 minutes on every one of the 50 days (100% attendance). This is unusual — confirm with the data owner that the Power BI export is complete and not pre-filtered.
- 19 AWS Cloud sessions last exactly 30 minutes and correctly count as *not attended*.
- 17 weekly lab scores and 13 weekly quiz scores are 0.
- No participant name is shared between tracks or between two learners of one track, and every participation name matches an attendance name.
