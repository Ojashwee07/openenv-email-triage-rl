"""
app.py — FastAPI server for Email Triage RL OpenEnv.

Implements full OpenEnv HTTP API including the /tasks endpoint
required for the Phase 2 Task Validation check.
"""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from env import EmailEnv
from models import Action
from tasks import TASKS, TASKS_BY_ID

app = FastAPI(
    title="Email Triage RL OpenEnv",
    description=(
        "Reinforcement learning environment for email triage. "
        "Agents classify emails and take actions: reply, escalate, archive, request_info."
    ),
    version="1.0.0",
)

# ── One env instance per task (lazy-init) ────────────────────────────────────
_envs: Dict[str, EmailEnv] = {}
_current_task_id: str = "easy"


def get_env(task_id: str = None) -> EmailEnv:
    global _current_task_id
    tid = task_id or _current_task_id
    if tid not in TASKS_BY_ID:
        tid = "easy"
    _current_task_id = tid
    if tid not in _envs:
        _envs[tid] = EmailEnv(task_id=tid)
    return _envs[tid]


# ── Request models ────────────────────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy"


class StepRequest(BaseModel):
    action_type: str
    task_id: Optional[str] = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "name": "Email Triage RL OpenEnv",
        "version": "1.0.0",
        "tasks": list(TASKS_BY_ID.keys()),
        "endpoints": ["/reset", "/step", "/state", "/tasks", "/health"],
        "spec": "openenv>=0.1.0",
    }


@app.get("/health")
async def health():
    return {"status": "ok", "environment": "email_triage_env"}


@app.get("/tasks")
async def list_tasks():
    """
    Return all available tasks with grader information.
    The openenv Phase 2 validator calls this endpoint to discover
    tasks with graders and verifies at least 3 are present.
    """
    return [
        {
            "id":               task["id"],
            "name":             task["name"],
            "description":      task["description"],
            "difficulty":       task["difficulty"],
            "max_steps":        task["max_steps"],
            "reward_threshold": task["reward_threshold"],
            "correct_action":   task["correct_action"],
            "grader":           task["grader_ref"],    # e.g. "graders.grade_easy"
            "has_grader":       True,
        }
        for task in TASKS
    ]


@app.post("/reset")
async def reset(request: Request):
    """Reset environment and return first observation."""
    try:
        try:
            body = await request.json()
        except Exception:
            body = {}
        task_id = str(body.get("task_id", "easy"))
        if task_id not in TASKS_BY_ID:
            task_id = "easy"

        env = get_env(task_id)
        obs = env.reset(task_id=task_id)
        return obs.dict()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/step")
async def step(request: Request):
    """Apply action and return next observation, reward, done."""
    try:
        try:
            body = await request.json()
        except Exception:
            body = {}

        task_id    = str(body.get("task_id", _current_task_id))
        action_str = str(body.get("action_type", "reply"))

        valid = ["reply", "escalate", "archive", "request_info"]
        if action_str not in valid:
            action_str = "request_info"

        env = get_env(task_id)
        if env.done:
            raise HTTPException(
                status_code=400,
                detail="Episode done. Call POST /reset to start a new episode.",
            )

        action = Action(action_type=action_str)
        obs, reward, done, info = env.step(action)

        return {
            "observation": obs.dict(),
            "reward":      reward.value,
            "done":        done,
            "info":        info,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/state")
async def state(task_id: Optional[str] = None):
    """Return current environment state."""
    try:
        env = get_env(task_id)
        return {
            "task":       env.task,
            "steps":      env.steps,
            "done":       env.done,
            "task_id":    env.task_id or _current_task_id,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Exception handler ─────────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def generic_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__},
    )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
