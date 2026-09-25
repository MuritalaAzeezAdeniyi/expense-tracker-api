from typing import Any

from fastapi import FastAPI

from app.routes.auth import router as auth_router


app = FastAPI(
    title="Expense Tracker API",
    description="An AI-native expense tracking API",
    version="1.0.0",
)

app.state.users: dict[str, dict[str, Any]] = {}
app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}