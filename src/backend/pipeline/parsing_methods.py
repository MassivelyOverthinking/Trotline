# ----------------------------------------
# IMPORTS
# ----------------------------------------

from urllib.parse import ParseResult, urlparse
from typing import Optional, Union, Dict

from src.backend.pipeline.helper_methods import num_of_subdomains, contains_suspicious_domain_extension
from src.backend.pipeline.dataset import suspicious_domain_extensions_set

# ----------------------------------------
# PIPELINE URL-PARSING METHODS
# ----------------------------------------

# Method for parsing the specified URL and produce a default Dict-object if it fails.
def parse_url_and_handle_errors(url: str) -> Union[ParseResult, Dict[str, Optional[str]]]:
  # Parse the URL to retreive critical information.
  try:
    parsed_url = urlparse(url)

    return parsed_url
  except Exception:
    # If URL doesn't exist or is corrupted -> Return 'None' values in dict.
    return {
      "url": url,
      "length_hostname": None,
      "length_path": None,
      "length_query": None,
      "is_https": None,
      "nb_subdomains": None,
      "contains_sus_domain_ext": None,
    }

# Finalised Wrapper method for parsing, processing and formulating data related to the URL.
# Returns a Python Dict-object with relevant data. 
def final_url_parser(url: str):
  # Handle URL errors and retrieve information.
  parsed_url = parse_url_and_handle_errors(url=url)

  # If the return values are NOT ParseReuslt -> Return the Dict.
  if not isinstance(parsed_url, ParseResult):
    return parsed_url

  # Extract the internal values to create Results-dict.
  parsed_hostname = parsed_url.netloc
  parsed_path = parsed_url.path or ""
  parsed_query = parsed_url.query or ""

  return {
      "url": url,
      "length_hostname": len(parsed_hostname),
      "length_path": len(parsed_path),
      "length_query": len(parsed_query),
      "is_https": parsed_url.scheme.lower() == "https",
      "nb_subdomains": num_of_subdomains(hostname=parsed_hostname),
      "contains_sus_domain_ext": contains_suspicious_domain_extension(
          domain=parsed_hostname,
          extensions=suspicious_domain_extensions_set
      )
  }