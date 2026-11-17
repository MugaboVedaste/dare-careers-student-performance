
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import csv
import re

from openpyxl import load_workbook

DATA_DIR = Path("data/raw/aws_cloud")


def normalize_name(name):
    return re.sub(r"\s+", " ", str(name).strip()).lower()


def check_attendance():
    print("\n========== ATTENDANCE QUALITY ==========")

    name_to_email = defaultdict(set)
    attendance_dates = set()
    duplicate_records = 0
    short_sessions = 0
    total_records = 0
    role_counts = Counter()
    daily_counts = Counter()

    for file in DATA_DIR.glob("Zoom Attendance/Week */*.csv"):
        date = datetime.strptime(file.stem, "%d-%b-%Y").date()
        attendance_dates.add(date)

        daily_emails = []

        with file.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                total_records += 1

                email = row["Email"].strip().lower()
                name = normalize_name(row["Name"])

                name_to_email[name].add(email)
                daily_emails.append(email)

                duration = datetime.strptime(
                    row["Duration"].strip(), "%H:%M:%S"
                )

                if duration.time() <= datetime.strptime(
                    "00:30:00", "%H:%M:%S"
                ).time():
                    short_sessions += 1

                role_counts[row["Role"]] += 1

        daily_counts[date] = len(daily_emails)

        duplicate_records += (
            len(daily_emails) - len(set(daily_emails))
        )

    print("Attendance dates:", len(attendance_dates))
    print("Total records:", total_records)
    print("Duplicate learner records per day:", duplicate_records)
    print("Sessions of 30 minutes or less:", short_sessions)
    print("Role distribution:", role_counts)
    print("Daily attendance records:", Counter(daily_counts.values()))

    return name_to_email, attendance_dates


def check_participation(name_to_email, attendance_dates):
    print("\n========== PARTICIPATION QUALITY ==========")

    file = DATA_DIR / "Participation" / "Participation records.xlsx"
    workbook = load_workbook(file, read_only=True, data_only=True)

    ws = workbook.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))

    unmatched = Counter()
    duplicate_participation = 0
    participation_dates = set()
    total_entries = 0
    matched_entries = 0
    daily_counts = Counter()
    seen = set()

    for date_value, participants in rows:
        date = datetime.strptime(
            str(date_value), "%d-%b-%Y"
        ).date()

        participation_dates.add(date)

        names = [
            normalize_name(name)
            for name in str(participants or "").split(",")
            if name.strip()
        ]

        daily_counts[date] = len(names)

        for name in names:
            total_entries += 1

            emails = name_to_email.get(name, set())

            if len(emails) == 1:
                email = next(iter(emails))
                matched_entries += 1

                key = (date, email)

                if key in seen:
                    duplicate_participation += 1
                seen.add(key)

            elif not emails:
                unmatched[name] += 1

    print("Participation dates:", len(participation_dates))
    print("Total participation entries:", total_entries)
    print("Matched entries:", matched_entries)
    print("Unmatched entries:", sum(unmatched.values()))
    print("Unique unmatched names:", len(unmatched))
    print("Duplicate learner/date entries:", duplicate_participation)
    print("Participation dates missing attendance:",
          len(participation_dates - attendance_dates))
    print("Attendance dates missing participation:",
          len(attendance_dates - participation_dates))

    print("\nTop unmatched names:")

    for name, count in unmatched.most_common(20):
        print(f"{name}: {count}")

    workbook.close()


if __name__ == "__main__":
    names, dates = check_attendance()
    check_participation(names, dates)
