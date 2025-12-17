# ----------------------------------------
# IMPORTS
# ----------------------------------------

from fastapi import FastAPI

from routers import data

# ----------------------------------------
# FASTAPI APPLICATION SETUP
# ----------------------------------------

app = FastAPI()

app.include_router(data.router)

@app.get("/")
async def root():
    return {"Root Webpage": "Welcome to Trotline"}