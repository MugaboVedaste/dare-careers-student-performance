
from pathlib import Path
from collections import Counter
import argparse

from openpyxl import load_workbook


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


def find_workbook(folder):
    """Find the Excel workbook in a track-specific folder."""
    files = sorted(
        file for file in folder.glob("*.xlsx")
        if not file.name.startswith("~$")
    )

    if not files:
        raise FileNotFoundError(
            f"No Excel workbook found in: {folder}"
        )

    if len(files) > 1:
        raise ValueError(
            f"Multiple Excel workbooks found in {folder}: "
            f"{[file.name for file in files]}"
        )

    return files[0]


def validate_assessments(data_dir):
    print("\n========== ASSESSMENT QUALITY ==========")

    folder = data_dir / "Labs & Quizes"
    file = find_workbook(folder)

    print("Assessment workbook:", file.name)

    workbook = load_workbook(file, read_only=True, data_only=True)

    for sheet_name in ["Labs", "Quizzes"]:
        if sheet_name not in workbook.sheetnames:
            raise ValueError(
                f"Missing worksheet '{sheet_name}' in {file.name}"
            )

        ws = workbook[sheet_name]

        rows = list(ws.iter_rows(values_only=True))

        if not rows:
            print(f"\n{sheet_name.upper()}: Empty worksheet")
            continue

        headers = list(rows[0])

        emails = []
        scores = []
        missing_scores = 0
        invalid_scores = 0
        duplicate_emails = 0
        seen_emails = set()

        week_columns = [
            header for header in headers
            if str(header).strip().lower().startswith("week")
        ]

        for row in rows[1:]:
            email = str(row[0] or "").strip().lower()

            if email in seen_emails:
                duplicate_emails += 1

            if email:
                seen_emails.add(email)
                emails.append(email)

            for score in row[1:]:
                if score is None or score == "":
                    missing_scores += 1
                    continue

                if (
                    not isinstance(score, (int, float))
                    or not 0 <= score <= 100
                ):
                    invalid_scores += 1
                    continue

                scores.append(score)

        print(f"\n{sheet_name.upper()}")
        print("Learner rows:", len(rows) - 1)
        print("Unique learner emails:", len(seen_emails))
        print("Weekly columns:", len(week_columns))
        print("Week column names:", week_columns)
        print("Missing scores:", missing_scores)
        print("Invalid scores:", invalid_scores)
        print("Duplicate learner emails:", duplicate_emails)

        if scores:
            print("Valid scores:", len(scores))
            print("Minimum score:", min(scores))
            print("Maximum score:", max(scores))

    workbook.close()


def validate_learner_status(data_dir):
    print("\n========== LEARNER STATUS QUALITY ==========")

    folder = data_dir / "Status of Learners"
    file = find_workbook(folder)

    print("Learner status workbook:", file.name)

    workbook = load_workbook(file, read_only=True, data_only=True)
    ws = workbook.active

    rows = list(ws.iter_rows(values_only=True))

    if not rows:
        raise ValueError(f"Empty learner status workbook: {file.name}")

    headers = list(rows[0])

    email_index = headers.index("email")
    graduation_index = headers.index("Graduation Status")
    certification_index = headers.index("Certification Status")

    seen_emails = set()
    missing_emails = 0
    duplicate_emails = 0
    graduation_counts = Counter()
    certification_counts = Counter()

    for row in rows[1:]:
        email = str(row[email_index] or "").strip().lower()

        if not email:
            missing_emails += 1
            continue

        if email in seen_emails:
            duplicate_emails += 1

        seen_emails.add(email)

        graduation_counts[row[graduation_index]] += 1
        certification_counts[row[certification_index]] += 1

    print("Learner records:", len(rows) - 1)
    print("Unique learner emails:", len(seen_emails))
    print("Missing emails:", missing_emails)
    print("Duplicate emails:", duplicate_emails)
    print("Graduation status:", graduation_counts)
    print("Certification status:", certification_counts)

    workbook.close()


def main():
    parser = argparse.ArgumentParser(
        description="Validate assessment and learner status data."
    )

    parser.add_argument(
        "track",
        choices=["aws_cloud", "power_bi"]
    )

    args = parser.parse_args()
    data_dir = RAW_DATA_DIR / args.track

    if not data_dir.exists():
        parser.error(f"Data directory does not exist: {data_dir}")

    print(f"\nVALIDATING TRACK: {args.track.upper()}")

    validate_assessments(data_dir)
    validate_learner_status(data_dir)


if __name__ == "__main__":
    main()
