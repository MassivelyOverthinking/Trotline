# ----------------------------------------
# IMPORTS
# ----------------------------------------

import pandas as pd

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from typing import Optional, Union

from src.backend.pipeline.final_pipeline import finalised_data_pipeline
from src.backend.application.main import app

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
async def retrieve_url_status(url_string: str):
    if not isinstance(url_string, str):
        raise HTTPException(
            status_code=415,
            detail="Invalid data type - URL data must be of Type: str"
        )
    
    # Convert the URL-String using 'Finalized_data_pipeline'.
    url_data = finalised_data_pipeline(url=url_string)
    # Check if the data was converted correctly.
    if not isinstance(url_data, pd.Series):
        raise HTTPException(
            status_code=422,
            detail="Corrupted data - URL data was processed incorrectly"
        )
    
    prediction = app.state.model.predict(url_data)