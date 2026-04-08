"""
tasks.py — Task definitions for Email Triage RL OpenEnv.
All 6 tasks, each with its own grader function.
"""
from graders import (
    grade_easy, grade_medium, grade_hard,
    grade_archive, grade_info, grade_critical
)

TASKS = [
    {
        "id": "easy",
        "name": "Simple Customer Query",
        "description": "A straightforward question about working hours — reply is the correct action.",
        "email_text": "What are your working hours?",
        "sender": "customer",
        "urgency": 2,
        "correct_action": "reply",
        "difficulty": "easy",
        "max_steps": 3,
        "reward_threshold": 0.5,
        "grader": grade_easy,
        "grader_ref": "graders.grade_easy",
    },
    {
        "id": "medium",
        "name": "Billing Dispute",
        "description": "Customer charged twice — escalate or request more info.",
        "email_text": "I was charged twice, need refund",
        "sender": "customer",
        "urgency": 6,
        "correct_action": "escalate",
        "difficulty": "medium",
        "max_steps": 3,
        "reward_threshold": 0.5,
        "grader": grade_medium,
        "grader_ref": "graders.grade_medium",
    },
    {
        "id": "hard",
        "name": "Server Outage",
        "description": "Critical server down — must escalate immediately.",
        "email_text": "Server down urgent fix needed",
        "sender": "client",
        "urgency": 9,
        "correct_action": "escalate",
        "difficulty": "hard",
        "max_steps": 3,
        "reward_threshold": 0.5,
        "grader": grade_hard,
        "grader_ref": "graders.grade_hard",
    },
    {
        "id": "newsletter",
        "name": "Newsletter Archiving",
        "description": "Monthly marketing newsletter — archive it, no action needed.",
        "email_text": "Monthly newsletter - no action needed",
        "sender": "marketing",
        "urgency": 1,
        "correct_action": "archive",
        "difficulty": "easy",
        "max_steps": 3,
        "reward_threshold": 0.5,
        "grader": grade_archive,
        "grader_ref": "graders.grade_archive",
    },
    {
        "id": "info_request",
        "name": "Return Policy Inquiry",
        "description": "Customer asks to clarify return policy — request additional info.",
        "email_text": "Can you clarify the return policy?",
        "sender": "customer",
        "urgency": 5,
        "correct_action": "request_info",
        "difficulty": "medium",
        "max_steps": 3,
        "reward_threshold": 0.5,
        "grader": grade_info,
        "grader_ref": "graders.grade_info",
    },
    {
        "id": "critical",
        "name": "Security Data Breach",
        "description": "Data breach detected — escalate immediately, highest priority.",
        "email_text": "Data breach detected, immediate action required!",
        "sender": "security",
        "urgency": 10,
        "correct_action": "escalate",
        "difficulty": "hard",
        "max_steps": 3,
        "reward_threshold": 0.5,
        "grader": grade_critical,
        "grader_ref": "graders.grade_critical",
    },
]

# Dict lookup by ID for convenience
TASKS_BY_ID = {t["id"]: t for t in TASKS}
