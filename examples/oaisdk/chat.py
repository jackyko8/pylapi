import logging
from oaisdk import OaiSDK

@OaiSDK.resource_class("chat")
class ChatResource(OaiSDK):
    def __init__(self, *args, **kwargs):
        logger = OaiSDK.getLogger()
        logger.debug(f"ChatResource.__init__: args={args}; kwargs={kwargs}")
        super().__init__(*args, **kwargs)
        self._messages = []


    def instruct_model(self, instructions):
        self._messages.append({
            "role": "system",
            "content": instructions,
        })


    @OaiSDK.resource_method("chat/completions", "POST", load="$")
    def ask(self, question: str):
        logger = OaiSDK.getLogger()
        default_model = "gpt-3.5-turbo"
        logger.debug(f"ask: question={question}; default_mode={default_model}")

        @OaiSDK.callback
        def request(self, **kwargs):
            logger.debug(f">>>>>>>> request: kwargs={kwargs}")
            logger.debug(f">>>>>>>> request: from self.request={self.request}")
            model_id = kwargs["model"] if "model" in kwargs else default_model
            self._messages.append({
                "role": "user",
                "content": kwargs["question"],
            })
            self.raw_request["json"] = {
                "model": model_id,
                "messages": self._messages,
                "temperature": 0.7
            }
            self.raw_request["params"] = {}
            logger.debug(f">>>>>>>> request: to   self.request={self.request}")

        @OaiSDK.callback
        def response(self, **kwargs):
            logger.debug(f"<<<<<<<< response: kwargs={kwargs}")
            logger.debug(f"<<<<<<<< response: from self._response_data={self._response_data}")
            if not self.response_ok():
                logger.debug(f"<<<<<<<< response: not ok")
            elif "choices" not in self.response_data:
                logger.debug(f"<<<<<<<< response: no answers found")
            else:
                choices = self.response_data["choices"]
                # Keep the first choice in self._messages for context
                self._messages.append(choices[0]["message"])
                # Extract all answers
                answers = [_["message"]["content"] for _ in choices]
                self.response_data.update({
                    "answers": answers,
                })
                # logger.debug(f"<<<<<<<< response: self._messages={self._messages}")

    # @OaiSDK.resource_method("chat/completions", "POST")
    # def completions(self, data: dict):
    #     pass
