import os
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import Employee, Task, SystemConfig
from app.auth import hash_password
from app.config import settings
from app.services.excel_service import validate_spreadsheet, import_validated_rows

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed Administrator
        admin = db.query(Employee).filter(Employee.role == "ADMIN").first()
        if not admin:
            admin = Employee(
                employee_id="ADM001",
                name="System Administrator",
                email=settings.DEFAULT_ADMIN_EMAIL.lower(),
                department="Management",
                role="ADMIN",
                password_hash=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
                is_active=True
            )
            db.add(admin)
            db.commit()
            print(f"[Seed] Created admin: {admin.email}")

        # 2. Seed 100 sample employees and tasks if none exist
        task_count = db.query(Task).count()
        if task_count == 0:
            sample_file = os.path.join(os.path.dirname(__file__), "sample_data", "employees_100_tasks.xlsx")
            if os.path.exists(sample_file):
                with open(sample_file, "rb") as f:
                    content = f.read()
                val_result = validate_spreadsheet(content, "employees_100_tasks.xlsx", db)
                if val_result.valid_rows_count > 0:
                    import_res = import_validated_rows(val_result.preview_rows, db, overwrite_existing=False)
                    print(f"[Seed] Imported {import_res['employees_created']} employees and {import_res['tasks_created']} tasks from spreadsheet!")
            else:
                print(f"[Seed] Sample file {sample_file} not found.")
        else:
            print(f"[Seed] Database already contains {task_count} tasks.")

    except Exception as e:
        print(f"[Seed] Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
