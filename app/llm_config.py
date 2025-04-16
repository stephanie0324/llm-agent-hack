from langchain_openai import ChatOpenAI, AzureChatOpenAI


def get_phi4_llm():
    return ChatOpenAI(
        model="microsoft/phi-4",
        base_url="<your-host>",
        openai_api_key="EMPTY",
        openai_api_base="",
        temperature=0,
    )


def get_gpt_4o_llm():
    return AzureChatOpenAI(
        azure_deployment="gpt-4o-mini",
        api_version="2024-08-01-preview",
        azure_endpoint="https://model-deploy.openai.azure.com/",
        api_key="<your-api-key>",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
