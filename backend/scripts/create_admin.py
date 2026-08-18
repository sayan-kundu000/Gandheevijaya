"""
Gandheevijaya Admin Bootstrap CLI Script.

Allows controlled creation or promotion of administrator accounts.
Never executed automatically on application startup.

Usage:
  python backend/scripts/create_admin.py --email admin@gandheevijaya.com --password SecureAdminPass123! --name "System Admin"
"""
import argparse
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from sqlalchemy import select

from backend.app.core.database import SessionLocal
from backend.app.core.security import get_password_hash
from backend.app.models.user import User
from backend.app.services.auth_service import log_security_event


def create_or_promote_admin(email: str, password: str, full_name: str = "Administrator") -> None:
    normalized_email = email.strip().lower()
    if len(password) < 8:
        print("Error: Password must be at least 8 characters long.")
        sys.exit(1)

    db = SessionLocal()
    try:
        user = db.scalar(select(User).where(User.email == normalized_email))
        hashed_pwd = get_password_hash(password)

        if user:
            print(f"Found existing user with email [{normalized_email}]. Promoting role to ADMIN...")
            user.role = "ADMIN"
            user.password_hash = hashed_pwd
            user.is_active = True
            user.full_name = full_name or user.full_name
            log_security_event(db, event_type="ADMIN_PROMOTED", user_id=user.id, details={"action": "CLI_BOOTSTRAP"})
            db.commit()
            print(f"Success: User [{normalized_email}] is now an ADMINISTRATOR.")
        else:
            print(f"Creating new ADMINISTRATOR account for [{normalized_email}]...")
            new_admin = User(
                email=normalized_email,
                password_hash=hashed_pwd,
                full_name=full_name,
                role="ADMIN",
                is_active=True,
            )
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            log_security_event(db, event_type="ADMIN_CREATED", user_id=new_admin.id, details={"action": "CLI_BOOTSTRAP"})
            db.commit()
            print(f"Success: Created new ADMINISTRATOR account with ID [{new_admin.id}].")
    except Exception as exc:
        db.rollback()
        print(f"Error bootstrapping admin user: {exc}")
        sys.exit(1)
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Gandheevijaya Administrator Account Bootstrap CLI")
    parser.add_argument("--email", required=True, help="Administrator email address")
    parser.add_argument("--password", required=True, help="Administrator initial password (min 8 chars)")
    parser.add_argument("--name", default="System Administrator", help="Administrator full name")

    args = parser.parse_args()
    create_or_promote_admin(email=args.email, password=args.password, full_name=args.name)


if __name__ == "__main__":
    main()
