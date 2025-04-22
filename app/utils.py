from typing import TypedDict, Optional
import urllib3
from config import settings

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Suppress SSL warnings if needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_response_from_ai_service(query: str) -> Optional[str]:
    """
    透過 Azure AI 服務取得回應（每次創建新的對話，模擬清除聊天）

    :param query: 用戶輸入的查詢內容
    :param language: 使用語言（目前未使用，可作為擴展用）
    :return: AI 回應訊息列表（純文字），或 None 表示失敗
    """
    try:
        # 初始化憑證與 client
        credential = DefaultAzureCredential()

        project_client = AIProjectClient.from_connection_string(
            credential=credential, conn_str=settings.AGENT_CONNECTION_STRING
        )

        # 取得 agent
        agent = project_client.agents.get_agent(settings.AGENT_ID)
        # 每次創建新的 thread，模擬清除聊天
        thread = project_client.agents.create_thread()

        # 發送訊息
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=query,
        )

        # 執行 AI 回應處理
        project_client.agents.create_and_process_run(
            thread_id=thread.id, agent_id=agent.id
        )

        messages = project_client.agents.list_messages(thread_id=thread.id)

        response_list = [
            m.as_dict()["text"]["value"]
            for m in messages.text_messages
            if m.as_dict().get("type") == "text" and "text" in m.as_dict()
        ]
        # logger.info(response_list)

        return response_list[0] if response_list else None

    except Exception as e:
        print(f"[get_response_from_ai_service] Error: {e}")
        return None
