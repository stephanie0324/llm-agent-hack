from pydantic import RootModel
from typing import Dict

from pydantic import BaseModel
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_community.llms import HuggingFaceTextGenInference


class ModelEntry(BaseModel):
    type: str
    args: dict

    def as_instance(self):
        if self.type == "ChatOpenAI":
            return ChatOpenAI(**self.args)
        elif self.type == "AzureChatOpenAI":
            return AzureChatOpenAI(**self.args)
        elif self.type == "HuggingFaceTextGenInference":
            return HuggingFaceTextGenInference(**self.args)
        else:
            raise Exception(f"未定義的 model type: {self.type}")


class LlmsConfig(RootModel):
    root: Dict[str, ModelEntry]
