import time
import uuid
from typing import List

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Replace with your assigned origin
ALLOWED_ORIGIN = "https://dash-jcy61u.example.com"

# Replace with YOUR logged-in email
EMAIL = "24f3000591@ds.study.iitm.ac.in"

# Strict CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response


app.add_middleware(RequestMiddleware)


@app.get("/stats")
async def stats(values: str = Query(...)):
    nums: List[int] = [int(x.strip()) for x in values.split(",") if x.strip()]

    count = len(nums)
    total = sum(nums)

    return {
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / count,
    }
