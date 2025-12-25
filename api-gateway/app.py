from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI(title="API Gateway")

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8001")

@app.post("/orders")
async def create_order(request: Request):
    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{ORDER_SERVICE_URL}/orders", json=body)
            return JSONResponse(content=response.json(), status_code=response.status_code)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Order service unreachable: {exc}")
    except Exception as exc:
         raise HTTPException(status_code=500, detail=str(exc))

@app.get("/health")
async def health():
    return {"status": "ok"}
