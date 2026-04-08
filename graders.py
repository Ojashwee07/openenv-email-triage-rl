def grade_easy(task, action_type, steps=None):
    """Grader for low urgency tasks - expects 'reply'"""
    if action_type == "reply":
        return 1.0
    return 0.0


def grade_medium(task, action_type, steps=None):
    """Grader for medium urgency tasks - expects 'request_info' or 'escalate'"""
    if action_type in ("request_info", "escalate"):
        return 1.0
    return 0.0


def grade_hard(task, action_type, steps=None):
    """Grader for high urgency tasks - expects 'escalate'"""
    if action_type == "escalate":
        return 1.0
    return 0.0


def grade(task, action_type, steps=None):
    """Generic fallback grader based on urgency"""
    if task["urgency"] >= 7 and action_type == "escalate":
        return 1.0
    elif task["urgency"] >= 4 and action_type == "request_info":
        return 1.0
    elif task["urgency"] < 4 and action_type == "reply":
        return 1.0
    return 0.0
