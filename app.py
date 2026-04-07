from fastapi import FastAPI
from env import EmailEnv
from models import Action

app = FastAPI()
env = EmailEnv()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step():
    action = Action(action_type="reply")
    obs, reward, done, _ = env.step(action)

    return {
        "observation": obs.dict(),
        "reward": reward.value,
        "done": done
    }
