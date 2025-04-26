import os
import logging
from beeai_framework.backend.chat import ChatModel

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
logger = logging.getLogger(__name__)

class LLMProvider:
    def __init__(self):
        self.providers = {
            "openai": self._get_openai,
            "watsonx": self._get_watsonx,
            "ollama": self._get_ollama,
        }

    def get_llm(self, provider_name, **kwargs):
        provider = self.providers.get(provider_name.lower())
        if not provider:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")
        logger.info(f"LLM provider: {provider_name}")
        return provider(**kwargs)

    def _get_openai(self, model="gpt-3.5-turbo"):
        return ChatModel.from_name(
            f"openai:{model}",
            options={
                "api_key": os.getenv("OPENAI_API_KEY"),
                "api_base": "https://api.openai.com/v1",
            },
        )

    def _get_watsonx(self, model="meta-llama/llama-3-3-70b-instruct"):
        return ChatModel.from_name(
            f"watsonx:{model}",
            options={
                "project_id": os.getenv('WATSONX_PROJECT_ID'),
                "api_key": os.getenv('WATSONX_API_KEY'),
                "api_base": os.getenv('WATSONX_API_URL'),
            },
        )

    def _get_ollama(self, model="llama3.1"):
        return ChatModel.from_name(f"ollama:{model}")
 