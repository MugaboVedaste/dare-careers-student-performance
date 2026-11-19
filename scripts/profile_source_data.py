
import argparse
import csv
from collections import Counter
from pathlib import Path
from openpyxl import load_workbook

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


def inspect_attendance(data_dir):
    print("\n========== ATTENDANCE DETAILS ==========")

    attendance_files = sorted(
        data_dir.glob("Zoom Attendance/Week */*.csv")
    )

    all_emails = set()
    total_records = 0
    duration_counts = Counter()
    role_counts = Counter()

    for file in attendance_files:
        with open(file, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                total_records += 1

                email = row.get("Email", "").strip().lower()
                if email:
                    all_emails.add(email)

                duration_counts[row.get("Duration", "").strip()] += 1
                role_counts[row.get("Role", "").strip()] += 1

    print(f"Attendance files: {len(attendance_files)}")
    print(f"Total attendance records: {total_records}")
    print(f"Unique learner emails: {len(all_emails)}")
    print(f"Roles: {role_counts}")

    print("\nMost common session durations:")
    for duration, count in duration_counts.most_common(10):
        print(f"{duration}: {count}")

    return all_emails


def inspect_excel(data_dir):
    print("\n========== EXCEL SOURCE DETAILS ==========")

    excel_files = sorted(data_dir.rglob("*.xlsx"))

    for file in excel_files:
        print(f"\nFILE: {file.relative_to(data_dir)}")

        workbook = load_workbook(file, read_only=True, data_only=True)

        for sheet in workbook.worksheets:
            print(f"\nSHEET: {sheet.title}")

            rows = sheet.iter_rows(values_only=True)
            headers = next(rows, None)

            if headers is None:
                print("Empty sheet")
                continue

            print(f"Columns: {headers}")

            data_rows = list(rows)
            print(f"Data rows: {len(data_rows)}")

            if data_rows:
                print("Sample rows:")
                for row in data_rows[:3]:
                    print(row)

        workbook.close()


def main():
    parser = argparse.ArgumentParser(
        description="Inspect raw source data for a training track."
    )

    parser.add_argument(
        "track",
        choices=["aws_cloud", "power_bi"],
        help="Training track to inspect."
    )

    args = parser.parse_args()
    data_dir = RAW_DATA_DIR / args.track

    print(f"\nINSPECTING TRACK: {args.track.upper()}")
    print(f"Source directory: {data_dir}")

    if not data_dir.exists():
        raise FileNotFoundError(
            f"Track directory does not exist: {data_dir}"
        )

    inspect_attendance(data_dir)
    inspect_excel(data_dir)


if __name__ == "__main__":
    main()
