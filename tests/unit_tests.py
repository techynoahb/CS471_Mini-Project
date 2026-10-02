import pytest
import sqlite3
from faker import Faker

@pytest.fixture(scope="module")
def mock_db():
    fake = Faker()
    db_con = sqlite3.connect(":memory:")
    cur = db_con.cursor()
    cur.execute("CREATE TABLE testTable (id INTEGER, obj STRING);")
    for i in range(10_000):
        cur.execute("INSERT INTO testTable (id, obj) VALUES (?, ?);", (str(i).zfill(4), fake.word()))

    db_con.commit()
    yield db_con
    db_con.close()

def test_get_item(mock_db):
    query_id = str(0).zfill(4)
    obj = mock_db.execute("SELECT obj FROM testTable WHERE id = ?;", (query_id,)).fetchone()

    print(obj)

    assert obj is not None