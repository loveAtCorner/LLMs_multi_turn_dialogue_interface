import requests
from typing import List, Dict
from datetime import datetime, timedelta
import logging
import yaml
import time
import threading

# 读取 YAML 配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 配置日志记录
logging.basicConfig(
    filename='../logs/conversation.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

# 清理间隔时间和对话存续时间
cleaning_interval = timedelta(seconds=config['conversation']['cleaning']['interval'])
conversation_lifetime = timedelta(minutes=config['conversation']['cleaning']['lifetime'])
max_context_length = config['conversation']['max_context_length']

# 1. 定义数据结构

class SessionState:
    def __init__(self, user_id: str, session_id: str):
        self.user_id = user_id
        self.session_id = session_id
        self.start_time = datetime.now()
        self.context = []

# 用于管理用户的会话历史记录
class ConversationHistory:
    def __init__(self):
        self.histories: Dict[str, List[Dict[str, str]]] = {}

    def add_message(self, user_id: str, session_id: str, message: Dict[str, str]):
        key = f"{user_id}_{session_id}"
        if key not in self.histories:
            self.histories[key] = []
        self.histories[key].append(message)

    def get_messages(self, user_id: str, session_id: str) -> List[Dict[str, str]]:
        return self.histories.get(f"{user_id}_{session_id}", [])

    def clean_up(self):
        now = datetime.now()
        for key in list(self.histories.keys()):
            messages = self.histories[key]
            if messages and now - datetime.fromisoformat(messages[-1]['timestamp']) > conversation_lifetime:
                logger.info(f"Cleaning up history for {key}")
                del self.histories[key]

# 2. 会话管理函数

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}

    def start_new_session(self, user_id: str) -> SessionState:
        session_id = f"{user_id}_{int(datetime.now().timestamp())}"
        session_state = SessionState(user_id, session_id)
        self.sessions[user_id] = session_state
        return session_state

    def get_session(self, user_id: str) -> SessionState:
        return self.sessions.get(user_id, self.start_new_session(user_id))

# 3. 历史对话管理函数

class HistoryManager:
    def __init__(self):
        self.conversation_history = ConversationHistory()

    def add_to_history(self, user_id: str, session_id: str, user_message: str, bot_response: str):
        message = {
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.add_message(user_id, session_id, message)

    def get_history(self, user_id: str, session_id: str, max_length: int = 4000) -> List[Dict[str, str]]:
        messages = self.conversation_history.get_messages(user_id, session_id)
        total_length = 0
        trimmed_history = []
        
        for msg in reversed(messages):
            msg_length = len(msg["user_message"]) + len(msg["bot_response"])
            if total_length + msg_length > max_length:
                break
            trimmed_history.insert(0, msg)
            total_length += msg_length
        
        return trimmed_history
    
    def start_cleaning_task(self):
        def clean_periodically():
            while True:
                self.conversation_history.clean_up()
                threading.Event().wait(cleaning_interval.total_seconds())

        cleaning_thread = threading.Thread(target=clean_periodically, daemon=True)
        cleaning_thread.start()

# 4. 集成会话和历史管理

class BaseMultipleTurnConversationManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.history_manager = HistoryManager()
        self.api_url = config['api']['url']
        self.headers = config['api']['headers']
        self.history_manager.start_cleaning_task()

    def handle_message(self, user_id: str, session_id: str, user_message: str, system_prompt: str) -> str:
        session = self.session_manager.get_session(user_id)
        history = self.history_manager.get_history(user_id, session_id, max_context_length)

        bot_response = self.generate_response(user_message, history, system_prompt)

        self.history_manager.add_to_history(user_id, session_id, user_message, bot_response)

        logger.info(f"User ID: {user_id} | Session ID: {session_id} | User Message: {user_message} | Bot Response: {bot_response}")

        return bot_response

    def generate_response(self, user_message: str, history: List[Dict[str, str]], system_prompt: str) -> str:
        messages = [{"role": "system", "content": system_prompt}]
        for h in history:
            messages.append({"role": "user", "content": h["user_message"]})
            messages.append({"role": "assistant", "content": h["bot_response"]})
        messages.append({"role": "user", "content": user_message})

        data = {
            "model": config['conversation']['model'],
            "messages": messages,
            "temperature": config['conversation']['temperature']
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)
        response_data = response.json()

        logger.info(f"Request Data: {data}")
        logger.info(f"Response Data: {response_data}")

        return response_data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    conversation_manager = BaseMultipleTurnConversationManager()
    user_id = "test_user"
    session_id = "session_123"

    system_prompt = "你现在是一个历史学家，请给出详细的历史故事。"
    user_message = "给我讲一些有关汉服的故事吧"
    response = conversation_manager.handle_message(user_id, session_id, user_message, system_prompt)
    print("Bot:", response)

    system_prompt = "你现在是一个营销专家，请提供详细的营销策划。"
    user_message = "请根据上一个问题的回答写一个营销策划"
    response = conversation_manager.handle_message(user_id, session_id, user_message, system_prompt)
    print("Bot:", response)

    system_prompt = "你现在是一个商业评论家，请评价营销策划。"
    user_message = "请评价上一个问题中提到的营销策划"
    response = conversation_manager.handle_message(user_id, session_id, user_message, system_prompt)
    print("Bot:", response)

    # 定义睡眠时间3分钟
    sleep_duration = timedelta(minutes=2)

    # 计算总秒数并睡眠
    time.sleep(sleep_duration.total_seconds())

    # 查询历史对话记录
    history = conversation_manager.history_manager.get_history(user_id, session_id)
    print("History:", history)
