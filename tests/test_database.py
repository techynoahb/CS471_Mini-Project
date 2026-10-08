def test_get_item(mock_db):
    query_id = str(0).zfill(10)
    obj = mock_db.execute("SELECT object FROM inventoryTable WHERE rfid = ?;", (query_id,)).fetchone()

    assert obj is not None
