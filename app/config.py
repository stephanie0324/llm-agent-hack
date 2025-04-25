import json
from typing import Optional, List, Union, Pattern, Dict
from pydantic import validator, PositiveInt
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, confloat, constr, conlist

from schemas.llms_config_schema import LlmsConfig, ModelEntry


class Settings(BaseSettings):

    # DEBUG模式，若為true會輸出chain執行的詳細過程.
    DEBUG: bool = False

    WEATHER_API_KEY: str = ""

    # Agent
    AGENT_CONNECTION_STRING: str = ""
    AGENT_ID: str = ""

    LOCAL_MODEL_NAME: str = "microsoft/phi-4"
    LOCAL_MODEL_API: str = ""
    OPENAI_API_KEY: str = "EMPTY"
    ## AOAI
    AZURE_DEPLOYMENT: constr(min_length=1) = "gpt-4o-mini"
    AZURE_API_VERSION: constr(min_length=1) = "2024-08-01-preview"
    AZURE_OPENAI_ENDPOINT: str = "https://model-deploy.openai.azure.com/"
    AZURE_OPENAI_API_KEY: str = ""

    MODEL_CONFIG: LlmsConfig = {
        "AOAI": {
            "type": "AzureChatOpenAI",
            "args": {
                "max_tokens": 5000,
                "temperature": 0,
                "max_retries": 0,
                "request_timeout": 90,
            },
        },
        "LOCAL": {
            "type": "ChatOpenAI",
            "args": {
                "model_name": "microsoft/phi-4",
                "openai_api_key": "EMPTY",
                "openai_api_base": "",
                "temperature": 0,
            },
        },
    }

    @validator("MODEL_CONFIG", pre=True, always=True)
    def model_config_convert_to_object_and_add_openai_key(
        cls,
        # NOTE: 無論是用預設值還是用環境變數帶入，v type都是Dict[str, dict]，而非Dict[str, ModelEntry]
        v: Dict[str, dict],
        values,
    ) -> LlmsConfig:
        for key, model_conf in v.items():
            # 將dict 轉 ModelEntry obj.
            if isinstance(model_conf, dict):
                model_conf = ModelEntry(**model_conf)
                v[key] = model_conf
            if model_conf.type == "ChatOpenAI":
                model_conf.args["openai_api_key"] = values["OPENAI_API_KEY"]
                model_conf.args["model_name"] = values["LOCAL_MODEL_NAME"]
                model_conf.args["openai_api_base"] = values["LOCAL_MODEL_API"]
            if model_conf.type == "AzureChatOpenAI":
                model_conf.args["azure_deployment"] = values["AZURE_DEPLOYMENT"]
                model_conf.args["api_version"] = values["AZURE_API_VERSION"]
                model_conf.args["api_key"] = values["AZURE_OPENAI_API_KEY"]
                model_conf.args["azure_endpoint"] = values["AZURE_OPENAI_ENDPOINT"]

        print(f"model_config: {v}")
        return v

    ### CORS設定 ###

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

    # Origins that match this regex OR are in the above list are allowed
    BACKEND_CORS_ORIGIN_REGEX: Optional[Pattern] = ".*"

    ### Doc ###

    # 傳入"None"代表關閉api docs網頁
    DOCS_URL: Optional[str] = "/docs"

    @validator("DOCS_URL", pre=True)
    def convert_str_none(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str) and v.lower() == "none":
            return None
        return v

    class Config:
        env_file = "conf/.env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
