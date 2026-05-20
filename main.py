
from finance.models.ollama import *
from finance.utils.progress import *
from finance.utils.data import *


def main():
    print("Ollama base URL:", get_ollama_base_url())
    print("Available Ollama models:", list_available_ollama_models())
    model = get_ollama_model("qwen3:8b")
    print("Got Ollama model instance:", model)

    #ret = model.invoke("What is the stock price of Apple Inc. (AAPL) today?")
    #print("Model response:", ret)

    #inspect_object(model)
    #live_table()
    ret = get_finance_metrics("AAPL", "2026-05-20")
    inspect_object(ret)


if __name__ == "__main__":
    main()

