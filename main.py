
from finance.models.ollama import *
from finance.utils.progress import *
from finance.utils.data import *
import scipy.stats as stats
import numpy as np


def main():
    #print("Ollama base URL:", get_ollama_base_url())
    #print("Available Ollama models:", list_available_ollama_models())
    #model = get_ollama_model("qwen3:8b")
    #print("Got Ollama model instance:", model)

    #ret = model.invoke("What is the stock price of Apple Inc. (AAPL) today?")
    #print("Model response:", ret)

    #inspect_object(model)
    #live_table()
    #ret = get_finance_metrics("AAPL", "2026-05-20")
    #inspect_object(ret)
    df = read_data('AAPL', "2000-01-01", "2024-12-31", interval='1d')
    print(df.head())

    dta = df['ret'].values
    print('Stock index')
    print("Kurtosis: ", stats.kurtosis(dta))
    print('Skew:', stats.skew(dta))
    print('Mean:', np.mean(dta))
    print('Median:', np.median(dta))


if __name__ == "__main__":
    main()

