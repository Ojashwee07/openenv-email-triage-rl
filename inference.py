import os
from openai import OpenAI
from env import EmailEnv
from models import Action

client = OpenAI(base_url=os.getenv("API_BASE_URL"), api_key=os.getenv("HF_TOKEN"))
MODEL = os.getenv("MODEL_NAME","gpt-4o-mini")

def get_action(obs):
    prompt=f"Email:{obs.email_text}\nUrgency:{obs.urgency}\nChoose: reply, escalate, archive, request_info"
    try:
        res=client.chat.completions.create(model=MODEL,messages=[{"role":"user","content":prompt}])
        text=res.choices[0].message.content.lower()
    except:
        text="request_info"

    for a in ["reply","escalate","archive","request_info"]:
        if a in text:
            return Action(action_type=a)
    return Action(action_type="request_info")

def run():
    env=EmailEnv()
    scores=[]
    for _ in range(3):
        obs=env.reset()
        done=False
        while not done:
            action=get_action(obs)
            obs,reward,done,_=env.step(action)
        scores.append(reward.value)
    print("Final Score:",sum(scores)/len(scores))

if __name__=="__main__":
    run()
