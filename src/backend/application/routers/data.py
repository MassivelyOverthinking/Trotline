# ----------------------------------------
# IMPORTS
# ----------------------------------------

import pandas as pd
import redis as rds
import xgboost as xgb

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from botocore.client import BaseClient

from src.backend.pipeline.final_pipeline import finalised_data_pipeline

# ----------------------------------------
# FASTAPI DATA ENDPOINTS
# ----------------------------------------

# Setup Data-related APIrouter -> Handles sent URLs.
router = APIRouter(
    prefix="/data",
    tags=["data", "phishing"],
    responses={404: {"description": "Not found!"}}
)

@router.put(
    "/{url_string}",
    tags=["data", "url", "phishing"],
    responses={404: {"Description": "Operation not found!"}}
)
async def retrieve_url_status(url_string: str, request: Request):
    # Safety check for URL-string param -> must be of Type: str
    if not isinstance(url_string, str):
        raise HTTPException(
            status_code=415,
            detail="Invalid data type - URL data must be of Type: str"
        )

    # Retrieve the DB, Cache and Model connections from internal FastAPI.
    s3_db:      BaseClient = request.app.state.s3
    rds_cache:  rds.Redis = request.app.state.cache
    xgb_model:  xgb.Booster = request.app.state.model

    # 1. Step -> Check Redis Cache for stored key-value pair.
    cached_url_data = rds_cache.get(name=url_string)
    if cached_url_data is not None:
        return cached_url_data["status"]
    
    # 2. Step -> Convert the URL-String using 'Finalized_data_pipeline'.
    url_data: pd.Series = finalised_data_pipeline(url=url_string)
    # Check if the data was converted correctly.
    if not isinstance(url_data, pd.Series):
        raise HTTPException(
            status_code=422,
            detail="Corrupted data - URL data was processed incorrectly"
        )
    
    # 3. Step -> Make URL prediction using XGBoost model.
    prediction = xgb_model.predict(url_data)

    results = {
        "url": url_string,
        "status": prediction 
    }

    rds_cache.set(
        name=url_string,
        value=prediction
    )

    return results
