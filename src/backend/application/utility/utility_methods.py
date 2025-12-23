# ----------------------------------------
# IMPORTS
# ----------------------------------------

import xgboost as xgb

from botocore.response import StreamingBody

# ----------------------------------------
# UTILITY & HELPER METHODS
# ----------------------------------------

def from_reponse_to_model(body: StreamingBody) -> xgb.Booster:
    """
    Extract the necessary binary data from S3 (AWS) client session, and build internal new XGboost
    inference model for URL-string predictions.

    Parameters
    ----------
    body : StreamingBody
        AWS client response.

    Returns
    -------
    xgboost.Booster
        XGBoost inference model for URL-string predictions.

    Exceptions
    ----------
    ModuleNotFoundError
        Raised if the StreamingBody element contains no binary data for XGBoost modeling. 
    """

    # Extract the data from the 'Body' element.
    model_body = body["Body"]
    model_bytes = model_body.read()

    # Raise appropriate error if no data was found.
    if not model_bytes:
        raise ModuleNotFoundError("XGBoost Model file not loaded correctly!")
    
    # Train & return the finalized inference model.
    xgb_model = xgb.Booster()
    xgb_model.load_model(bytearray(model_bytes))

    return xgb_model



