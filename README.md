# Multi‑Agent AI Assistant (Flask · LangGraph · React)

A production‑oriented, tool‑using **multi‑agent** system with a **LangGraph supervisor** orchestrating domain agents (Math · Weather · Space Launches · Todoist · Poem). Real‑time **SSE streaming** to a **React + Tailwind** chat UI with an Agent‑Flow panel for step tracing.

> ⚑ This codebase consolidates earlier experiments into one stable repo. (Previous iterations lived in smaller repos; this is the unified, cleaned‑up version.)

---

## project highligter:

* **Clear orchestration**: A LangGraph **supervisor graph** routes user requests to the right agent and tools, then aggregates results into a final answer.
* **Deterministic tool‑use**: Agents call **typed tools** (Pydantic/LC Tools) for weather, launches, and Todoist—showing practical API integration patterns.
* **Frontend you can feel**: React chat panel streams tokens/steps via **Server‑Sent Events**, with a right‑side **Agent Flow** timeline to visualize reasoning hops.
* **Resume‑friendly code**: Separation of concerns (agents/tools/models/config/frontend) with environment‑driven keys and CORS‑safe local dev.

---

## Architecture

```
User ↔ React (Vite + Tailwind + Framer Motion)
           │  POST /prompt  (SSE stream back)
           ▼
     Flask API  ──────────────────────────────────────────────────────────────
        │                   │                      │                 │
        ▼                   ▼                      ▼                 ▼
  LangGraph Supervisor  →  Math Agent         Weather Agent     Launch Agent
        │                   │ tools:add/mul     tool:get_weather  tool:get_launches
        │                   │                   (OpenWeather)     (The Space Devs)
        ▼                   
   Todoist Agent (tool:add_task / get_task)
        │
        ▼
   LLM via Groq (Llama‑3.3‑70B "versatile")
```

* **Supervisor**: LangGraph state graph that dispatches to agents and merges their replies.
* **Agents** (LangChain + LangGraph prebuilt ReAct agents):

  * `math_agent` → tools: `add`, `multiply`, `divide`
  * `weather_agent` → OpenWeatherMap API (`get_weather`)
  * `launch_vehicle_agent` → Launch Library 2 API (`get_launches` via The Space Devs)
  * `todolist_agent` → Todoist API (`add_task`, `get_task`)
  * `poem_agent` → LLM‑only creative generation
* **LLM provider**: `langchain_groq.ChatGroq` using **Llama‑3.3‑70B‑versatile**
* **Streaming**: Flask yields `text/event-stream` chunks → React reads via `ReadableStream` and updates chat + step timeline.

---

## Key Tech & APIs

**Backend**

* **Flask**, **Flask‑CORS**
* **LangGraph**, **LangChain**, **langchain\_groq**
* **Pydantic** typed tool I/O
* **Requests** for external APIs

**External APIs**

* **OpenWeatherMap** (current weather)
* **Todoist** (add/read tasks)
* **The Space Devs – Launch Library 2** (upcoming launches)

**Frontend**

* **React 19**, **Vite**, **Tailwind CSS**, **Framer Motion**, **react‑icons**

---

## Getting Started (Local Dev)

### 1) Backend

```bash
# Python 3.11+
python -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors langchain langgraph langchain-groq pydantic requests python-dotenv todoist-api-python

# set environment
cp .env.example .env   # or create .env by hand (see below)
python app.py          # runs on http://127.0.0.1:5050
```

**`.env`** (required)

```
GROQ_API_KEY=sk_...
OPENWEATHER_API_KEY=...
TODOIST_API_KEY=...
```

### 2) Frontend

```bash
cd frontend
npm i
npm run dev  # http://localhost:5173
```

> CORS is already enabled for local dev (Flask‑CORS). The chat panel posts to `http://localhost:5050/prompt` and streams back.

---

## API (Backend)

### `POST /prompt`

* **Body**: `{ "prompt": "string" }`
* **Response**: `text/event-stream` with JSON chunks
* **Contract**: each chunk includes either a partial `response` or a `step` entry; the last event sets `done: true`.

Example (pseudo):

```json
{
  "response": { "todolist_agent": {"content": "Added task: drink"} },
  "step": [{"type":"todoist_agent","content":"add_task -> OK"}],
  "done": false
}
```

---

## What to look at in code (quick tour)

* **`app.py`**: SSE generator and LangGraph supervisor wiring
* **`agents/*.py`**: per‑domain prompts + tool registration via `create_react_agent`
* **`tools/*.py`**: real http calls with schema‑validated outputs
* **`models/llm.py`**: single place to swap LLM/provider
* **Frontend `ChatPanel.jsx`**: streaming reader (ReadableStream → UI)
* **Frontend `AgentFlow.jsx`**: simple, recruiter‑friendly step timeline

---

## Notes on reliability & security

* **Secrets** via `.env` (never in code); production should use a secrets manager.
* **Rate‑limits / retries**: external APIs wrapped in `try/except` with error payloads; could extend with backoff.
* **Input safety**: tools validate outputs with Pydantic; consider server‑side content filters per domain.
* **CORS**: narrowly scoped to local dev origins (adjust in production).

---

## Roadmap

* Agent memory (vector DB) for follow‑ups
* Tracing/observability (LangSmith / OpenTelemetry)
* OAuth flow for Todoist instead of token
* Optional FastAPI migration for richer OpenAPI docs
* Dockerfiles for both services + compose

---

## Attribution

* Weather: OpenWeatherMap
* Launches: The Space Devs · Launch Library 2
* LLM serving: Groq (Llama‑3.3‑70B “versatile”)


