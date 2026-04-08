"""
graders.py — Per-task graders for Email Triage RL OpenEnv.

Each grader returns a float strictly in (0.01, 0.99).
The openenv Phase 2 validator rejects exact 0.0 and exact 1.0.
"""
import math


def _clamp(score: float) -> float:
    """Force score strictly into (0.01, 0.99). Never 0.0 or 1.0."""
    if not math.isfinite(float(score)):
        return 0.01
    return max(0.01, min(0.99, float(score)))


def grade_easy(task, action_type, steps=None):
    """Easy: simple customer query — reply is correct."""
    if action_type == "reply":
        return _clamp(0.9)
    return _clamp(0.2)


def grade_medium(task, action_type, steps=None):
    """Medium: billing issue — escalate or request_info."""
    if action_type in ("request_info", "escalate"):
        return _clamp(0.85)
    return _clamp(0.2)


def grade_hard(task, action_type, steps=None):
    """Hard: urgent server issue — must escalate."""
    if action_type == "escalate":
        return _clamp(0.9)
    return _clamp(0.15)


def grade_archive(task, action_type, steps=None):
    """Newsletter: no action needed — archive it."""
    if action_type == "archive":
        return _clamp(0.9)
    return _clamp(0.15)


def grade_info(task, action_type, steps=None):
    """Info request: need more details — request_info."""
    if action_type == "request_info":
        return _clamp(0.9)
    return _clamp(0.2)


def grade_critical(task, action_type, steps=None):
    """Critical: data breach — must escalate immediately."""
    if action_type == "escalate":
        return _clamp(0.95)
    return _clamp(0.1)


def grade(task, action_type, steps=None):
    """Generic urgency-based grader (fallback)."""
    urgency = task.get("urgency", 5) if task else 5
    if urgency >= 7 and action_type == "escalate":
        return _clamp(0.9)
    elif urgency >= 4 and action_type == "request_info":
        return _clamp(0.9)
    elif urgency < 4 and action_type == "reply":
        return _clamp(0.9)
    return _clamp(0.2)
