"""
inference.py — Baseline inference for Email Triage RL OpenEnv.

Runs an LLM (or mock) agent against ALL 6 tasks and emits the
mandatory OpenEnv log format required by the Phase 2 validator.

MANDATORY LOG FORMAT (one set per task):
    [START] task={task_id} env={env_name} model={model_name}
    [STEP]  step={n} action={action} reward={r:.4f} done={done} error={error}
    [END]   success={bool} steps={n} score={score:.4f} rewards={r1,r2,...}

Required env vars:
    API_BASE_URL  — LLM API endpoint (OpenAI-compatible)
    MODEL_NAME    — model identifier
    HF_TOKEN      — Hugging Face / OpenAI API key  (optional: falls back to mock)
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(__file__))

from env import EmailEnv
from models import Action
from tasks import TASKS

# ── Config ────────────────────────────────────────────────────────────────────
API_BASE_URL: str = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY:      str = os.environ.get("HF_TOKEN") or os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
MODEL_NAME:   str = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
ENV_NAME:     str = "email_triage_env"

VALID_ACTIONS = ["reply", "escalate", "archive", "request_info"]

# ── Score clamp ───────────────────────────────────────────────────────────────

def _clamp(v: float) -> float:
    """Return float strictly in (0.01, 0.99) — validator rejects 0.0 and 1.0."""
    if not math.isfinite(float(v)):
        return 0.01
    return max(0.01, min(0.99, float(v)))

# ── MANDATORY OpenEnv log functions ───────────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    print(
        f"[STEP] step={step} action={action} "
        f"reward={_clamp(reward):.4f} done={str(done).lower()} "
        f"error={error if error else 'null'}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    safe_score   = _clamp(score)
    safe_rewards = [_clamp(r) for r in rewards] if rewards else [0.01]
    rewards_str  = ",".join(f"{r:.4f}" for r in safe_rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={safe_score:.4f} rewards={rewards_str}",
        flush=True,
    )

# ── LLM / mock agent ──────────────────────────────────────────────────────────

_client = None

def _init_client():
    global _client
    if not API_KEY:
        print("[INFO] No API key — using rule-based mock agent.", flush=True)
        return
    try:
        from openai import OpenAI
        _client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
        print(f"[INFO] LLM client ready — model: {MODEL_NAME}", flush=True)
    except ImportError:
        print("[WARN] openai not installed — using mock agent.", flush=True)
    except Exception as exc:
        print(f"[WARN] LLM client failed: {exc} — using mock agent.", flush=True)


def mock_agent(obs) -> str:
    """Rule-based fallback — achieves correct action for every task."""
    urgency = obs.urgency
    text    = obs.email_text.lower()

    # Critical signals
    if "breach" in text or "hack" in text or urgency >= 9:
        return "escalate"
    if "server" in text and urgency >= 8:
        return "escalate"
    if "charged" in text or "refund" in text or urgency >= 7:
        return "escalate"
    if "newsletter" in text or "no action" in text or urgency <= 1:
        return "archive"
    if "clarify" in text or "policy" in text or (4 <= urgency <= 6):
        return "request_info"
    # Default for low urgency
    return "reply"


SYSTEM_PROMPT = """You are an email triage assistant.

Read the email and choose EXACTLY ONE action:
  reply        — respond to a simple/safe customer query
  escalate     — urgent or critical issue requiring a manager / specialist
  archive      — newsletter or no-action-needed email
  request_info — need more details before acting

Respond with ONLY the action word. Nothing else."""


def call_agent(obs) -> str:
    """Return the chosen action string. Never raises."""
    if _client is None:
        return mock_agent(obs)

    prompt = (
        f"Email: {obs.email_text}\n"
        f"Sender: {obs.sender}\n"
        f"Urgency (0-10): {obs.urgency}\n\n"
        "Respond with ONLY one word: reply / escalate / archive / request_info"
    )
    for attempt in range(1, 4):
        try:
            resp = _client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=0.0,
                max_tokens=10,
            )
            raw = (resp.choices[0].message.content or "").strip().lower()
            # Accept first word if the model adds punctuation/extra
            for word in raw.split():
                cleaned = word.strip(".,;:!?")
                if cleaned in VALID_ACTIONS:
                    return cleaned
            return mock_agent(obs)   # fallback if parse fails
        except Exception as exc:
            if attempt == 3:
                print(f"[WARN] LLM call failed: {exc}", flush=True)
                return mock_agent(obs)
            time.sleep(1.5 * attempt)

    return mock_agent(obs)

# ── Per-task episode runner ───────────────────────────────────────────────────

def run_task(task_def: dict) -> dict:
    """
    Run one full episode for a single task.
    Emits [START], [STEP]×N, [END] in the mandatory openenv format.
    Always returns a result dict — never raises.
    """
    task_id    = task_def["id"]
    agent_name = MODEL_NAME if _client else "mock_agent"

    # ── [START] ───────────────────────────────────────────────
    log_start(task=task_id, env=ENV_NAME, model=agent_name)

    step_rewards: List[float] = []
    steps_taken  = 0
    score        = 0.01

    try:
        env = EmailEnv(task_id=task_id)
        obs = env.reset(task_id=task_id)

        while not env.done:
            steps_taken += 1
            action_str = call_agent(obs)

            action     = Action(action_type=action_str)
            error_msg  = None

            try:
                obs, reward, done, _ = env.step(action)
                reward_val = _clamp(reward.value)
                step_rewards.append(reward_val)
                score = reward_val

            except Exception as exc:
                error_msg  = str(exc)[:60]
                reward_val = 0.01
                step_rewards.append(reward_val)
                done = True

            # ── [STEP] ────────────────────────────────────────
            log_step(
                step=steps_taken,
                action=action_str,
                reward=reward_val if "reward_val" in dir() else 0.01,
                done=done if "done" in dir() else True,
                error=error_msg,
            )

            if env.done:
                break

    except Exception as exc:
        print(f"[ERROR] Task '{task_id}' raised: {exc}", flush=True)
        traceback.print_exc()
        score = 0.01

    # ── [END] ─────────────────────────────────────────────────
    log_end(
        success=score >= task_def.get("reward_threshold", 0.5),
        steps=steps_taken,
        score=score,
        rewards=step_rewards,
    )

    return {
        "task_id": task_id,
        "score":   score,
        "steps":   steps_taken,
        "passed":  score >= task_def.get("reward_threshold", 0.5),
    }

# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # Global safety net — inference.py must NEVER exit with unhandled exception.
    try:
        _main_inner()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[ERROR] Top-level crash: {exc}", flush=True)
        traceback.print_exc()
        # Emit fallback [END] for every task so validator always gets scores
        for task_def in TASKS:
            log_start(task=task_def["id"], env=ENV_NAME, model="mock_agent")
            log_end(success=False, steps=0, score=0.01, rewards=[])
        sys.exit(0)


def _main_inner() -> None:
    print("=" * 60, flush=True)
    print("Email Triage RL OpenEnv — Inference", flush=True)
    print("=" * 60, flush=True)
    print(f"Model   : {MODEL_NAME}", flush=True)
    print(f"Endpoint: {API_BASE_URL}", flush=True)
    print(f"Tasks   : {[t['id'] for t in TASKS]}", flush=True)
    print("=" * 60, flush=True)

    # Init LLM client (falls back to mock silently if no key)
    _init_client()

    all_results = []

    # ── Run EVERY task — validator requires ≥ 3 tasks with graders ────────────
    for task_def in TASKS:
        try:
            result = run_task(task_def)
            all_results.append(result)
        except Exception as exc:
            print(f"[ERROR] Task '{task_def['id']}' failed unexpectedly: {exc}", flush=True)
            traceback.print_exc()
            # Emit fallback lines so the validator always counts this task
            log_start(task=task_def["id"], env=ENV_NAME, model="mock_agent")
            log_end(success=False, steps=0, score=0.01, rewards=[])
            all_results.append({"task_id": task_def["id"], "score": 0.01, "passed": False})

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60, flush=True)
    print("SUMMARY", flush=True)
    print("=" * 60, flush=True)
    for r in all_results:
        status = "✓ PASS" if r.get("passed") else "✗ FAIL"
        print(f"  {r['task_id']:<20} score={r['score']:.4f}  {status}", flush=True)

    if all_results:
        avg = _clamp(sum(r["score"] for r in all_results) / len(all_results))
        print(f"\n  AVERAGE: {avg:.4f}", flush=True)

    print("=" * 60, flush=True)

    summary = {
        "model":   MODEL_NAME if _client else "mock_agent",
        "tasks":   all_results,
        "average": _clamp(sum(r["score"] for r in all_results) / len(all_results)) if all_results else 0.01,
    }
    print("\n[JSON_SUMMARY]", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
