# Data Preparation and Cleaning

This document describes how the raw Dare Careers files become the Power BI model, which quality checks were run, and what they found.

The raw files in `data/raw/` are never edited. All cleaning is done in Power Query (`power_bi/power_query/Dare_Careers_PowerQueries.pq`), so the pipeline can be re-run end to end whenever the source files change.

## 1. Pipeline

```text
data/raw/<track>/...  ──►  Power Query  ──►  Fact_* / Dim* tables  ──►  DAX measures  ──►  dashboard
```

## 2. Transformations

### 2.1 Zoom attendance (`Fact_Zoom_Attendance`)

| Step | Why |
|---|---|
| Read all `Week N/*.csv` files of a track with `Folder.Files` and the shared `Transform File` function | 50 daily files per track → one table |
| Take the class date from the file name (`05-Aug-2024.csv`) with an `en-US` culture | The CSV has no date column |
| **AWS Cloud:** convert `Duration` from minutes to a duration | AWS exports minutes (`66`) |
| **Power BI:** read `Duration` as `h:mm:ss` | Power BI exports `1:46:00` |
| `Attendance Flag` = 1 when `Duration` > 30 minutes, else 0 | Business rule: attended only if **more than** 30 minutes |
| `Training Week` = `Week ` + whole weeks since 5 Aug 2024 + 1 | Week label used by `DimDate` |
| Add `Track`, then combine both tracks | One fact table for both tracks |
| `LearnerTrackKey` = lower-cased, trimmed e-mail + `\|` + track | Unique key per learner enrollment |

### 2.2 Participation (`FactParticipation`)

The source lists participants by **name**, one comma-separated cell per day.

| Step | Why |
|---|---|
| Split the `Participants` cell into one row per name and trim spaces | One row per learner per day |
| Build `LearnerNameMapping` (Name, Email, Track) from the attendance records | Participation files carry no e-mail |
| Join participation to the mapping on `Name` and add `LearnerTrackKey` | Links to `DimLearner`. The quality checks found no name shared between two learners, so each name maps to exactly one e-mail. |

### 2.3 Labs and quizzes (`FactLabs`, `FactQuizzes`)

| Step | Why |
|---|---|
| Read the `Labs` / `Quizzes` sheet, set `Int64` on the week columns, **unpivot** `Week 1`…`Week 10` into `Week` / `Score` | Wide sheet → tidy fact table |
| Add `Track` and `LearnerTrackKey`; combine both tracks | Same key as every other table |
| Add `Week End Date` = Friday of the week | Connects labs and quizzes to `DimDate`, so the Week and Month slicers filter them |

### 2.4 Learner status and `DimLearner`

| Step | Why |
|---|---|
| Read graduation / certification status for each track and combine | One status table |
| De-duplicate on `LearnerTrackKey` and merge the status columns back | One row per learner-track |
| Add `Cohort` (`Cohort 1`) and `Certification Type` (from track) | Slicer attributes |

### 2.5 `DimDate` and `DimWeek`

`DimDate` has one row per class day (taken from the attendance dates) with year, month number and name, day, training week and week number. `DimWeek` has one row per training week with its start date and month. Both are described in [data_dictionary.md](data_dictionary.md).

## 3. Quality checks

| Script | What it checks |
|---|---|
| `scripts/profile_source_data.py` | Structure and row counts of the AWS Cloud source files |
| `scripts/profile_power_bi_data.py` | Structure and row counts of the Power BI source files |
| `scripts/check_data_quality.py <track>` | Attendance: file/date counts, duplicate learner-days, roles, sessions ≤ 30 min. Participation: names matched to e-mails, ambiguous or duplicate names, date coverage |
| `scripts/check_assessment_quality.py <track>` | Labs/quizzes: missing, invalid and duplicate scores, score range. Status: duplicates, missing e-mails, value counts |

Run them from the project root (they need `openpyxl`):

```bash
python scripts/check_data_quality.py aws_cloud
python scripts/check_data_quality.py power_bi
python scripts/check_assessment_quality.py aws_cloud
python scripts/check_assessment_quality.py power_bi
```

## 4. Findings

| Area | Result |
|---|---|
| Attendance | 50 daily files per track; 2,000 (AWS Cloud) + 5,000 (Power BI) rows; exactly one row per learner per day; no blank e-mails; all roles `Participant` |
| Learners | 40 AWS Cloud + 100 Power BI = 140; no e-mail appears in both tracks; the attendance and status e-mail lists are identical |
| Participation | 1,784 + 4,253 entries, **all** matched to a learner; no ambiguous names, no duplicates, dates match the attendance dates |
| Labs / quizzes | No missing or invalid scores; range 0–100; 17 lab and 13 quiz scores are 0 |
| Status | No duplicates or missing e-mails; every non-graduate is also not certified |
| Short sessions | 415 AWS Cloud sessions ≤ 30 minutes (19 are exactly 30 and count as *not attended*); none in Power BI |

## 5. Assumptions and open questions

1. **Zero scores** are kept as real scores in assessment averages; a lab is "completed" when its score is above 0.
2. **Dropout** has no field in the source data. The project defines it as *Non Graduate + Not Certified + no qualifying attendance on the final class day*. This yields 2 dropouts (both AWS Cloud) out of 21 non-graduates. **Confirm this definition with the programme owners** — a different rule (for example, "every non-graduate") would change the headline numbers.
3. **Power BI attendance** is 100% for all 100 learners on all 50 days. Verify with the data owner that this export is complete.
4. **One cohort.** The data holds a single cohort (`Cohort 1`); the Cohort slicer therefore has one value until more cohorts are loaded.
5. **Name matching.** Participation is matched to learners by name only. If a future cohort contains two learners with the same name, the join would duplicate rows; match on name **and** track at that point.
