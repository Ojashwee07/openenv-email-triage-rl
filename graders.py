def grade_easy(task, action):
    """Grader for low urgency tasks - expects 'reply'"""
    if action.action_type == "reply":
        return 1.0
    return 0.0


def grade_medium(task, action):
    """Grader for medium urgency tasks - expects 'request_info' or 'escalate'"""
    if action.action_type in ("request_info", "escalate"):
        return 1.0
    return 0.0


def grade_hard(task, action):
    """Grader for high urgency tasks - expects 'escalate'"""
    if action.action_type == "escalate":
        return 1.0
    return 0.0


def grade(task, action):
    """Generic fallback grader based on urgency"""
    if task["urgency"] >= 7 and action.action_type == "escalate":
        return 1.0
    elif task["urgency"] >= 4 and action.action_type == "request_info":
        return 1.0
    elif task["urgency"] < 4 and action.action_type == "reply":
        return 1.0
    return 0.0
