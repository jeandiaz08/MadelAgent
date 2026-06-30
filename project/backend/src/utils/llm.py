import os
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq


load_dotenv(find_dotenv())

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def get_llm(temperature=0, max_tokens=None):
    return ChatGroq(
        model=DEFAULT_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )


def normalize_usage(response):
    usage = response.response_metadata.get("token_usage", {}) if response.response_metadata else {}
    if not usage and getattr(response, "usage_metadata", None):
        usage = {
            "prompt_tokens": response.usage_metadata.get("input_tokens", 0),
            "completion_tokens": response.usage_metadata.get("output_tokens", 0),
            "total_tokens": response.usage_metadata.get("total_tokens", 0),
        }

    prompt_tokens = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
    completion_tokens = usage.get("completion_tokens") or usage.get("output_tokens") or 0
    total_tokens = usage.get("total_tokens") or prompt_tokens + completion_tokens

    return {
        "model": DEFAULT_MODEL,
        "input_tokens": int(prompt_tokens or 0),
        "output_tokens": int(completion_tokens or 0),
        "total_tokens": int(total_tokens or 0),
    }


def ask_llm(prompt, user_question, temperature=0, max_tokens=300, return_usage=False):
    llm = get_llm(temperature=temperature, max_tokens=max_tokens)
    response = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=user_question),
    ])

    content = response.content.strip()
    if return_usage:
        return content, normalize_usage(response)
    return content
