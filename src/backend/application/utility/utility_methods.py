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
    model_json = model_bytes.decode('utf-8')

    xgb_model = xgb.Booster()
    final_model = xgb_model.load_model(model_json)

    return final_model



