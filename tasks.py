from graders import grade_easy, grade_medium, grade_hard

TASKS = [
    {
        "id": "easy",
        "email_text": "What are your working hours?",
        "sender": "customer",
        "urgency": 2,
        "correct_action": "reply",
        "grader": grade_easy          # ✅ Grader added
    },
    {
        "id": "medium",
        "email_text": "I was charged twice, need refund",
        "sender": "customer",
        "urgency": 6,
        "correct_action": "escalate",
        "grader": grade_medium        # ✅ Grader added
    },
    {
        "id": "hard",
        "email_text": "Server down urgent fix needed",
        "sender": "client",
        "urgency": 9,
        "correct_action": "escalate",
        "grader": grade_hard          # ✅ Grader added
    },
]
