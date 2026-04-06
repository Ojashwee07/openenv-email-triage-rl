import random
ACTIONS=["reply","escalate","archive","request_info"]
TASKS=[{"email":"Working hours?","urgency":2,"correct":"reply"},{"email":"Refund issue","urgency":6,"correct":"escalate"},{"email":"Server down urgent","urgency":9,"correct":"escalate"}]
class EmailEnv:
    def __init__(self):
        self.state=None
        self.steps=0
    def reset(self):
        self.state=random.choice(TASKS)
        self.steps=0
        return self.state["urgency"]//3
    def step(self,action_idx):
        self.steps+=1
        action=ACTIONS[action_idx]
        correct=self.state["correct"]
        if action==correct: reward,done=1.0,True
        elif action=="request_info": reward,done=0.5,False
        else: reward,done=-0.5,False
        reward-=0.1*self.steps
        if self.steps>=3: done=True
        return self.state["urgency"]//3,reward,done
