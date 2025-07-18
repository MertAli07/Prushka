from langchain_ollama import ChatOllama

# returns a llm object based on the model name
def choose_llm(provider_name, model_name, **kwargs):
    if provider_name == "ollama":
        if model_name == "gemma3_1b":
            return ChatOllama(model="gemma3:1b", **kwargs)
        else:
            raise ValueError(f"Unsupported model: {model_name}")
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")
