import openai


class ApiClient():
    def __init__(self, apiKey) -> None:
        self.apiKey = apiKey

    def complete(self, messages, model, max_tokens=1000, temperature=0.7):
        try:
            openai.api_key =self.apiKey

            response = openai.ChatCompletion.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages = messages
            )

            return response['choices'][0]['message']['content'].strip()

        except Exception as e:
            error_message = str(e)
            if "key" in error_message.lower():
                return "Invalid API key! Please check your credentials and try again."
            elif "connect" in error_message.lower():
                return "Failed to connect to OpenAI's servers. Please check your internet connection and try again." + error_message
            else:
                return error_message
