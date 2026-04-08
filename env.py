"""
env.py — Email Triage RL OpenEnv Environment.

Supports both random task selection (legacy) and specific task_id selection.
"""
import random
from models import Observation, Action, Reward
from tasks import TASKS, TASKS_BY_ID
from graders import grade


class EmailEnv:
    def __init__(self, task_id: str = None):
        self.task = None
        self.task_id = task_id   # if set, always use this task
        self.steps = 0
        self.done = False

    def reset(self, task_id: str = None) -> Observation:
        """Reset environment. If task_id given, use that task; else random."""
        tid = task_id or self.task_id
        if tid and tid in TASKS_BY_ID:
            self.task = TASKS_BY_ID[tid]
        else:
            self.task = random.choice(TASKS)

        self.steps = 0
        self.done = False

        return Observation(
            email_text=self.task["email_text"],
            sender=self.task["sender"],
            urgency=self.task["urgency"],
            step_count=self.steps,
        )

    def state(self):
        return self.task

    def step(self, action: Action):
        self.steps += 1

        valid_actions = ["reply", "escalate", "archive", "request_info"]
        if action.action_type not in valid_actions:
            action.action_type = "request_info"

        # Use the task-specific grader
        grader_fn = self.task.get("grader", grade)
        score = grader_fn(self.task, action.action_type, self.steps)

        # Ensure score is strictly in (0.01, 0.99)
        score = max(0.01, min(0.99, float(score)))

        reward = Reward(value=score)

        if score >= 0.85 or self.steps >= self.task.get("max_steps", 3):
            self.done = True

        obs = Observation(
            email_text=self.task["email_text"],
            sender=self.task["sender"],
            urgency=self.task["urgency"],
            step_count=self.steps,
        )

        return obs, reward, self.done, {}
