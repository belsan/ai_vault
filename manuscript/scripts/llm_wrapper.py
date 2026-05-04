import time

import requests

OLLAMA_BASE_URL = "http://192.168.50.3:11700"
OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"
SHOW_URL = f"{OLLAMA_BASE_URL}/api/show"
TOKENIZE_URL = f"{OLLAMA_BASE_URL}/api/tokenize"


class LLMWrapper:
    def __init__(self, model):
        self.model = model

    def get_model(self):
        return self.model

    def get_available_models(self):
        raise NotImplementedError()

    def count_tokens(self, prompt: str) -> int:
        raise NotImplementedError()

    def get_context_length(self, model=None):
        raise NotImplementedError()

    def ask(self, prompt) -> str:
        raise NotImplementedError()


class MockLLM(LLMWrapper):
    def __init__(self, model):
        super().__init__(model)
        self.answer = ""

    def get_available_models(self):
        return ["mock_model"]

    def count_tokens(self, prompt: str) -> int:
        return 0

    def get_context_length(self, model=None):
        return 10000

    def ask(self, prompt) -> str:
        return self.answer


class OLLAMAWrapper(LLMWrapper):
    def __init__(self, model, wait_time=0):
        super().__init__(model)
        self.wait_time = wait_time

    def get_available_models(self):
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                for model in models:
                    response = requests.post(f"{OLLAMA_BASE_URL}/api/show", json={"name": model["name"]})
                    if response.status_code == 200:
                        model_info = response.json()
                        print(model["name"], model_info["model_info"]["general.parameter_count"], end="")
                        try:
                            print(model_info["model_info"]["general.size_label"])
                        except KeyError:
                            print("")
                    # print(model["name"],f"{model["size"]/1e9:.0f}")
                return [model["name"] for model in models]
                # print("Installed Models:")
                # for model in models:
                #    print(f"- {model['name']}")
            else:
                raise ValueError("No models installed.")
        else:
            print(f"Error fetching models: {response.status_code}, {response.text}")
            raise ValueError(f"Error fetching models: {response.status_code}, {response.text}")

    def count_tokens(self, prompt) -> int:
        payload = {"model": self.model, "prompt": prompt}
        response = requests.post(TOKENIZE_URL, json=payload)

        if response.status_code == 200:
            return len(response.json().get("tokens", []))

        raise RuntimeError("Failed to get token count from Ollama")

    def get_context_length(self, model=None):
        if model is None:
            model = self.model

        payload = {"name": model}
        response = requests.post(SHOW_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            print(data)
            return data.get("details", {}).get("context_length", None)  # Get the context length if available

        raise RuntimeError(f"Failed to fetch model info: {response.text}")

    def ask(self, prompt) -> str:
        payload = {
            "model": self.model,  # Change this to your installed model, e.g., "mistral" or "gemma"
            "prompt": prompt,
            "stream": False,
        }
        if self.wait_time > 0:
            time.sleep(self.wait_time)

        # print(f"Sending question... length: {len(payload['prompt'])}")
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response found.")

        raise ValueError(f"Some Problem with the LLM - Status {response.status_code}")  # should not be value error


if __name__ == "__main__":
    llm = OLLAMAWrapper("gemma3:4b")

    models = llm.get_available_models()
    print(f"OLLAMA at {OLLAMA_BASE_URL} is serving {len(models)} models:")
    for model in models:
        print(f"   {model}")

    llm.model = models[0]
    print(f"Using model {llm.model}")

    t0 = time.time()
    for _ in range(1):
        prompt = "This is just a test. Say Cheese!"
        print(llm.ask(prompt))

    print(f"Took {time.time() - t0:.1f}s")
