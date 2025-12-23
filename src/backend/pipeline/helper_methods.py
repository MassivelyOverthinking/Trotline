# ----------------------------------------
# IMPORTS
# ----------------------------------------

import tldextract as tld
import math

from typing import Optional, Union, Dict
from tldextract import ExtractResult
from pyxdameraulevenshtein import damerau_levenshtein_distance as pdl_distance

from src.backend.pipeline.dataset import suspicious_keywords_set

# ----------------------------------------
# PIPELINE HELPER METHODS
# ----------------------------------------

# Check the number of subdomains contained within the main URL domain.
# As subdomains are commonly separated by period symbols - The method check for their presence.
def num_of_subdomains(hostname: str) -> int:
  """
  Check the number of distinct subdomains present in the hostname by dividing into lesser domain 
  instaces using - Utility method in Trotline finalised Data Pipeline.
  
  Parameters
  ----------
  hostname : str
    String representation of URL hostname.

  Returns
  -------
  int
    Number of unique subdomains present in specified hostname. 
  """
  return hostname.count(".") - 1

# Extract the hostname from the specified URL -> tldextract-package.
# Helper method for extracting the unabridged hostname.
def extract_hostname(url: str) -> ExtractResult:
  """
  Method for extracting domain-related information - fx. hostname, extensions, path etc. - from 
  specified URL-string - Utility method in Trotline finalised Data Pipeline.

  Parameters
  ----------
  url : str
    URL-string to extract domain instance from.

  Returns
  -------
  tldextract.ExtractResult
    Custom data-class for storing the extracted URL information.
  """
  return tld.extract(url)

# Check if the specified domain is Typosquatted using Damerau-Levenshtein Distance
# If the domain if off by 1 - 2 character changes -> Return True.
def is_domain_typosquatted(hostname: ExtractResult, domains: list[str], threshold: int) -> bool:
  host_domain = hostname.domain
  for domain in domains:
    distance = pdl_distance(host_domain, domain)   # Calculate the DL-distance.
    if distance != 0 and distance <= threshold:   # Check if distance if below threshold & not 0.
      return True

  return False

# Check if the specified domain ends with an exention
# that is commonly utilized in Typosquatting attacks
def contains_suspicious_domain_extension(domain: str, extensions: list[str]) -> bool:
  for extension in extensions:
    if domain.endswith(extension):
      return True

  return False

# Check if the specified domain includes one or more suspicious keywords
# commonly associated with Phishing attacks.
def contains_suspicious_keyword(text: str, keywords: list[str]) -> bool:
  for keyword in keywords:
    if keyword in text:
      return True
  return False

# Calculate the Shannon Entropy (Degree of Unpredictability) for the specified domain.
def calculate_shannon_entropy(text: str) -> float:

   probabilities = [float(text.count(char)) / len(text) for char in list(text)]
   entropy = -sum([p * math.log2(p) for p in probabilities])

   return entropy

# Finalised Wrapper-method for determining Shannon Entropy + Suspicious Keywords.
# Returns a Python Dict-object.
def retrieve_remaining_data(url: str) -> Dict[str, Union[float, int]]:
  # Gather all information into Results-dict
  results = {
      "domain_entropy": calculate_shannon_entropy(text=url),
      "contains_sus_keyword": contains_suspicious_keyword(
          text=url,
          keywords=suspicious_keywords_set
      )
  }

  return results