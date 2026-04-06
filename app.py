from fastapi import FastAPI
from env import EmailEnv
from models import Action

app = FastAPI()
env = EmailEnv()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    return env.reset().dict()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.value,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()
