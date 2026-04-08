from app.services.debt import simplify_debts

def test_no_splits():
    result = simplify_debts([])
    assert result == []

def test_simple_debt():
    splits = [
        {"from_user": 2, "to_user": 1, "amount": 50.0}
    ]
    result = simplify_debts(splits)
    assert len(result) == 1
    assert result[0]["from_user"] == 2
    assert result[0]["to_user"] == 1
    assert result[0]["amount"] == 50.0

def test_debt_cancellation():
    # A owes B $50, B owes A $30 → net B owes A $20
    splits = [
        {"from_user": 2, "to_user": 1, "amount": 50.0},
        {"from_user": 1, "to_user": 2, "amount": 30.0}
    ]
    result = simplify_debts(splits)
    assert len(result) == 1
    assert result[0]["from_user"] == 2
    assert result[0]["to_user"] == 1
    assert result[0]["amount"] == 20.0

def test_three_person_simplification():
    splits = [
        {"from_user": 2, "to_user": 1, "amount": 50.0},
        {"from_user": 3, "to_user": 1, "amount": 50.0},
        {"from_user": 3, "to_user": 2, "amount": 30.0}
    ]
    result = simplify_debts(splits)
    total_owed = sum(t["amount"] for t in result)
    assert round(total_owed, 2) == 100.0

def test_equal_debts_cancel():
    # A owes B $50, B owes A $50 → net zero
    splits = [
        {"from_user": 1, "to_user": 2, "amount": 50.0},
        {"from_user": 2, "to_user": 1, "amount": 50.0}
    ]
    result = simplify_debts(splits)
    assert result == []