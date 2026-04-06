# 🚀 OpenEnv + Reinforcement Learning: Email Triage Environment

## 📌 Overview
This project implements a **real-world OpenEnv environment** simulating an automated email triage system.  
An AI agent must decide how to handle incoming emails (reply, escalate, archive, or request information).

Additionally, we extend the system with a **Reinforcement Learning (Q-learning) agent** that learns optimal decision-making policies based on rewards.

---

## 🧠 Features

### ✅ OpenEnv Environment
- Fully compliant with OpenEnv specification
- Implements:
  - `reset()`
  - `step()`
  - `state()`
- Typed models using Pydantic
- FastAPI endpoints for interaction
- Deterministic grading system

### 🤖 AI Inference
- Uses OpenAI client
- Reads:
  - `API_BASE_URL`
  - `MODEL_NAME`
  - `HF_TOKEN`
- Produces reproducible baseline scores

### 🏆 Reinforcement Learning (Bonus)
- Q-learning agent
- Learns optimal actions from reward signals
- Improves performance over time

---

## 🎯 Tasks

| Task | Description | Difficulty |
|------|------------|------------|
| Easy | General queries (working hours) | 🟢 |
| Medium | Refund / billing issues | 🟡 |
| Hard | Critical system issues | 🔴 |

---

## 📊 Reward System

- Correct action → `+1.0`
- Partial action → `+0.5`
- Wrong action → `0.0`
- Step penalty → `-0.1 * steps`

👉 Rewards are continuous (0.0 → 1.0)

---

## 📦 Project Structure
