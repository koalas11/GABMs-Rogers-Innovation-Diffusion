from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.models import ChatCompletionClient


def create_llm_client() -> ChatCompletionClient:
    """Get or create LLM client instance"""
    return OllamaChatCompletionClient(
        #model="mistral:7b",
        model="llama3.1:8b",
    )
