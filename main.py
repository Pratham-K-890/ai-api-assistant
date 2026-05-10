from tools import calculate, get_weather, search
from tool_definitions import calculator_tool, weather_tool, search_tool
from session_manager import sessions, lifespan
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from datetime import datetime
import uuid
import json
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(lifespan=lifespan)
client=Groq()




class ChatRequest(BaseModel):
    message:str
    session_id:str

class SystemRequest(BaseModel):
    prompt:str
    session_id:str

@app.get("/session")
def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"messages": [],
                          "last_active": datetime.now()}
    return {"session_id": session_id}

@app.post("/system")
def system(request:SystemRequest):
    session = sessions.get(request.session_id)
    if session is None:
      return {"error": "session not found"}
    messages=session["messages"]
    messages.append({"role":"system","content":request.prompt})
    session["last_active"]=datetime.now()
    return {"status": "system prompt set"}

@app.post("/chat")
def chat(request: ChatRequest):
    # 1. Session lookup — FIRST
    session = sessions.get(request.session_id)
    if session is None:
        return {"error": "session not found"}
    messages = session["messages"]
    
    # 2. Append user message
    messages.append({"role": "user", "content": request.message})
    
    # 3. First API call with all tools
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=1024,
        tools=[calculator_tool, weather_tool, search_tool]
    )
    
    # 4. Did AI want a tool?
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        
        # Which tool?
        if tool_call.function.name == "calculator":
            result = calculate(args["a"], args["b"], args["operation"])
        elif tool_call.function.name == "weather":
            result = get_weather(args["city"])
        elif tool_call.function.name == "search":
            result = search(args["query"])
        
        # Append tool result
        messages.append(response.choices[0].message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })
        
        # Second API call
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024
        )
        messages.append({"role": "assistant", "content": final_response.choices[0].message.content})
        session["last_active"] = datetime.now()
        return {"response": final_response.choices[0].message.content}
    
    # 5. No tool — direct response
    else:
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        session["last_active"] = datetime.now()
        return {"response": response.choices[0].message.content}


@app.get("/health")
def healthCheck():
    return {"status":"ok"}