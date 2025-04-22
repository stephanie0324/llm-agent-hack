import logging

from config import settings

logging.basicConfig(
    format=settings.LOG_FORMAT,
    datefmt=settings.LOG_DATE_FORMAT,
    level=settings.LOG_LEVEL,
)
logger = logging.getLogger(__name__)

# 關閉所有 azure SDK 的 log
logging.getLogger("azure").setLevel(logging.WARNING)
