# ----------------------------------------
# IMPORTS
# ----------------------------------------

from collections import Counter
from typing import Dict, Union

# ----------------------------------------
# PIPELINE CHARACTER & DIGITS METHODS
# ----------------------------------------

# Count the apperance of special character instances in the specified URL.
def categorize_special_chars(text: str) -> Dict[str, int]:
  """
  Utilise Python native 'Counter' to count the instances of special chars & digits in the specified
  URL-string - Utility method in Trotline finalised Data Pipeline.
  
  Parameters
  ----------
  text : str
    URL-string to be parses & data extracted from.

  Returns
  -------
  Dict[str, int]
    Dictionary of special chars + digits and the number of individual occurences.
  """

  counter = Counter(text)

  return {
      "nb_www": text.count("www"),
      "special_chars": {
        "nb_dots": counter["."],
        "nb_hyphens": counter["-"],
        "nb_at": counter["@"],
        "nb_qm": counter["?"],
        "nb_and": counter["&"],
        "nb_or": counter["|"],
        "nb_eq": counter["="],
        "nb_underscore": counter["_"],
        "nb_tilde": counter["~"],
        "nb_percent": counter["%"],
        "nb_slash": counter["/"],
        "nb_star": counter["*"],
        "nb_colon": counter[":"],
        "nb_comma": counter[","],
        "nb_apostrophe": counter["'"],
        "nb_pound": counter["#"],
        "nb_semicolumn": counter[";"],
        "nb_dollar": counter["$"],
        "nb_space": counter[" "],
        "nb_digits": sum(counter[digit] for digit in "0123456789"),
      }
  }

# Finalized Wrapper method for extracting, processing and formulating Character-based data.
# Returns a Python Dict-object.
def retrieve_character_based_data(url: str) -> Dict[str, Union[float, int]]:
  """
  Wrapper method for extracting character-based numerical data from specified URL-string - 
  Utility method in Trotline finalised Data Pipeline.

  Parameters
  ----------
  url: str
    URL-string to be parses & data extracted from.

  Returns
  -------
  Dict[str, float | int]
    Dictionary format of extracted character-based data.
  """
  # Extract the necessary numerical data from URL
  url_length = len(url)

  # Extract character data from URL
  special_chars_data = categorize_special_chars(text=url)           # Char instances
  special_char_instances = special_chars_data.pop("special_chars")  # Inside values
  special_chars_num = sum(special_char_instances.values())          # Num of Chars

  # Extract digit data from URL
  digits_num = special_char_instances["nb_digits"]                  # Num of Digits

  # Calculate the ratios for Special Chars & Digits
  special_chars_data["url_length"] = url_length
  special_chars_data["special_chars_ratio"] = float(special_chars_num / url_length)
  special_chars_data["digits_ratio"] = float(digits_num / url_length)

  # Concatenate the 2 dicts into a single instance
  results = special_chars_data | special_char_instances

  return results