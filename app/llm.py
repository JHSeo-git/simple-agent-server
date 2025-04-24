import boto3
from langchain_aws import ChatBedrock

from app.log import get_logger

logger = get_logger(__name__)


def initialize_llm():
    brt = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",
    )

    model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    config = {
        "max_tokens": 4096,
        "temperature": 0,
        "top_p": 0.999,
        "top_k": 256,
    }

    return ChatBedrock(
        client=brt,
        model_id=model_id,
        model_kwargs=config,
    )


_llm_cache = None


def get_llm():
    global _llm_cache

    if _llm_cache is not None:
        return _llm_cache

    _llm_cache = initialize_llm()

    if _llm_cache is None:
        raise ValueError("Failed to initialize LLM")

    return _llm_cache
