
## AWS Cloud Data Quality Validation

Validation was performed on the original AWS Cloud source datasets.

### Attendance
- Total attendance CSV files: 50
- Total attendance records: 5,000
- Unique learner emails: 100
- Attendance records per day: 100
- Duplicate learner records per day: 0
- Sessions lasting 30 minutes or less: 0
- All records had the Participant role.

### Participation
- Total participation dates: 50
- Total participation entries: 4,253
- Successfully matched entries: 4,253
- Unmatched learner names: 0
- Duplicate learner/date entries: 0
- Missing dates between attendance and participation: 0

### Validation Conclusion

The AWS Cloud attendance and participation datasets passed the implemented quality checks.

All participation names were successfully matched to learner records, and both datasets cover the same 50 training dates.

Attendance qualification will use the business rule:
A learner is considered present when their session duration is strictly greater than 30 minutes.

### Outstanding Business Rules
- Confirm the expected number of training sessions for attendance-rate calculations.
- Confirm whether a zero lab score means incomplete or submitted with a score of zero.
- Confirm whether Non Graduate means dropout or includes learners still in progress.
