from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from controllers import routes
from database.connection import engine
from database import models

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    response = RedirectResponse('/docs')
    return response

app.include_router(routes.router)