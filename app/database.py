from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:Peekaboo96@localhost:5432/industrial_monitor"

engine = create_engine(DATABASE_URL)
class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def make_reminder_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        print(f"reminder {count} sent")
        return count

    return counter
counter = make_reminder_counter()

first = counter()
second = counter()

print(first)
print(second)

def test_counter():
    test_counter = make_reminder_counter()
    assert test_counter() == 1
    assert test_counter() == 2
    assert test_counter() == 3