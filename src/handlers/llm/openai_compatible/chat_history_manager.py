from dataclasses import dataclass
import re
from typing import Literal, Optional


from engine_utils.media_utils import ImageUtils


@dataclass
class HistoryMessage:
    role: Optional[Literal['avatar', 'human']] = None
    content: str = ''
    timestamp: Optional[str] = None


name_dict = {
    "avatar": "assistant",
    "human": "user"
}


def filter_text(text):
    pattern = r"[^a-zA-Z0-9\u4e00-\u9fff,.\~!?，。！？ ]"  # 匹配不在范围内的字符
    filtered_text = re.sub(pattern, "", text)
    return filtered_text


class ChatHistory:
    def __init__(self, history_length):
        self.max_history_length = history_length
        self.message_history = []

    def add_message(self, message: HistoryMessage):
        history = self.message_history
        history.append(message)
        # thread safe
        while len(history) >= self.max_history_length:
            history.pop(0)

    def generate_next_messages(self, chat_text, images):
        def history_to_message(history: HistoryMessage):
            return {
                "role": name_dict[history.role],
                "content": filter_text(history.content),
            }
        history = self.message_history
        messages = list(map(history_to_message, history))
        if images and len(images) > 0:
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": filter_text(chat_text),
                    },
                ] + (list(map(lambda x: {"type": "image_url", "image_url": {"url": ImageUtils.format_image(x)}}, images)))
            })
        else: 
            messages.append({
                "role": "user",
                "content": filter_text(chat_text),
            })
        return messages        
    

  