from fastapi import FastAPI

app = FastAPI(
    title="Expense Tracker API",
    description="An AI-native expense tracking API",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}