# ----------------------------------------
# IMPORTS
# ----------------------------------------

import boto3 as b3
import xgboost as xgb
import os

from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import contextmanager
from botocore.response import StreamingBody

from src.backend.application.routers import data_web
from src.backend.application.utility import from_reponse_to_model

# ----------------------------------------
# FASTAPI APPLICATION SETUP
# ----------------------------------------

# Load .env variables using dotenv
load_dotenv()

# Lifespan functions -> XGBoost model configured on 'Startup'.
@contextmanager
def lifespan(app: FastAPI):
    # Load S3 Database session (AWS) -> Add to app.state
    s3_client = b3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME")
    )

    # Load model data from session (AWS) S3.
    model_response: StreamingBody = s3_client.get_object(
        Bucket="arn:aws:s3:eu-north-1:212282292075:accesspoint/xgb-model",
        Key="XGBoost-model.ubj"
    )

    # Convert StreamingBody-object to finalised XGBoost model.
    xgb_model: xgb.Booster = from_reponse_to_model(model_response)

    # Load all session data into app.state configuration -> Lifespan.
    app.state.model = xgb_model
    app.state.s3 = s3_client

    yield       # Lifespan seperator

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
app.include_router(data_web.router)         # Route to Web-oriented API Endpoints. 

@app.get("/")
async def root():
    return {"Root Webpage": "Welcome to Trotline"}