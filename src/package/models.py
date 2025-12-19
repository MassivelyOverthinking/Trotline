# ----------------------------------------
# IMPORTS
# ----------------------------------------

import json

# ----------------------------------------
# PYPI MODELS
# ----------------------------------------

class TrotResult:

    __slots__ = ("data", "url", "status")

    def __init__(self, data):
        self.data: dict = json.loads(data)
        self.url = self.data["url"]
        self.status = self.data["status"]