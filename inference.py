import os
from env import EmailEnv
from models import Action
from openai import OpenAI

# ✅ MUST use these env variables (IMPORTANT)
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")


def get_action(obs):
    try:
        prompt = f"""
You are an email triage assistant.

Email: {obs.email_text}
Urgency: {obs.urgency}

Choose ONLY ONE action from:
reply, escalate, archive, request_info
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5  # 🔥 keep low to save tokens
        )

        action_text = response.choices[0].message.content.strip().lower()

        # ✅ safety check
        if action_text not in ["reply", "escalate", "archive", "request_info"]:
            action_text = "request_info"

        return Action(action_type=action_text)

    except Exception:
        # ✅ fallback (never crash)
        if obs.urgency >= 7:
            return Action(action_type="escalate")
        elif obs.urgency >= 4:
            return Action(action_type="request_info")
        else:
            return Action(action_type="reply")


def run():
    env = EmailEnv()
    scores = []

    print("[START] OpenEnv Evaluation")

    for i in range(3):
        obs = env.reset()
        done = False

        print(f"[STEP] Task {i+1} started")

        while not done:
            action = get_action(obs)
            obs, reward, done, _ = env.step(action)

            print(f"[STEP] Action={action.action_type}, Reward={reward.value}")

        scores.append(reward.value)
        print(f"[STEP] Task {i+1} completed")

    final_score = sum(scores) / len(scores)

    print(f"[END] Final Score={final_score}")


if __name__ == "__main__":
    run()
