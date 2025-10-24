# Code with FastAPI (app = FastAPI(...))


from fastapi import FastAPI

# Other imports

app = FastAPI(title="...", description="...")


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=dict, status_code=201)
def predict(payload: dict) -> dict:
    # TODO: complete and replace with the correct Pydantic classes defined in web_service/lib/models.py
    # This is a placeholder until the colleague implements the API
    return {"message": "API not yet implemented", "status": "placeholder"}
