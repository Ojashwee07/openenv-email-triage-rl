import numpy as np
from train import train
from env import EmailEnv
def test():
    agent=train()
    env=EmailEnv();total=0
    for _ in range(10):
        s=env.reset();done=False
        while not done:
            a=int(agent.q[s].argmax())
            s,r,done=env.step(a)
            total+=r
    print("Avg Reward:",total/10)
if __name__=="__main__": test()
