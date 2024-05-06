# PyLapi API generated by pylapi_autogen.py
#
# API Class: oAPI
# 11 Resource Classes:
#      AudioResource: 2 native methods
#      ChatResource: 1 native methods
#      CompletionsResource: 1 native methods
#      EditsResource: 1 native methods
#      EmbeddingsResource: 1 native methods
#      FilesResource: 5 native methods
#      FineTunesResource: 5 native methods
#      FineTuningResource: 5 native methods
#      ImagesResource: 3 native methods
#      ModelsResource: 3 native methods
#      ModerationsResource: 1 native methods
# Total: 28 native methods


from pylapi import PyLapi, PyLapiError

class oAPI(PyLapi):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.api_url = "https://api.openai.com/v1"
        self.api_auth_type = "Bearer"


@oAPI.resource_class("audio", "audio")
class AudioResource(oAPI):
# To instantiate: oAPI.resource("audio")
# Number of native methods: 2
#     createTranscription
#     createTranslation

    @oAPI.resource_method("transcriptions", http_method="POST")
    def createTranscription(self): pass
    # To call: oAPI.resource("audio").createTranscription(...)
    # Request: POST https://api.openai.com/v1/audio/transcriptions

    # Summary: Transcribes audio into the input language.
    #
    # Request Body:
    #   content:
    #     multipart/form-data:
    #       schema:
    #         $ref: '#/components/schemas/CreateTranscriptionRequest'

    @oAPI.resource_method("translations", http_method="POST")
    def createTranslation(self): pass
    # To call: oAPI.resource("audio").createTranslation(...)
    # Request: POST https://api.openai.com/v1/audio/translations

    # Summary: Translates audio into English.
    #
    # Request Body:
    #   content:
    #     multipart/form-data:
    #       schema:
    #         $ref: '#/components/schemas/CreateTranslationRequest'

@oAPI.resource_class("chat", "chat")
class ChatResource(oAPI):
# To instantiate: oAPI.resource("chat")
# Number of native methods: 1
#     createChatCompletion

    @oAPI.resource_method("completions", http_method="POST")
    def createChatCompletion(self): pass
    # To call: oAPI.resource("chat").createChatCompletion(...)
    # Request: POST https://api.openai.com/v1/chat/completions

    # Summary: Creates a model response for the given chat conversation.
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateChatCompletionRequest'

@oAPI.resource_class("completions", "completions")
class CompletionsResource(oAPI):
# To instantiate: oAPI.resource("completions")
# Number of native methods: 1
#     createCompletion

    @oAPI.resource_method("", http_method="POST")
    def createCompletion(self): pass
    # To call: oAPI.resource("completions").createCompletion(...)
    # Request: POST https://api.openai.com/v1/completions

    # Summary: Creates a completion for the provided prompt and parameters.
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateCompletionRequest'

@oAPI.resource_class("edits", "edits")
class EditsResource(oAPI):
# To instantiate: oAPI.resource("edits")
# Number of native methods: 1
#     createEdit

    @oAPI.resource_method("", http_method="POST")
    def createEdit(self): pass
    # To call: oAPI.resource("edits").createEdit(...)
    # Request: POST https://api.openai.com/v1/edits

    # Summary: Creates a new edit for the provided input, instruction, and parameters.
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateEditRequest'

@oAPI.resource_class("embeddings", "embeddings")
class EmbeddingsResource(oAPI):
# To instantiate: oAPI.resource("embeddings")
# Number of native methods: 1
#     createEmbedding

    @oAPI.resource_method("", http_method="POST")
    def createEmbedding(self): pass
    # To call: oAPI.resource("embeddings").createEmbedding(...)
    # Request: POST https://api.openai.com/v1/embeddings

    # Summary: Creates an embedding vector representing the input text.
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateEmbeddingRequest'

@oAPI.resource_class("files", "files")
class FilesResource(oAPI):
# To instantiate: oAPI.resource("files")
# Number of native methods: 5
#     createFile
#     deleteFile
#     downloadFile
#     listFiles
#     retrieveFile

    @oAPI.resource_method("", http_method="POST")
    def createFile(self): pass
    # To call: oAPI.resource("files").createFile(...)
    # Request: POST https://api.openai.com/v1/files

    # Summary: Upload a file that contains document(s) to be used across various endpoints/features. Currently, the size of all the files uploaded by one organization can be up to 1 GB. Please contact us if you need to increase the storage limit.
    #
    # Request Body:
    #   content:
    #     multipart/form-data:
    #       schema:
    #         $ref: '#/components/schemas/CreateFileRequest'

    @oAPI.resource_method("{file_id}", http_method="DELETE")
    def deleteFile(self): pass
    # To call: oAPI.resource("files").deleteFile(file_id=..., ...)
    # Request: DELETE https://api.openai.com/v1/files/{file_id}

    # Summary: Delete a file.
    #
    # Parameters:
    #   file_id:
    #     in: path
    #     description: The ID of the file to use for this request.
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #     style: ''
    #     explode: false

    @oAPI.resource_method("{file_id}/content", http_method="GET")
    def downloadFile(self): pass
    # To call: oAPI.resource("files").downloadFile(file_id=..., ...)
    # Request: GET https://api.openai.com/v1/files/{file_id}/content

    # Summary: Returns the contents of the specified file.
    #
    # Parameters:
    #   file_id:
    #     in: path
    #     description: The ID of the file to use for this request.
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #     style: ''
    #     explode: false

    @oAPI.resource_method("", http_method="GET")
    def listFiles(self): pass
    # To call: oAPI.resource("files").listFiles(...)
    # Request: GET https://api.openai.com/v1/files

    # Summary: Returns a list of files that belong to the user's organization.

    @oAPI.resource_method("{file_id}", http_method="GET")
    def retrieveFile(self): pass
    # To call: oAPI.resource("files").retrieveFile(file_id=..., ...)
    # Request: GET https://api.openai.com/v1/files/{file_id}

    # Summary: Returns information about a specific file.
    #
    # Parameters:
    #   file_id:
    #     in: path
    #     description: The ID of the file to use for this request.
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #     style: ''
    #     explode: false

@oAPI.resource_class("fine_tunes", "fine-tunes")
class FineTunesResource(oAPI):
# To instantiate: oAPI.resource("fine_tunes")
# Number of native methods: 5
#     cancelFineTune
#     createFineTune
#     listFineTuneEvents
#     listFineTunes
#     retrieveFineTune

    @oAPI.resource_method("{fine_tune_id}/cancel", http_method="POST")
    def cancelFineTune(self): pass
    # To call: oAPI.resource("fine_tunes").cancelFineTune(fine_tune_id=..., ...)
    # Request: POST https://api.openai.com/v1/fine-tunes/{fine_tune_id}/cancel

    # Summary: Immediately cancel a fine-tune job.
    #
    # Parameters:
    #   fine_tune_id:
    #     in: path
    #     description: 'The ID of the fine-tune job to cancel
    #
    #       '
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: ft-AF1WoRqd3aJAHsqc9NY7iL8F
    #     style: ''
    #     explode: false

    @oAPI.resource_method("", http_method="POST")
    def createFineTune(self): pass
    # To call: oAPI.resource("fine_tunes").createFineTune(...)
    # Request: POST https://api.openai.com/v1/fine-tunes

    # Summary: Creates a job that fine-tunes a specified model from a given dataset.
    #
    #   Response includes details of the enqueued job including job status and the name of the fine-tuned models once complete.
    #
    #   [Learn more about fine-tuning](/docs/guides/legacy-fine-tuning)
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateFineTuneRequest'

    @oAPI.resource_method("{fine_tune_id}/events", http_method="GET")
    def listFineTuneEvents(self): pass
    # To call: oAPI.resource("fine_tunes").listFineTuneEvents(fine_tune_id=..., ...)
    # Request: GET https://api.openai.com/v1/fine-tunes/{fine_tune_id}/events

    # Summary: Get fine-grained status updates for a fine-tune job.
    #
    # Parameters:
    #   fine_tune_id:
    #     in: path
    #     description: 'The ID of the fine-tune job to get events for.
    #
    #       '
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: ft-AF1WoRqd3aJAHsqc9NY7iL8F
    #     style: ''
    #     explode: false
    #   stream:
    #     in: query
    #     description: 'Whether to stream events for the fine-tune job. If set to true,
    #
    #       events will be sent as data-only
    #
    #       [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
    #
    #       as they become available. The stream will terminate with a
    #
    #       `data: [DONE]` message when the job is finished (succeeded, cancelled,
    #
    #       or failed).
    #
    #
    #       If set to false, only events generated so far will be returned.
    #
    #       '
    #     required: false
    #     example: ''
    #     schema:
    #       type: boolean
    #       default: false
    #     style: ''
    #     explode: false

    @oAPI.resource_method("", http_method="GET")
    def listFineTunes(self): pass
    # To call: oAPI.resource("fine_tunes").listFineTunes(...)
    # Request: GET https://api.openai.com/v1/fine-tunes

    # Summary: List your organization's fine-tuning jobs

    @oAPI.resource_method("{fine_tune_id}", http_method="GET")
    def retrieveFineTune(self): pass
    # To call: oAPI.resource("fine_tunes").retrieveFineTune(fine_tune_id=..., ...)
    # Request: GET https://api.openai.com/v1/fine-tunes/{fine_tune_id}

    # Summary: Gets info about the fine-tune job.
    #
    #   [Learn more about fine-tuning](/docs/guides/legacy-fine-tuning)
    #
    # Parameters:
    #   fine_tune_id:
    #     in: path
    #     description: 'The ID of the fine-tune job
    #
    #       '
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: ft-AF1WoRqd3aJAHsqc9NY7iL8F
    #     style: ''
    #     explode: false

@oAPI.resource_class("fine_tuning", "fine_tuning")
class FineTuningResource(oAPI):
# To instantiate: oAPI.resource("fine_tuning")
# Number of native methods: 5
#     cancelFineTuningJob
#     createFineTuningJob
#     listFineTuningEvents
#     listPaginatedFineTuningJobs
#     retrieveFineTuningJob

    @oAPI.resource_method("jobs/{fine_tuning_job_id}/cancel", http_method="POST")
    def cancelFineTuningJob(self): pass
    # To call: oAPI.resource("fine_tuning").cancelFineTuningJob(fine_tuning_job_id=..., ...)
    # Request: POST https://api.openai.com/v1/fine_tuning/jobs/{fine_tuning_job_id}/cancel

    # Summary: Immediately cancel a fine-tune job.
    #
    # Parameters:
    #   fine_tuning_job_id:
    #     in: path
    #     description: 'The ID of the fine-tuning job to cancel.
    #
    #       '
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: ft-AF1WoRqd3aJAHsqc9NY7iL8F
    #     style: ''
    #     explode: false

    @oAPI.resource_method("jobs", http_method="POST")
    def createFineTuningJob(self): pass
    # To call: oAPI.resource("fine_tuning").createFineTuningJob(...)
    # Request: POST https://api.openai.com/v1/fine_tuning/jobs

    # Summary: Creates a job that fine-tunes a specified model from a given dataset.
    #
    #   Response includes details of the enqueued job including job status and the name of the fine-tuned models once complete.
    #
    #   [Learn more about fine-tuning](/docs/guides/fine-tuning)
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateFineTuningJobRequest'

    @oAPI.resource_method("jobs/{fine_tuning_job_id}/events", http_method="GET")
    def listFineTuningEvents(self): pass
    # To call: oAPI.resource("fine_tuning").listFineTuningEvents(fine_tuning_job_id=..., ...)
    # Request: GET https://api.openai.com/v1/fine_tuning/jobs/{fine_tuning_job_id}/events

    # Summary: Get status updates for a fine-tuning job.
    #
    # Parameters:
    #   fine_tuning_job_id:
    #     in: path
    #     description: 'The ID of the fine-tuning job to get events for.
    #
    #       '
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: ft-AF1WoRqd3aJAHsqc9NY7iL8F
    #     style: ''
    #     explode: false
    #   after:
    #     in: query
    #     description: Identifier for the last event from the previous pagination request.
    #     required: false
    #     example: ''
    #     schema:
    #       type: string
    #     style: ''
    #     explode: false
    #   limit:
    #     in: query
    #     description: Number of events to retrieve.
    #     required: false
    #     example: ''
    #     schema:
    #       type: integer
    #       default: 20
    #     style: ''
    #     explode: false

    @oAPI.resource_method("jobs", http_method="GET")
    def listPaginatedFineTuningJobs(self): pass
    # To call: oAPI.resource("fine_tuning").listPaginatedFineTuningJobs(...)
    # Request: GET https://api.openai.com/v1/fine_tuning/jobs

    # Summary: List your organization's fine-tuning jobs
    #
    # Parameters:
    #   after:
    #     in: query
    #     description: Identifier for the last job from the previous pagination request.
    #     required: false
    #     example: ''
    #     schema:
    #       type: string
    #     style: ''
    #     explode: false
    #   limit:
    #     in: query
    #     description: Number of fine-tuning jobs to retrieve.
    #     required: false
    #     example: ''
    #     schema:
    #       type: integer
    #       default: 20
    #     style: ''
    #     explode: false

    @oAPI.resource_method("jobs/{fine_tuning_job_id}", http_method="GET")
    def retrieveFineTuningJob(self): pass
    # To call: oAPI.resource("fine_tuning").retrieveFineTuningJob(fine_tuning_job_id=..., ...)
    # Request: GET https://api.openai.com/v1/fine_tuning/jobs/{fine_tuning_job_id}

    # Summary: Get info about a fine-tuning job.
    #
    #   [Learn more about fine-tuning](/docs/guides/fine-tuning)
    #
    # Parameters:
    #   fine_tuning_job_id:
    #     in: path
    #     description: 'The ID of the fine-tuning job.
    #
    #       '
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: ft-AF1WoRqd3aJAHsqc9NY7iL8F
    #     style: ''
    #     explode: false

@oAPI.resource_class("images", "images")
class ImagesResource(oAPI):
# To instantiate: oAPI.resource("images")
# Number of native methods: 3
#     createImage
#     createImageEdit
#     createImageVariation

    @oAPI.resource_method("generations", http_method="POST")
    def createImage(self): pass
    # To call: oAPI.resource("images").createImage(...)
    # Request: POST https://api.openai.com/v1/images/generations

    # Summary: Creates an image given a prompt.
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateImageRequest'

    @oAPI.resource_method("edits", http_method="POST")
    def createImageEdit(self): pass
    # To call: oAPI.resource("images").createImageEdit(...)
    # Request: POST https://api.openai.com/v1/images/edits

    # Summary: Creates an edited or extended image given an original image and a prompt.
    #
    # Request Body:
    #   content:
    #     multipart/form-data:
    #       schema:
    #         $ref: '#/components/schemas/CreateImageEditRequest'

    @oAPI.resource_method("variations", http_method="POST")
    def createImageVariation(self): pass
    # To call: oAPI.resource("images").createImageVariation(...)
    # Request: POST https://api.openai.com/v1/images/variations

    # Summary: Creates a variation of a given image.
    #
    # Request Body:
    #   content:
    #     multipart/form-data:
    #       schema:
    #         $ref: '#/components/schemas/CreateImageVariationRequest'

@oAPI.resource_class("models", "models")
class ModelsResource(oAPI):
# To instantiate: oAPI.resource("models")
# Number of native methods: 3
#     deleteModel
#     listModels
#     retrieveModel

    @oAPI.resource_method("{model}", http_method="DELETE")
    def deleteModel(self): pass
    # To call: oAPI.resource("models").deleteModel(model=..., ...)
    # Request: DELETE https://api.openai.com/v1/models/{model}

    # Summary: Delete a fine-tuned model. You must have the Owner role in your organization to delete a model.
    #
    # Parameters:
    #   model:
    #     in: path
    #     description: The model to delete
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: ft:gpt-3.5-turbo:acemeco:suffix:abc123
    #     style: ''
    #     explode: false

    @oAPI.resource_method("", http_method="GET")
    def listModels(self): pass
    # To call: oAPI.resource("models").listModels(...)
    # Request: GET https://api.openai.com/v1/models

    # Summary: Lists the currently available models, and provides basic information about each one such as the owner and availability.

    @oAPI.resource_method("{model}", http_method="GET")
    def retrieveModel(self): pass
    # To call: oAPI.resource("models").retrieveModel(model=..., ...)
    # Request: GET https://api.openai.com/v1/models/{model}

    # Summary: Retrieves a model instance, providing basic information about the model such as the owner and permissioning.
    #
    # Parameters:
    #   model:
    #     in: path
    #     description: The ID of the model to use for this request
    #     required: true
    #     example: ''
    #     schema:
    #       type: string
    #       example: gpt-3.5-turbo
    #     style: ''
    #     explode: false

@oAPI.resource_class("moderations", "moderations")
class ModerationsResource(oAPI):
# To instantiate: oAPI.resource("moderations")
# Number of native methods: 1
#     createModeration

    @oAPI.resource_method("", http_method="POST")
    def createModeration(self): pass
    # To call: oAPI.resource("moderations").createModeration(...)
    # Request: POST https://api.openai.com/v1/moderations

    # Summary: Classifies if text violates OpenAI's Content Policy
    #
    # Request Body:
    #   content:
    #     application/json:
    #       schema:
    #         $ref: '#/components/schemas/CreateModerationRequest'


# Custom new resource classes

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
