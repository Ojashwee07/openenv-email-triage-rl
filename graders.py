def grade_easy(task, action_type, steps=None):
    if action_type == "reply":
        return 0.9
    return 0.1

def grade_medium(task, action_type, steps=None):
    if action_type in ("request_info", "escalate"):
        return 0.9
    return 0.1

def grade_hard(task, action_type, steps=None):
    if action_type == "escalate":
        return 0.9
    return 0.1

def grade_archive(task, action_type, steps=None):
    if action_type == "archive":
        return 0.9
    return 0.1

def grade_info(task, action_type, steps=None):
    if action_type == "request_info":
        return 0.9
    return 0.1

def grade_critical(task, action_type, steps=None):
    if action_type == "escalate":
        return 0.9
    return 0.1

def grade(task, action_type, steps=None):
    if task["urgency"] >= 7 and action_type == "escalate":
        return 0.9
    elif task["urgency"] >= 4 and action_type == "request_info":
        return 0.9
    elif task["urgency"] < 4 and action_type == "reply":
        return 0.9
    return 0.1
