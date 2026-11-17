
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, date, time
import argparse
import csv
import re

from openpyxl import load_workbook


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


def normalize_name(name):
    return re.sub(r"\s+", " ", str(name).strip()).lower()


def parse_date(value):
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    return datetime.strptime(str(value).strip(), "%d-%b-%Y").date()


def check_attendance(data_dir):
    print("\n========== ATTENDANCE QUALITY ==========")

    name_to_email = defaultdict(set)
    attendance_dates = set()
    duplicate_records = 0
    short_sessions = 0
    total_records = 0
    role_counts = Counter()
    daily_counts = Counter()

    files = sorted(
        data_dir.glob("Zoom Attendance/Week */*.csv")
    )

    for file in files:
        session_date = datetime.strptime(
            file.stem, "%d-%b-%Y"
        ).date()

        attendance_dates.add(session_date)
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
                ).time()

                if duration <= time(0, 30):
                    short_sessions += 1

                role_counts[row["Role"]] += 1

        daily_counts[session_date] = len(daily_emails)

        duplicate_records += (
            len(daily_emails) - len(set(daily_emails))
        )

    print("Attendance CSV files:", len(files))
    print("Attendance dates:", len(attendance_dates))
    print("Total records:", total_records)
    print("Unique learner emails:",
          len({email for emails in name_to_email.values()
               for email in emails}))
    print("Duplicate learner records per day:", duplicate_records)
    print("Sessions of 30 minutes or less:", short_sessions)
    print("Role distribution:", role_counts)
    print("Daily attendance records:", Counter(daily_counts.values()))

    return name_to_email, attendance_dates


def check_participation(data_dir, name_to_email, attendance_dates):
    print("\n========== PARTICIPATION QUALITY ==========")

    file = data_dir / "Participation" / "Participation records.xlsx"

    if not file.exists():
        print("Participation workbook not found:", file)
        return

    workbook = load_workbook(file, read_only=True, data_only=True)

    ws = workbook.active

    unmatched = Counter()
    ambiguous = Counter()
    duplicate_participation = 0
    participation_dates = set()
    total_entries = 0
    matched_entries = 0
    daily_counts = Counter()
    seen = set()

    for date_value, participants in ws.iter_rows(
        min_row=2, values_only=True
    ):
        session_date = parse_date(date_value)
        participation_dates.add(session_date)

        names = [
            normalize_name(name)
            for name in str(participants or "").split(",")
            if name.strip()
        ]

        daily_counts[session_date] = len(names)

        for name in names:
            total_entries += 1
            emails = name_to_email.get(name, set())

            if len(emails) == 1:
                email = next(iter(emails))
                matched_entries += 1

                key = (session_date, email)

                if key in seen:
                    duplicate_participation += 1

                seen.add(key)

            elif len(emails) > 1:
                ambiguous[name] += 1

            else:
                unmatched[name] += 1

    print("Participation dates:", len(participation_dates))
    print("Total participation entries:", total_entries)
    print("Matched entries:", matched_entries)
    print("Unmatched entries:", sum(unmatched.values()))
    print("Unique unmatched names:", len(unmatched))
    print("Ambiguous names:", sum(ambiguous.values()))
    print("Duplicate learner/date entries:", duplicate_participation)

    print(
        "Participation dates missing attendance:",
        len(participation_dates - attendance_dates)
    )

    print(
        "Attendance dates missing participation:",
        len(attendance_dates - participation_dates)
    )

    print("\nTop unmatched names:")

    for name, count in unmatched.most_common(20):
        print(f"{name}: {count}")

    if ambiguous:
        print("\nAmbiguous learner names:")

        for name, count in ambiguous.most_common(20):
            print(f"{name}: {count}")

    workbook.close()


def main():
    parser = argparse.ArgumentParser(
        description="Validate learner attendance and participation data."
    )

    parser.add_argument(
        "track",
        choices=["aws_cloud", "power_bi"],
        help="Training track to validate."
    )

    args = parser.parse_args()

    data_dir = RAW_DATA_DIR / args.track

    if not data_dir.exists():
        parser.error(f"Data directory does not exist: {data_dir}")

    print(f"\nVALIDATING TRACK: {args.track.upper()}")

    names, dates = check_attendance(data_dir)
    check_participation(data_dir, names, dates)


if __name__ == "__main__":
    main()
