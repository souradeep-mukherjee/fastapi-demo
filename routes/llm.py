from fastapi import APIRouter, Query
import httpx

router = APIRouter()

@router.get("/ask-llm")
async def ask_llm(
    prompt: str = Query(..., description="Your question for the model"),
    model: str = "llama2"
):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=None
        )
        resp.raise_for_status()
        data = resp.json()
    return {"response": data["response"]}
