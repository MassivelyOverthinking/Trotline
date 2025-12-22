# ----------------------------------------
# IMPORTS
# ----------------------------------------

import pandas as pd
import xgboost as xgb

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from src.backend.pipeline.final_pipeline import finalised_data_pipeline_for_web

# ----------------------------------------
# FASTAPI DATA ENDPOINTS -> WEB APP
# ----------------------------------------

# Setup Data-related APIrouter -> Handles sent URLs.
router = APIRouter(
    prefix="/data/web",
    tags=["data", "phishing"],
    responses={404: {"description": "Not found!"}}
)

@router.put(
    "/{url_string}",
    tags=["data", "url", "phishing"],
    responses={404: {"Description": "Operation not found!"}}
)
async def retrieve_url_status_web(url_string: str, request: Request):
    # Safety check for URL-string param -> must be of Type: str
    if not isinstance(url_string, str):
        raise HTTPException(
            status_code=415,
            detail="Invalid data type - URL data must be of Type: str"
        )

    # Retrieve the Model connection from internal FastAPI.
    xgb_model: xgb.Booster = request.app.state.model
    
    # 1. Step -> Convert the URL-String using 'Finalized_data_pipeline'.
    url_data: pd.Series = finalised_data_pipeline_for_web(url=url_string)
    # Check if the data was converted correctly.
    if not isinstance(url_data, pd.Series):
        raise HTTPException(
            status_code=422,
            detail="Corrupted data - URL data was processed incorrectly"
        )
    
    # 2. Step -> Make URL prediction using XGBoost model.
    prediction = xgb_model.predict(url_data)

    return {"url": url_string, "status": prediction}
