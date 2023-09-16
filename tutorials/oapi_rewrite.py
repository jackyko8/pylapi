@oAPI.resource_class(resource_name="conversation")
class Conversation(oAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.message_bank = []

    @oAPI.resource_method(method_path="chat/completions", http_method="POST", load="$")
    def ask(self, question: str):

        @oAPI.callback
        def request(self, role="user", model="gpt-3.5-turbo", **kwargs):
            self.message_bank.append({
                "role": role,
                "content": kwargs["question"],
            })
            self.raw_request["json"] = {
                "model": model,
                "messages": self.message_bank,
                "temperature": 0.7
            }
            self.raw_request["params"] = {}

        @oAPI.callback
        def response(self, **kwargs):
            if self.response_ok() and "choices" in self.response_data:
                choices = self.response_data["choices"]
                self.message_bank.append(choices[0]["message"])
                answers = [_["message"]["content"] for _ in choices]
                self.response_data.update({
                    "answers": answers,
                })
