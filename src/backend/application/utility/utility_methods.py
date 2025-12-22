# ----------------------------------------
# IMPORTS
# ----------------------------------------

import tempfile
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
    
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        tmp.write(model_bytes)
        tmp.flush()
        xgb_model = xgb.Booster()
        xgb_model.load_model(tmp.name)

    return xgb_model



