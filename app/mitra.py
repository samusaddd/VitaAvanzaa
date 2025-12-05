
from fastapi import APIRouter, Depends, HTTPException
from . import schemas
from .deps import get_current_user
from .config import get_settings

import httpx

router = APIRouter(prefix="/mitra", tags=["mitra"])

@router.post("/chat", response_model=schemas.MitraChatResponse)
async def mitra_chat(
    payload: schemas.MitraChatRequest,
    user=Depends(get_current_user),
):
    settings = get_settings()
    if not settings.OPENAI_API_KEY:
        # simple fallback – echo style – so frontend still works without key
        last_user_msg = ""
        for m in reversed(payload.messages):
            if m.role == "user":
                last_user_msg = m.content
                break
        reply = f"Mitra (dev mode): I received your message: '{last_user_msg}'. Once the OpenAI key is configured, I'll give you smarter replies."
        return schemas.MitraChatResponse(reply=reply)

    # Example using OpenAI Chat Completions HTTP API (no SDK needed)
    system_prompt = (
        "You are Mitra, the AI assistant of VitaAvanza. "
        "You help students, migrants, and young workers with finances, logistics, and wellbeing. "
        "Be concise, kind and practical."
    )

    messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m.role, "content": m.content} for m in payload.messages
    ]

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "gpt-4.1-mini",
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
        if resp.status_code >= 400:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {resp.text}")
        data = resp.json()
        reply_text = data["choices"][0]["message"]["content"]
        return schemas.MitraChatResponse(reply=reply_text)
