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

# Load .env variables using dotenv
load_dotenv()

# Lifespan functions -> XGBoost model configured on 'Startup'.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load S3 Database session (AWS) -> Add to app.state
    s3_client = b3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME")
    )

    # Load Redis Caching session (AWS) -> Add to app.state
    rds_cache = rds.Redis(
        host="random-endpoint-aws",
        port=6379,
        decode_responses=True,
        ssl=True
    )

    model_response = s3_client.get_object(
        Bucket="xgb-model",
        Key="trotline-xgb-model.json"
    )

    # Load XGBoost model from JSON-file -> Add to app.state
    xgb_model = xgb.Booster().load_model(model_response)

    app.state.model = xgb_model
    app.state.cache = rds_cache
    app.state.s3 = s3_client

    yield       # Lifespan seperator

    # Close the Redis Caching session.
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