import numpy as np,random
class QLearningAgent:
    def __init__(self):
        self.q=np.zeros((3,4));self.lr=0.1;self.gamma=0.9;self.eps=0.2
    def act(self,s):
        return random.randint(0,3) if random.random()<self.eps else int(self.q[s].argmax())
    def update(self,s,a,r,ns):
        self.q[s][a]+=self.lr*(r+self.gamma*self.q[ns].max()-self.q[s][a])
