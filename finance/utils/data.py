import requests
import time
import os
from pydantic import BaseModel
from typing import Optional


class FinancialMetrics(BaseModel):
    ticker: str
    report_period: str
    fiscal_period: str
    currency: str
    accession_number: str
    filing_url: str
    enterprise_value: float | None
    price_to_earnings_ratio: float | None
    price_to_book_ratio: float | None
    price_to_sales_ratio: float | None
    enterprise_value_to_ebitda_ratio: float | None
    enterprise_value_to_revenue_ratio: float | None
    free_cash_flow_yield: float | None
    peg_ratio: float | None
    gross_margin: float | None
    operating_margin: float | None
    net_margin: float | None
    return_on_equity: float | None
    return_on_assets: float | None
    return_on_invested_capital: float | None
    asset_turnover: float | None
    inventory_turnover: float | None
    receivables_turnover: float | None
    days_sales_outstanding: float | None
    operating_cycle: float | None
    working_capital_turnover: float | None
    current_ratio: float | None
    quick_ratio: float | None
    cash_ratio: float | None
    operating_cash_flow_ratio: float | None
    debt_to_equity: float | None
    debt_to_assets: float | None
    interest_coverage: float | None
    revenue_growth: float | None
    earnings_growth: float | None
    book_value_growth: float | None
    earnings_per_share_growth: float | None
    free_cash_flow_growth: float | None
    operating_income_growth: float | None
    ebitda_growth: float | None
    payout_ratio: float | None
    earnings_per_share: float | None
    book_value_per_share: float | None
    free_cash_flow_per_share: float | None

class FinancialMetricsResponse(BaseModel):
    financial_metrics: list[FinancialMetrics]

def _make_api_request(url: str, headers: Optional[dict] = None, method: str = "GET", json_data: Optional[dict] = None, max_retries: int = 3) -> requests.Response:
    """Make an HTTP request with retries."""
    for attempt in range(max_retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=5)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json_data, timeout=5)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                if hasattr(e.response, "status_code") and e.response.status_code == 429:  # Too Many Requests
                    delay = 60 + (30 * attempt)
                    print(f"Rate limited (429). Attempt {attempt + 1}/{max_retries}. Waiting {delay}s before retrying...")
                    time.sleep(delay)
                continue
            raise

def get_finance_metrics(ticker: str, end_date: str, period: str = "ttm", limit: int = 10):
    headers = {}
    financial_api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
    if financial_api_key:
        headers["X-API-KEY"] = financial_api_key

    url = f"https://api.financialdatasets.ai/financial-metrics/?ticker={ticker}&report_period_lte={end_date}&limit={limit}&period={period}"
    response = _make_api_request(url, headers)
    if response.status_code != 200:
        return []
    return FinancialMetricsResponse(**response.json())