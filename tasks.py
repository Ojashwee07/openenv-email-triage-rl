from graders import grade_easy, grade_medium, grade_hard, grade_archive, grade_info, grade_critical

TASKS = [
    {
        "id": "easy",
        "email_text": "What are your working hours?",
        "sender": "customer",
        "urgency": 2,
        "correct_action": "reply",
        "grader": grade_easy
    },
    {
        "id": "medium",
        "email_text": "I was charged twice, need refund",
        "sender": "customer",
        "urgency": 6,
        "correct_action": "escalate",
        "grader": grade_medium
    },
    {
        "id": "hard",
        "email_text": "Server down urgent fix needed",
        "sender": "client",
        "urgency": 9,
        "correct_action": "escalate",
        "grader": grade_hard
    },
    {
        "id": "newsletter",
        "email_text": "Monthly newsletter - no action needed",
        "sender": "marketing",
        "urgency": 1,
        "correct_action": "archive",
        "grader": grade_archive
    },
    {
        "id": "info_request",
        "email_text": "Can you clarify the return policy?",
        "sender": "customer",
        "urgency": 5,
        "correct_action": "request_info",
        "grader": grade_info
    },
    {
        "id": "critical",
        "email_text": "Data breach detected, immediate action required!",
        "sender": "security",
        "urgency": 10,
        "correct_action": "escalate",
        "grader": grade_critical
    },
]
