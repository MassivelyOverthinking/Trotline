# ----------------------------------------
# IMPORTS
# ----------------------------------------

from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import data

# ----------------------------------------
# FASTAPI APPLICATION SETUP
# ----------------------------------------

# Lifespan functions -> XGBoost model configured on 'Startup'.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

summary = """
Trotline is a phishing URL detection service built with FastAPI, 
powered by an XGBoost model. It analyzes URLs using a robust set of engineered numerical
features generated through a custom data pipeline to accurately identify
and classify phishing threats in real time.
"""

# Setup & configure the main FastAPI application.
app = FastAPI(
    title="Trotline",
    summary=summary,
    description="Swift Phishing URL Detector powered by XGBoost modeling",
    version="0.1.0",
    include_in_schema=True,
    lifespan=lifespan
)

# ----------------------------------------
# XGBOOST MODEL SETUP
# ----------------------------------------

# Internal XGBoost Model for predictions.
global xgb_model

# ----------------------------------------
# API ROUTE CONFIGURATION
# ----------------------------------------

# FastAPI Routes (Data).
app.include_router(data.router)

@app.get("/")
async def root():
    return {"Root Webpage": "Welcome to Trotline"}