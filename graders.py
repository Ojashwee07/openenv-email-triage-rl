def grade(task, action, steps):
    correct = task["correct_action"]

    if action == correct:
        score = 1.0
    elif action == "request_info":
        score = 0.5
    else:
        score = 0.0

    score -= 0.1 * steps
    return max(0.0, min(1.0, score))
