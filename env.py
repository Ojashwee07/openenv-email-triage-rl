import random
from models import Observation, Action, Reward
from tasks import TASKS
from graders import grade

class EmailEnv:
    def __init__(self):
        self.task = None
        self.steps = 0
        self.done = False

    def reset(self):
        self.task = random.choice(TASKS)
        self.steps = 0
        self.done = False

        return Observation(
            email_text=self.task["email_text"],
            sender=self.task["sender"],
            urgency=self.task["urgency"],
            step_count=self.steps
        )

    def state(self):
        return self.task

    def step(self, action: Action):
        self.steps += 1

        if action.action_type not in ["reply","escalate","archive","request_info"]:
            action.action_type = "request_info"

        score = grade(self.task, action.action_type, self.steps)
        reward = Reward(value=score)

        if score >= 0.9 or self.steps >= 3:
            self.done = True

        obs = Observation(
            email_text=self.task["email_text"],
            sender=self.task["sender"],
            urgency=self.task["urgency"],
            step_count=self.steps
        )

        return obs, reward, self.done, {}
