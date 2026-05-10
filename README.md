# AI Assistant API

A production-ready AI chat backend built with FastAPI and Groq, featuring tool calling, per-session memory, and session expiry.

**Live API:** `https://ai-api-assistant-production.up.railway.app`  
**Docs:** `https://ai-api-assistant-production.up.railway.app/docs`

---

## Features

- Multi-turn conversation with full message history
- Per-session memory with UUID session IDs
- Auto session expiry after 30 minutes of inactivity
- Tool calling — calculator, weather, and web search
- Configurable system prompts per session
- Deployed on Railway

---

## Tech Stack

- Python + FastAPI
- Groq API (llama-3.1-8b-instant / llama-3.3-70b-versatile)
- DuckDuckGo Search
- Railway (deployment)

---

## Project Structure

```
ai-assistant-api/
├── main.py              # FastAPI app and all routes
├── tools.py             # Tool functions (calculate, weather, search)
├── tool_definitions.py  # Tool JSON schemas for the AI
├── session_manager.py   # Session storage and cleanup
├── requirements.txt     # Dependencies
└── README.md
```

---

## API Endpoints

### `GET /session`
Creates a new session and returns a unique session ID.

**Response:**
```json
{
  "session_id": "f3d594b6-6b26-4213-92d5-cc8ae61ca6f7"
}
```

---

### `POST /system`
Sets a system prompt for a session (persona, behavior, constraints).

**Request:**
```json
{
  "session_id": "your-session-id",
  "prompt": "You are a Python tutor who never gives full code answers."
}
```

**Response:**
```json
{
  "status": "system prompt set"
}
```

---

### `POST /chat`
Sends a message and gets a response. AI automatically uses tools when needed.

**Request:**
```json
{
  "session_id": "your-session-id",
  "message": "What is 234 multiplied by 567?"
}
```

**Response:**
```json
{
  "response": "The result of 234 multiplied by 567 is 132,678."
}
```

---

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

---

## Available Tools

The AI automatically decides when to use these tools:

| Tool | Trigger | Example |
|------|---------|---------|
| Calculator | Math questions | "What is 3045 × 5678?" |
| Weather | Weather questions | "What's the weather in Mumbai?" |
| Web Search | Current events / unknown info | "Latest AI news in 2026?" |

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/Pratham-K-890/ai-api-assistant
cd ai-api-assistant

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_key_here > .env

# Run the server
uvicorn main:app --reload
```

---

## Example Flow

```bash
# 1. Create a session
curl -X GET https://ai-api-assistant-production.up.railway.app/session

# 2. Set a system prompt
curl -X POST https://ai-api-assistant-production.up.railway.app/system \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-id", "prompt": "You are a helpful assistant."}'

# 3. Chat
curl -X POST https://ai-api-assistant-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-id", "message": "What is the weather in Bangalore?"}'
```

---

## Built By

Pratham — Week 1, Phase 2 of AI Development curriculum.
