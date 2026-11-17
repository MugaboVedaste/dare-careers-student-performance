
from pathlib import Path
from collections import Counter
import csv

from openpyxl import load_workbook

DATA_DIR = Path("data/raw/power_bi")


def profile_attendance():
    print("\n========== POWER BI ATTENDANCE ==========")

    files = list(DATA_DIR.glob("Zoom Attendance/Week */*.csv"))
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


def profile_workbooks():
    print("\n========== POWER BI EXCEL WORKBOOKS ==========")

    for file in DATA_DIR.rglob("*.xlsx"):
        print(f"\nFILE: {file.name}")

        workbook = load_workbook(
            file, read_only=True, data_only=True
        )

        for sheet in workbook.worksheets:
            print(f"\nSHEET: {sheet.title}")

            rows = sheet.iter_rows(values_only=True)
            header = next(rows, None)

            print("Columns:", header)

            row_count = 0
            for _ in rows:
                row_count += 1

            print("Data rows:", row_count)

        workbook.close()


if __name__ == "__main__":
    profile_attendance()
    profile_workbooks()
