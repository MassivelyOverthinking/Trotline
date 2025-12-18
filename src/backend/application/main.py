# ----------------------------------------
# IMPORTS
# ----------------------------------------

import xgboost as xgb
import boto3 as b3
import redis as rds
import os

from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from routers import data

# ----------------------------------------
# FASTAPI APPLICATION SETUP
# ----------------------------------------

load_dotenv()

# Lifespan functions -> XGBoost model configured on 'Startup'.
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = xgb.Booster().load_model("trotline_xgb_model.json")

    app.state.database = b3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME")
    )

    app.state.cache = rds.Redis(
        host="random-endpoint-aws",
        port=6379,
        decode_responses=True,
        ssl=True
    )

    yield
    
    app.state.cache.close()

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
# API ROUTE CONFIGURATION
# ----------------------------------------

# FastAPI Routes (Data).
app.include_router(data.router)

@app.get("/")
async def root():
    return {"Root Webpage": "Welcome to Trotline"}