import anthropic
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

async def categorize_expense(description: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": (
                "Categorize this travel expense into exactly one of: "
                "food, transport, accommodation, activities, shopping, other.\n"
                f"Expense: {description}\n"
                "Reply with just the category word, nothing else."
            )
        }]
    )
    return msg.content[0].text.strip().lower()

async def ask_budget_question(trip_data: dict, question: str) -> str:
    breakdown = "\n".join([f"  {k}: ${v:.2f}" for k, v in trip_data["breakdown"].items()])
    context = (
        f"Trip: {trip_data['name']}\n"
        f"Base currency: {trip_data['base_currency']}\n"
        f"Total budget: ${trip_data['budget']:.2f}\n"
        f"Total spent: ${trip_data['total_spent']:.2f}\n"
        f"Remaining: ${trip_data['budget'] - trip_data['total_spent']:.2f}\n"
        f"Spending by category:\n{breakdown}\n"
    )
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": (
                f"You are a smart travel budget assistant.\n"
                f"Here is the traveler's trip data:\n{context}\n"
                f"Question: {question}\n"
                f"Answer in 2-3 sentences, be specific and helpful."
            )
        }]
    )
    return msg.content[0].text.strip()

async def categorize_expense(description: str) -> str:
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": (
                    "Categorize this travel expense into exactly one of: "
                    "food, transport, accommodation, activities, shopping, other.\n"
                    f"Expense: {description}\n"
                    "Reply with just the category word, nothing else."
                )
            }]
        )
        return msg.content[0].text.strip().lower()
    except Exception as e:
        print(f"Claude error: {e}")
        return "other"