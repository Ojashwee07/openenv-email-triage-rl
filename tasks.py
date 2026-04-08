
Copy

TASKS = [
    {
        "id": "easy",
        "email_text": "What are your working hours?",
        "sender": "customer",
        "urgency": 2,
        "correct_action": "reply",
        "grader": {
            "type": "exact_match",
            "expected_action": "reply"
        }
    },
    {
        "id": "medium",
        "email_text": "I was charged twice, need refund",
        "sender": "customer",
        "urgency": 6,
        "correct_action": "escalate",
        "grader": {
            "type": "exact_match",
            "expected_action": "escalate"
        }
    },
    {
        "id": "hard",
        "email_text": "Server down urgent fix needed",
        "sender": "client",
        "urgency": 9,
        "correct_action": "escalate",
        "grader": {
            "type": "exact_match",
            "expected_action": "escalate"
        }
    }
]
