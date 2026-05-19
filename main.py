
from finance.models.ollama import *
from finance.utils.progress import *


def main():
    print("Ollama base URL:", get_ollama_base_url())
    print("Available Ollama models:", list_available_ollama_models())
    model = get_ollama_model("qwen3:8b")
    print("Got Ollama model instance:", model)

    #ret = model.invoke("What is the stock price of Apple Inc. (AAPL) today?")
    #print("Model response:", ret)

    inspect_object(model)
    live_table()


if __name__ == "__main__":
    main()
