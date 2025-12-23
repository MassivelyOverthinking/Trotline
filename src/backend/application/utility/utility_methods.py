# ----------------------------------------
# IMPORTS
# ----------------------------------------

import xgboost as xgb

from botocore.response import StreamingBody

# ----------------------------------------
# UTILITY & HELPER METHODS
# ----------------------------------------

def from_reponse_to_model(body: StreamingBody) -> xgb.Booster:
    model_body = body["Body"]
    model_bytes = model_body.read()

    if not model_bytes:
        raise ModuleNotFoundError("XGBoost Model file not loaded correctly!")
    
    xgb_model = xgb.Booster()
    xgb_model.load_model(bytearray(model_bytes))

    return xgb_model



