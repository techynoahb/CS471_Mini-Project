# For testing logic behind SQL queries

def test_get_item(mock_db):
    query_id = str(0).zfill(10)
    obj = mock_db.execute("SELECT object FROM inventoryTable WHERE rfid = ?;", (query_id,)).fetchone()

    assert obj is not None

def test_remove_item(mock_db):
    query_id = str(0).zfill(10)
    mock_db.execute("DELETE FROM inventoryTable WHERE rfid = (?);", (query_id,)).fetchone()
    obj = mock_db.execute("SELECT object FROM inventoryTable WHERE rfid = ?;", (query_id,)).fetchone()

    assert obj is None
