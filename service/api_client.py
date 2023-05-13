import openai


class ApiClient:
    def __init__(self, apiKey) -> None:
        self.apiKey = apiKey
        self.messages = list()

    def complete(self, message, system_setting, model, max_tokens=1000, temperature=0.7):
        try:
            openai.api_key = self.apiKey

            self.build_query(message, system_setting=system_setting)

            response = openai.ChatCompletion.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=self.messages
            )

            response = response['choices'][0]['message']['content'].strip()
            self.add_response(response)

            return response
        except Exception as e:
            error_message = str(e)
            if "key" in error_message.lower():
                return "Invalid API key! Please check your credentials and try again."
            elif "connect" in error_message.lower():
                return "Failed to connect to OpenAI's servers. Please check your internet connection and try again." + error_message
            else:
                return error_message

    def build_query(self, message, system_setting="you are a helpful assistant"):
        if not self.messages:
            self.messages.append(
                {
                    "role": "system",
                    "content": system_setting
                }
            )

            self.messages.append(
                {
                    "role": "user",
                    "content": message
                }
            )
        else:
            self.messages.append(
                {
                    "role": "user",
                    "content": message
                }
            )

    def add_response(self, response):
        self.messages.append(
            {"role": "assistant", "content": response}
        )

