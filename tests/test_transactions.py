# tests/test_transactions.py
from datetime import date

def test_create_transaction(client):
    payload = {
        "date": "2025-08-01",
        "amount": 23.45,
        "merchant": "Cafe",
        "description": "Latte",
        "category": "Food"
    }
    r = client.post("/transactions", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] > 0
    assert data["user_id"] == 1
    assert data["merchant"] == "Cafe"
    assert data["amount"] == 23.45

def test_get_transaction_by_id(client):
    # create one
    r = client.post("/transactions", json={
        "date": "2025-08-02",
        "amount": 50.00,
        "merchant": "Uber",
        "description": "Ride downtown",
        "category": "Transport"
    })
    tx_id = r.json()["id"]

    # retrieve it
    r2 = client.get(f"/transactions/{tx_id}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["id"] == tx_id
    assert data["merchant"] == "Uber"

def test_list_transactions_with_filters(client):
    # seed a few
    client.post("/transactions", json={
        "date": "2025-02-01",
        "amount": 20.00,
        "merchant": "GMarket",
        "description": "Groceries",
        "category": "Food"
    })
    client.post("/transactions", json={
        "date": "2025-02-15",
        "amount": 12.00,
        "merchant": "Bus Co",
        "description": "Bus ticket",
        "category": "Transport"
    })
    client.post("/transactions", json={
        "date": "2025-03-01",
        "amount": 35.00,
        "merchant": "GMarket",
        "description": "More groceries",
        "category": "Food"
    })

    # Filter Feb only, category=Food, search "gro"
    r = client.get("/transactions", params={
        "from_date": "2025-02-01",
        "to_date": "2025-02-28",
        "category": "Food",
        "q": "gro"
    })
    assert r.status_code == 200
    items = r.json()
    # Only the 2025-02-01 Food/Groceries should match
    assert len(items) == 1
    assert items[0]["description"].lower().startswith("gro")

def test_update_transaction(client):
    # create
    r = client.post("/transactions", json={
        "date": "2025-08-03",
        "amount": 10.00,
        "merchant": "Kiosk",
        "description": "Snack",
        "category": "Food"
    })
    tx_id = r.json()["id"]

    # update
    r2 = client.put(f"/transactions/{tx_id}", json={
        "date": "2025-08-03",
        "amount": 15.50,
        "merchant": "Kiosk",
        "description": "Snack + drink",
        "category": "Food"
    })
    assert r2.status_code == 200
    updated = r2.json()
    assert updated["amount"] == 15.50
    assert updated["description"] == "Snack + drink"

def test_delete_transaction(client):
    # create
    r = client.post("/transactions", json={
        "date": "2025-08-04",
        "amount": 8.90,
        "merchant": "7-Eleven",
        "description": "Water",
        "category": "Other"
    })
    tx_id = r.json()["id"]

    # delete
    r2 = client.delete(f"/transactions/{tx_id}")
    assert r2.status_code == 200

    # ensure gone
    r3 = client.get(f"/transactions/{tx_id}")
    assert r3.status_code == 404
