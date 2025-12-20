# ----------------------------------------
# IMPORTS
# ----------------------------------------

import tldextract as tld
import whois
import datetime

from tldextract import ExtractResult
from datetime import timezone
from typing import Optional, Union, Dict
from whois.exceptions import WhoisError, WhoisCommandFailedError, WhoisDomainNotFoundError

from src.backend.pipeline.helper_methods import extract_hostname, is_domain_typosquatted
from src.backend.pipeline.dataset import typosquatted_domains_set

# ----------------------------------------
# PIPELINE WHOIS METHODS
# ----------------------------------------

# Extract the necessary WHOIS documentation regarding the specified URL domain.
# Currently returns the days since Registration & days until Expiration.
def get_whois_info(text: ExtractResult):

  # Retrieve the full URL from ExtractResult.
  text = f"{text.subdomain}.{text.domain}.{text.suffix}"

  try:
    text.encode("idna")                                               # Attempt to encode = IDNA.

    whois_information_dict = whois.whois(text, timeout=1)             # Extract WHOIS information.

    current_time = datetime.now(timezone.utc)

    registration_date = whois_information_dict.get("creation_date")   # Get registration date
    expiration_date = whois_information_dict.get("expiration_date")   # Get expiration date

    if isinstance(registration_date, list):                           # Check if dates are list-objects
      registration_date = registration_date[0]
    if isinstance(expiration_date, list):
      expiration_date = expiration_date[0]

    days_since_whois_regis = (current_time - registration_date).days if registration_date else 0
    days_until_whois_expir = (expiration_date - current_time).days if expiration_date else 0

    return days_since_whois_regis, days_until_whois_expir
  except (WhoisCommandFailedError, WhoisDomainNotFoundError, WhoisError, UnicodeError, ConnectionResetError):
    return None, None
  
# Wrapper method for extracting, processing and formulating WHOIS Data correctly.
# Returns a Python Dict.
def retrieve_extracted_url_data(url: str) -> Dict[str, Optional[Union[float, int]]]:
  # Parse the URL to retreive critical information.
  extracted_url = extract_hostname(url=url)

  # Retrieve WHOIS information.
  reg_date, exp_date = get_whois_info(text=extracted_url)

  # Gather all information into Results-dict
  results = {
      "is_typosquatted": is_domain_typosquatted(
          hostname=extracted_url,
          domains=typosquatted_domains_set,
          threshold=2
      ),
      "whois_valid": bool(reg_date and exp_date),
      "days_since_whois_reg": reg_date,
      "days_until_whois_exp": exp_date,
  }

  return results
