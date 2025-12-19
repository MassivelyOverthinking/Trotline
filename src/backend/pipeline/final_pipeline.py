# ----------------------------------------
# IMPORTS
# ----------------------------------------

import pandas as pd

from typing import Dict, Any

from src.backend.pipeline.helper_methods import retrieve_remaining_data
from src.backend.pipeline.character_methods import retrieve_character_based_data
from src.backend.pipeline.whois_methods import retrieve_extracted_url_data
from src.backend.pipeline.parsing_methods import final_url_parser

# ----------------------------------------
# FINAL PIPELINE METHODS
# ----------------------------------------

# Pipeline method for Website Application
def finalised_data_pipeline_for_web(url: str) -> pd.Series:
  # Validation check for URL-parameter
  if not isinstance(url, str):
    raise ValueError(f"URL must be of Type: str - Current type {type(url)}")

  # Retrieve the URL-related data -> Convert to Dict-objects.
  parsed_url_data = final_url_parser(url=url)
  extracted_url_data = retrieve_extracted_url_data(url=url)
  character_based_data = retrieve_character_based_data(url=url)
  remaining_data = retrieve_remaining_data(url=url)

  # Concat Dict-objects into single instance.
  results = parsed_url_data | extracted_url_data | character_based_data | remaining_data

  # 'Url' key-value pair is no longer needed -> Delete the pair.
  try:
    del results["url"]
  except KeyError as kerr:
    raise kerr

  # Convert Booleans to binary.
  for key, value in results.items():
    if isinstance(value, bool):
      results[key] = int(value)

  # Convert to pd.Series-object and return the final data.
  return pd.Series(results)


# Pipeline method for PyPi.org Package.
def finalised_data_pipeline_for_py(url: str) -> Dict[str, Any]:
  # Validation check for URL-parameter
  if not isinstance(url, str):
    raise ValueError(f"URL must be of Type: str - Current type {type(url)}")

  # Retrieve the URL-related data -> Convert to Dict-objects.
  parsed_url_data = final_url_parser(url=url)
  extracted_url_data = retrieve_extracted_url_data(url=url)
  character_based_data = retrieve_character_based_data(url=url)
  remaining_data = retrieve_remaining_data(url=url)

  # Concat Dict-objects into single instance.
  results = parsed_url_data | extracted_url_data | character_based_data | remaining_data

  # Convert Booleans to binary.
  for key, value in results.items():
    if isinstance(value, bool):
      results[key] = int(value)

  # Return a Python-Dict object.
  return results