# ----------------------------------------
# IMPORTS
# ----------------------------------------

import fastapi

from fastapi import APIRouter
from typing import Optional, Union

# ----------------------------------------
# FASTAPI DATA ENDPOINTS
# ----------------------------------------

router = APIRouter(
    prefix="/data",
    tags=["data", "phishing"],
    responses={404: {"description": "Not found!"}}
)

