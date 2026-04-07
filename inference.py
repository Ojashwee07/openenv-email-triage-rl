import os
from openai import OpenAI
from env import EmailEnv
from models import Action

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")


def get_action(obs):
    prompt = f"""
    Email: {obs.email_text}
    Urgency: {obs.urgency}
    Choose one action: reply, escalate, archive, request_info
    """

    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        text = res.choices[0].message.content.lower()
    except:
        text = "request_info"

    for a in ["reply", "escalate", "archive", "request_info"]:
        if a in text:
            return Action(action_type=a)

    return Action(action_type="request_info")


def run():
    env = EmailEnv()
    scores = []

    print("[START] Running OpenEnv Evaluation")

    for i in range(3):
        obs = env.reset()
        done = False

        print(f"[STEP] Task {i+1} started")

        while not done:
            action = get_action(obs)
            obs, reward, done, _ = env.step(action)

            print(f"[STEP] Action: {action.action_type}, Reward: {reward.value}")

        scores.append(reward.value)
        print(f"[STEP] Task {i+1} completed with score: {reward.value}")

    final_score = sum(scores) / len(scores)

    print("[END] Final Score:", final_score)


if __name__ == "__main__":
    run()
