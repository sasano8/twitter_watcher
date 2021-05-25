import logging

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage

from .config import LineChannelConfig

logger = logging.getLogger(__name__)

LINE_CHANNEL_ACCESS_TOKEN = LineChannelConfig().LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


def broadcast(*messages):
    print(messages)
    arr = [TextSendMessage(text=msg) for msg in messages if msg is not None]
    try:
        line_bot_api.broadcast(messages=arr)
    except LineBotApiError as e:
        logger.critical(e)