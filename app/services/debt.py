from collections import defaultdict
from typing import List, Dict

def simplify_debts(splits: List[Dict]) -> List[Dict]:
    """
    Takes a list of expense splits and returns the minimum
    number of transactions needed to settle all debts.

    splits: [{"from_user": 1, "to_user": 2, "amount": 50.0}, ...]
    returns: [{"from_user": 1, "to_user": 2, "amount": 20.0}, ...]
    """

    # Step 1 — calculate net balance for each person
    # positive means they are owed money
    # negative means they owe money
    balance = defaultdict(float)

    for split in splits:
        balance[split["to_user"]] += split["amount"]    # person who paid is owed
        balance[split["from_user"]] -= split["amount"]  # person who owes loses balance

    # Step 2 — separate into creditors (owed money) and debtors (owe money)
    creditors = []  # [(amount, user_id), ...]
    debtors = []    # [(amount, user_id), ...]

    for user_id, net in balance.items():
        if net > 0.01:
            creditors.append([net, user_id])
        elif net < -0.01:
            debtors.append([-net, user_id])

    # Step 3 — greedily match debtors to creditors
    transactions = []

    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debt_amount, debtor = debtors[i]
        credit_amount, creditor = creditors[j]

        settled = min(debt_amount, credit_amount)

        transactions.append({
            "from_user": debtor,
            "to_user": creditor,
            "amount": round(settled, 2)
        })

        debtors[i][0] -= settled
        creditors[j][0] -= settled

        if debtors[i][0] < 0.01:
            i += 1
        if creditors[j][0] < 0.01:
            j += 1

    return transactions


def get_trip_splits(db, trip_id: int) -> List[Dict]:
    """
    Fetches all unsettled expense splits for a trip
    and formats them for the simplify_debts function.
    """
    from app.models.expense import Expense
    from app.models.member import TripMember

    expenses = db.query(Expense).filter(Expense.trip_id == trip_id).all()

    splits = []
    for expense in expenses:
        for split in expense.splits:
            if not split.settled:
                splits.append({
                    "from_user": split.user_id,
                    "to_user": expense.paid_by,
                    "amount": split.amount_owed
                })

    return splits