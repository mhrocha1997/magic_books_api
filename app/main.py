from fastapi import FastAPI
from controllers import routes
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(routes.router)