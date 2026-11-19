## AWS Cloud Data Quality Validation

Validation was performed on the corrected AWS Cloud source datasets.

### Attendance

- Total attendance CSV files: 50
- Total attendance records: 2,000
- Unique learner emails: 40
- Attendance records per day: 40
- Duplicate learner records per day: 0
- Sessions lasting 30 minutes or less: 415
- Sessions lasting more than 30 minutes: 1,585
- All attendance records were checked against the attendance qualification rule.

### Participation

- Total participation dates: 50
- Total participation entries: 1,784
- Successfully matched entries: 1,784
- Unmatched learner names: 0
- Ambiguous learner names: 0
- Duplicate learner/date entries: 0
- Missing dates between attendance and participation: 0

### Assessments

- Total learners assessed: 40
- Valid lab scores: 400
- Valid quiz scores: 400
- Missing or invalid scores: 0
- Duplicate assessment email records: 0

### Learner Status

- Total learner status records: 40
- Graduates: 33
- Non-graduates: 7
- Certified learners: 24
- Learners not certified: 16
- Missing or duplicate learner email records: 0

### Validation Conclusion

The corrected AWS Cloud datasets passed the implemented data quality checks.

All 1,784 participation entries were successfully matched to learner records. Attendance and participation datasets cover the same 50 training dates.

The assessment datasets contain valid lab and quiz scores for all 40 learners, with no missing or invalid scores.

The learner status dataset contains 40 records with no missing or duplicate email addresses.

Attendance qualification follows this business rule:

A learner is considered present only when their session duration is strictly greater than 30 minutes. Sessions lasting exactly 30 minutes or less are excluded from attendance counts.

### Outstanding Business Rules

- Confirm the expected number of training sessions for attendance-rate calculations.
- Confirm whether a zero lab or quiz score means incomplete or submitted with a score of zero.
- Confirm whether Non Graduate means dropout or includes learners still in progress.