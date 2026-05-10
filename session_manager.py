import asyncio
from contextlib import asynccontextmanager
from datetime import datetime,timedelta
from fastapi import FastAPI


sessions={}    

async def cleanup_sessions():
    while True:
        await asyncio.sleep(60)  # check every 60 seconds
        now = datetime.now()
        expired = [
            sid for sid, session in sessions.items()
            if now - session["last_active"] > timedelta(minutes=30)
        ]
        for sid in expired:
            del sessions[sid]
        print(f"Cleaned up {len(expired)} sessions")

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(cleanup_sessions())
    yield