# Data Model

## 1. Overview

The dashboard uses a star schema: dimension tables describe *who* and *when*, fact tables hold the measurable events. All relationships are one-to-many with single-direction filtering, from dimension to fact.

## 2. Tables

| Table | Type | Grain |
|---|---|---|
| `DimLearner` | Dimension | One row per learner **per track** (`LearnerTrackKey`) |
| `DimDate` | Dimension | One row per class day |
| `DimWeek` | Dimension | One row per training week (1–10) |
| `Fact_Zoom_Attendance` | Fact | One row per learner per class day (Zoom session) |
| `FactParticipation` | Fact | One row per learner per day participated |
| `FactLabs` | Fact | One row per learner per week (lab score) |
| `FactQuizzes` | Fact | One row per learner per week (quiz score) |
| `DAX_Measures` | Measure holder | – |

`FactLearnerStatus` is a staging query: its graduation and certification columns are merged into `DimLearner`.

Field-level detail is in [data_dictionary.md](data_dictionary.md).

## 3. Relationships

All relationships are active, one-to-many, single direction (dimension → fact).

| One side | Many side | Purpose |
|---|---|---|
| `DimLearner[LearnerTrackKey]` | `Fact_Zoom_Attendance[LearnerTrackKey]` | Learner → attendance |
| `DimLearner[LearnerTrackKey]` | `FactParticipation[LearnerTrackKey]` | Learner → participation |
| `DimLearner[LearnerTrackKey]` | `FactLabs[LearnerTrackKey]` | Learner → labs |
| `DimLearner[LearnerTrackKey]` | `FactQuizzes[LearnerTrackKey]` | Learner → quizzes |
| `DimDate[Date]` | `Fact_Zoom_Attendance[Attendance Date]` | Date → attendance |
| `DimDate[Date]` | `FactParticipation[Date]` | Date → participation |
| `DimDate[Date]` | `FactLabs[Week End Date]` | Week / month → labs |
| `DimDate[Date]` | `FactQuizzes[Week End Date]` | Week / month → quizzes |
| `DimWeek[Week]` | `FactLabs[Week]` | Week lookup for labs |
| `DimWeek[Week]` | `FactQuizzes[Week]` | Week lookup for quizzes |

There is **no relationship between `DimDate` and `DimWeek`**. Linking them created ambiguous filter paths, so labs and quizzes are connected to `DimDate` directly instead (see §5).

## 4. Slicer sources

| Slicer | Field |
|---|---|
| Cohort | `DimLearner[Cohort]` |
| Track | `DimLearner[Track]` |
| Certification Type | `DimLearner[Certification Type]` |
| Learner Status | `DimLearner[FactLearnerStatus.Certification Status]` |
| Program Status | `DimLearner[Program Status]` |
| Month | `DimDate[Month Name]` (sorted by `Month Number`) |
| Week | `DimDate[Training Week]` (sorted by `Week Number`) |

Month and Week come from `DimDate`, so they filter attendance, participation, labs and quizzes together.

## 5. Why labs and quizzes use `Week End Date`

Labs and quizzes are recorded per week, not per day. Each lab and quiz row therefore carries a `Week End Date` (the Friday of its week, for example Week 1 → 9 Aug 2024). Every week has a class on Friday, so every `Week End Date` exists in `DimDate`. Selecting a week or month in a `DimDate` slicer then also selects the matching labs and quizzes.

A week belongs to the month of its Friday: Week 9 (30 Sep – 4 Oct) counts as October.

## 6. Design notes

- **`LearnerTrackKey`** = lower-cased, trimmed e-mail + `|` + track. It keeps a learner enrolled on both tracks as two separate enrollments. (No learner currently appears in both tracks.)
- **`DimDate`** is built from the attendance records, so it holds class days only. `Scheduled Attendance Opportunities` relies on this: learners × distinct class days.
- **Participation** source files list participants by *name*. Power Query maps names to e-mails through the attendance records (join on name). No name is shared between learners, so each name maps to exactly one e-mail.

## 7. Validation

Check these after any model change:

1. In Model view every relationship above is a **solid line** (active), one-to-many, single direction. A dotted line is inactive and filters nothing.
2. With no slicers selected, the cards match the values in [dax_measures.md](dax_measures.md) section 11.
3. Select **Track = AWS Cloud**, then **Power BI**: attendance, participation and assessment bars must differ.
4. In the learner table, values must differ from learner to learner.
5. Select a **Week**, then a **Month**: attendance, participation, class hours, labs and assessments must all change.
6. `Month Name` sorts August → September → October and `Training Week` sorts Week 1 → Week 10.
