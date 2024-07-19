import requests
from typing import List, Dict
from datetime import datetime
import logging
import yaml

# 读取 YAML 配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 配置日志记录
logging.basicConfig(
    filename='conversation.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

class SessionState:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.session_id = self._generate_session_id()
        self.start_time = datetime.now()
        self.context = []

    def _generate_session_id(self):
        return f"{self.user_id}_{int(datetime.now().timestamp())}"

class ConversationHistory:
    def __init__(self):
        self.histories: Dict[str, List[Dict[str, str]]] = {}

    def add_message(self, user_id: str, message: Dict[str, str]):
        if user_id not in self.histories:
            self.histories[user_id] = []
        self.histories[user_id].append(message)

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}

    def start_new_session(self, user_id: str) -> SessionState:
        session_state = SessionState(user_id)
        self.sessions[user_id] = session_state
        return session_state

    def get_session(self, user_id: str) -> SessionState:
        return self.sessions.get(user_id, self.start_new_session(user_id))

class HistoryManager:
    def __init__(self):
        self.conversation_history = ConversationHistory()

    def add_to_history(self, user_id: str, user_message: str, bot_response: str):
        message = {
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.add_message(user_id, message)

    def get_history(self, user_id: str) -> List[Dict[str, str]]:
        return self.conversation_history.histories.get(user_id, [])

class ConversationManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.history_manager = HistoryManager()
        self.api_url = config['api']['url']
        self.headers = config['api']['headers']

    def handle_message(self, user_id: str, user_message: str) -> str:
        session = self.session_manager.get_session(user_id)
        history = self.history_manager.get_history(user_id)

        bot_response = self.generate_response(user_message, history)

        self.history_manager.add_to_history(user_id, user_message, bot_response)
        
        # 记录请求和回复到日志文件
        logger.info(f"User ID: {user_id} | User Message: {user_message} | Bot Response: {bot_response}")

        return bot_response

    def generate_response(self, user_message: str, history: List[Dict[str, str]]) -> str:
        messages = [{"role": "system", "content": config['conversation']['system_message']}]
        for h in history:
            messages.append({"role": "user", "content": h["user_message"]})
            messages.append({"role": "assistant", "content": h["bot_response"]})
        messages.append({"role": "user", "content": user_message})

        data = {
            "model": config['conversation']['model'],
            "messages": messages,
            "temperature": config['conversation']['temperature']
        }

        print(data)
        response = requests.post(self.api_url, headers=self.headers, json=data)
        response_data = response.json()
        
        # 记录请求和回复到日志文件
        logger.info(f"Request Data: {data}")
        logger.info(f"Response Data: {response_data}")

        return response_data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    conversation_manager = ConversationManager()
    user_id = "test_user"

    user_message = "给我讲一些有关汉服的故事吧"
    response = conversation_manager.handle_message(user_id, user_message)
    # print("Bot:", response)

    user_message = "请根据上一个问题的回答写一个营销策划"
    response = conversation_manager.handle_message(user_id, user_message)
    # print("Bot:", response)

    user_message = "请评价上一个问题中提到的营销策划"
    response = conversation_manager.handle_message(user_id, user_message)
    # print("Bot:", response)
    
    # 查询历史对话记录
    # history = conversation_manager.history_manager.get_history(user_id)
    # print("History:", history)
