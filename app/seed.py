from app.database import SessionLocal, init_db
from app.models import User
from app.auth.utils import get_password_hash


def seed_database():
    """Seed the database with initial data."""
    print("Initializing database...")

    try:
        init_db()
        print("✓ Database tables created")
    except Exception as e:
        print(f"Warning during database initialization: {e}")

    db = SessionLocal()

    try:
        # Check if demo user exists
        existing_user = db.query(User).filter(User.email == "demo@example.com").first()

        if existing_user:
            print("✓ Demo user already exists.")
        else:
            # Create demo user with a shorter password
            demo_password = "demo123"

            try:
                hashed_password = get_password_hash(demo_password)
                demo_user = User(
                    email="demo@example.com",
                    hashed_password=hashed_password,
                )
                db.add(demo_user)
                db.commit()
                print("✓ Created demo user:")
                print("  Email: demo@example.com")
                print("  Password: demo123")
            except Exception as hash_error:
                print(f"Error hashing password: {hash_error}")
                # Try alternative: use a simpler password or check bcrypt installation
                raise

        print("\n✓ Database seeded successfully!")
        print("\nYou can now start the server with:")
        print("  uvicorn app.main:app --reload")
        print("\nOr use:")
        print("  make dev")

    except Exception as e:
        print(f"Error seeding database: {e}")
        print("\nTroubleshooting:")
        print("1. Uninstall and reinstall bcrypt:")
        print("   pip uninstall bcrypt passlib")
        print("   pip install bcrypt==4.0.1 passlib[bcrypt]==1.7.4")
        print("\n2. If error persists, try:")
        print("   pip install bcrypt==4.1.2")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()