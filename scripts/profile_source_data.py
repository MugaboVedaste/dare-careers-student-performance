
from pathlib import Path
from collections import Counter
from datetime import datetime
import csv
from openpyxl import load_workbook

DATA_DIR = Path("data/raw/aws_cloud")


def inspect_attendance():
    print("\n========== ATTENDANCE ==========")

    files = sorted(DATA_DIR.glob("Zoom Attendance/Week */*.csv"))

    print("Total CSV files:", len(files))

    all_emails = set()
    headers = Counter()
    total_records = 0
    invalid_durations = 0

    for file in files:
        with file.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            headers[tuple(reader.fieldnames or [])] += 1

            for row in reader:
                total_records += 1
                email = (row.get("Email") or "").strip().lower()

                if email:
                    all_emails.add(email)

                try:
                    duration = datetime.strptime(
                        row["Duration"].strip(), "%H:%M:%S"
                    )
                except (ValueError, KeyError, AttributeError):
                    invalid_durations += 1

    print("CSV headers:", headers)
    print("Total attendance records:", total_records)
    print("Unique learner emails:", len(all_emails))
    print("Invalid durations:", invalid_durations)

    return all_emails


def inspect_excel():
    print("\n========== EXCEL WORKBOOKS ==========")

    for file in DATA_DIR.rglob("*.xlsx"):
        print(f"\nFILE: {file.name}")

        wb = load_workbook(file, read_only=True, data_only=True)

        for ws in wb.worksheets:
            rows = list(ws.iter_rows(values_only=True))

            print(f"\nSheet: {ws.title}")
            print("Rows:", len(rows) - 1)
            print("Columns:", rows[0] if rows else [])

            if ws.title == "Labs" or ws.title == "Quizzes":
                scores = [
                    value
                    for row in rows[1:]
                    for value in row[1:]
                    if isinstance(value, (int, float))
                ]

                print("Score count:", len(scores))
                print("Minimum score:", min(scores, default=None))
                print("Maximum score:", max(scores, default=None))

            if ws.title == "Sheet1" and "Participation" in file.name:
                participant_counts = []

                for row in rows[1:]:
                    if len(row) > 1 and row[1]:
                        names = [
                            name.strip()
                            for name in str(row[1]).split(",")
                            if name.strip()
                        ]
                        participant_counts.append(len(names))

                print("Participation dates:", len(participant_counts))
                print("Total participation entries:",
                      sum(participant_counts))
                print("Average daily participants:",
                      round(sum(participant_counts) /
                            len(participant_counts), 2)
                      if participant_counts else 0)

            if "Status" in file.name:
                print("Graduation statuses:",
                      Counter(row[1] for row in rows[1:] if len(row) > 1))
                print("Certification statuses:",
                      Counter(row[2] for row in rows[1:] if len(row) > 2))

        wb.close()


if __name__ == "__main__":
    inspect_attendance()
    inspect_excel()
