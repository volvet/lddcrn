import requests
import time
import os


def _make_api_request(url: str, headers: dict | None = None, method="GET", jaon_data: dict | None = None, max_retries: int = 3) -> requests.Response:
    """Make an HTTP request with retries."""
    for attempt in range(max_retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=5)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=jaon_data, timeout=5)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response
        except (requests.RequestException, ValueError) as e:
            if attempt < max_retries - 1:
                if response.status_code == 429:  # Too Many Requests
                    delay = 60 + (30 * attempt)
                    print(f"Rate limited (429). Attempt {attempt + 1}/{max_retries + 1}. Waiting {delay}s before retrying...")
                    time.sleep(delay)
                continue
            else:
                raise e


def get_finance_metrics(ticker: str, end_date: str, period="ttm", limit=10):
    headers = {}
    financial_api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
    if financial_api_key:
        headers["X-API-KEY"] = financial_api_key

    url = f"https://api.financialdatasets.ai/financial-metrics/?ticker={ticker}&report_period_lte={end_date}&limit={limit}&period={period}"
    response = _make_api_request(url, headers)
    if response.status_code != 200:
        return []
    return response.json()