"""Seed the curated interview question bank.

Run from the backend directory:

    python seed_db.py
"""

from app.core.database import SessionLocal
from app.services.question_bank_seed import seed_question_bank


def main() -> None:
    db = SessionLocal()
    try:
        inserted = seed_question_bank(db)
    finally:
        db.close()
    print(f"Question bank seeding complete. Rows inserted: {inserted}")


if __name__ == "__main__":
    main()
