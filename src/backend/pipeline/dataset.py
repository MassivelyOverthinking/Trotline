# ----------------------------------------
# DATASET LISTS
# ----------------------------------------

# Set of domain extensions that are commonly utilised in Phishing scams.
suspicious_domain_extensions_set = {
    ".xyz", ".top", ".club", ".shop", ".online", ".site", ".biz", ".info",
    ".cc", ".tk", ".ml", ".ga", ".ru", ".cf", ".gq", ".pw", ".cn", ".br", ".me",
    ".so", ".vg", ".to", ".hk", ".click", ".link", ".download", ".work",
    ".support", ".live", ".loan", ".men", ".review", ".stream", ".party",
    ".science", ".accountant", ".faith", ".date", ".racing", ".win", ".vip", ".bid",
    ".cam", ".kim", ".mom", ".loan", ".press", ".rest", ".space", ".trade", ".gratis",
    ".casino", ".bet", ".poker", ".su", ".la", ".pm", ".sh", ".krd", ".ltd", ".guru",
    ".free", ".asia"
}

# Set of suspicious keywords that are commonly utilised in Phishing scams.
suspicious_keywords_set = {
    "secure", "security", "verify", "verification", "auth", "authenticate", "login",
    "account", "update", "credentials", "reauth", "confirm", "confirmation", "identity",
    "id", "validate", "validation", "password", "reset", "signin", "sign-in", "signon",
    "sign-on", "access", "unlock", "unlock", "recovery", "support", "service", "invoice",
    "pay", "payment", "billing", "checkout", "order", "transaction", "refund", "bonus",
    "claim", "payout", "alert", "warning", "notice", "important", "urgent", "immediate",
    "suspended", "disabled", "locked", "compromised", "bank", "banking", "wallet",
    "crypto", "exchange", "finance", "download", "setup", "installer", "patch", "submit",
    "proceed", "restricted", "restriction", "failure", "failed", "error", "expired",
    "expiration", "attention", "critical", "mandatory", "reactivate", "reactivation",
}

# Set of domains that are commonly subjected to Typosquatting (Character change).
typosquatted_domains_set = {
    "paypal", "microsoft", "facebook", "verizon", "irs", "adobe", "amazon", "ebay",
    "apple", "wellsfargo", "instagram", "whatsapp", "coinbase", "netflix", "fedex",
    "linkedin", "reddit", "wikipedia", "bing", "naver", "yahoo", "temu", "spotify",
    "shopify", "yandex", "capitalone", "chase", "bankofamerica", "americanexpress",
    "klarna", "snapchat", "vidmate", "apkpure", "walmart", "target", "binance",
    "acesso", "experian", "creditkarma", "tbank", "hdfcbank", "caixa", "alfabank",
    "usbank", "santander", "venmo", "revolut", "westernunoin", "moneygram", "remitly",
    "cashapp", "zelle", "ofx", "telegram", "google", "twitter", "github", "gitlab",
    "dropbox", "onedrive", "outlook", "steam", "epicgames", "playstation", "nintendo",
    "uber", "lyft", "doordash", "airbnb", "booking", "hulu", "disneyplus", "primevideo",
    "paramountplus", "skype", "slack", "zoom", "salesforce", "workforce", "citibank",
    "barclays", "tmobile", "vodafone", "cloudflare", "aws", "azure",
}