
from pathlib import Path
from collections import Counter
import argparse
import csv

from openpyxl import load_workbook


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


def profile_attendance(data_dir):
    print("\n========== ATTENDANCE PROFILE ==========")

    files = sorted(data_dir.glob("Zoom Attendance/Week */*.csv"))

    print("Total CSV files:", len(files))

    total_records = 0
    unique_emails = set()
    headers = Counter()
    daily_counts = Counter()

    for file in files:
        with file.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            headers[tuple(reader.fieldnames or [])] += 1

            count = 0

            for row in reader:
                total_records += 1
                count += 1

                email = (row.get("Email") or "").strip().lower()

                if email:
                    unique_emails.add(email)

            daily_counts[count] += 1

    print("CSV headers:", headers)
    print("Total attendance records:", total_records)
    print("Unique learner emails:", len(unique_emails))
    print("Records per file:", daily_counts)


def profile_workbooks(data_dir):
    print("\n========== EXCEL WORKBOOK PROFILE ==========")

    files = sorted(data_dir.rglob("*.xlsx"))

    if not files:
        print("No Excel workbooks found.")

    for file in files:
        print(f"\nFILE: {file.relative_to(data_dir)}")

        workbook = load_workbook(
            file, read_only=True, data_only=True
        )

        for sheet in workbook.worksheets:
            print(f"\nSHEET: {sheet.title}")

            rows = sheet.iter_rows(values_only=True)
            header = next(rows, None)

            print("Columns:", header)

            row_count = sum(1 for _ in rows)

            print("Data rows:", row_count)

        workbook.close()


def main():
    parser = argparse.ArgumentParser(
        description="Profile source data for either training track."
    )

    parser.add_argument(
        "track",
        choices=["aws_cloud", "power_bi"],
        help="Training track to profile."
    )

    args = parser.parse_args()
    data_dir = RAW_DATA_DIR / args.track

    if not data_dir.exists():
        parser.error(f"Data directory does not exist: {data_dir}")

    print(f"\nPROFILING TRACK: {args.track.upper()}")

    profile_attendance(data_dir)
    profile_workbooks(data_dir)


if __name__ == "__main__":
    main()
