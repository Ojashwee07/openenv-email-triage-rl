from env import EmailEnv
from agent import QLearningAgent
def train(n=500):
    env,agent=EmailEnv(),QLearningAgent()
    for _ in range(n):
        s=env.reset();done=False
        while not done:
            a=agent.act(s)
            ns,r,done=env.step(a)
            agent.update(s,a,r,ns)
            s=ns
    return agent
