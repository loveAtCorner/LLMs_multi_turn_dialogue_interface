import unittest
from unittest.mock import patch
from datetime import datetime
import sys
sys.path.append("..")  
from src.multi_turn_dialogue_manager import BaseMultipleTurnConversationManager, SessionState, ConversationHistory, SessionManager, HistoryManager
import json

class TestSessionState(unittest.TestCase):
    """
    测试了SessionState类在初始化时创建一个新会话并打印用户ID。
    验证了属性如user_id、session_id（会话标识符）、开始时间（datetime类型）和上下文列表是否正确设置。
    """
    def test_session_creation(self):
        user_id = "test_user"
        session = SessionState(user_id, "session_123")
        print(f"Creating session for user_id: {user_id}")
        self.assertEqual(session.user_id, user_id)
        self.assertIsNotNone(session.session_id)
        self.assertIsInstance(session.start_time, datetime)
        self.assertEqual(session.context, [])

class TestConversationHistory(unittest.TestCase):
    """
    测试了ConversationHistory类中添加消息的功能，并通过打印用户ID、添加的消息内容以及历史记录的结构来确认功能的正确性。
    验证添加的消息能够成功存储在history数据结构中。
    """
    def test_add_message(self):
        history = ConversationHistory()
        user_id = "test_user"
        session_id = "session_123"
        message = {"user_message": "Hello", "bot_response": "Hi", "timestamp": datetime.now().isoformat()}
        print(f"Adding message to history for user_id: {user_id}, session_id: {session_id}")
        history.add_message(user_id, session_id, message)
        self.assertIn(f"{user_id}_{session_id}", history.histories)
        self.assertEqual(history.histories[f"{user_id}_{session_id}"][0], message)

class TestSessionManager(unittest.TestCase):
    """
    测试开始新会话：当给定一个用户ID时，验证了是否能够创建一个新的会话，并将其与提供的用户ID关联。
    """
    def test_start_new_session(self):
        manager = SessionManager()
        user_id = "test_user"
        print(f"Starting new session for user_id: {user_id}")
        session = manager.start_new_session(user_id)
        self.assertIn(user_id, manager.sessions)
        self.assertEqual(manager.sessions[user_id], session)

    """
    测试获取会话：通过提供一个已存在的用户ID来检查能否正确地检索相应的会话。
    """
    def test_get_session(self):
        manager = SessionManager()
        user_id = "test_user"
        print(f"Getting session for user_id: {user_id}")
        session = manager.get_session(user_id)
        self.assertEqual(manager.sessions[user_id], session)

class TestHistoryManager(unittest.TestCase):
    """
    测试add_to_history方法将特定用户的输入和回复添加到历史记录中，以及使用get_history方法获取用户的历史记录时是否能正确操作。
    """
    def test_add_to_history(self):
        manager = HistoryManager()
        user_id = "test_user"
        session_id = "session_123"
        user_message = "Hello"
        bot_response = "Hi"
        print(f"Adding to history for user_id: {user_id}, session_id: {session_id}, user_message: {user_message}, bot_response: {bot_response}")
        manager.add_to_history(user_id, session_id, user_message, bot_response)
        history = manager.get_history(user_id, session_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user_message"], user_message)
        self.assertEqual(history[0]["bot_response"], bot_response)
        self.assertIn("timestamp", history[0])

class TestBaseMultipleTurnConversationManager(unittest.TestCase):
    """
    测试handle_message：在模拟API调用响应的情况下（通过requests.post的mock），验证处理用户消息的功能，并检查与会话和历史管理相关的方法。
    """
    @patch('requests.post')
    def test_handle_message(self, mock_post):
        mock_response = {
            "choices": [
                {"message": {"content": "Hi there!"}}
            ]
        }
        mock_post.return_value.json.return_value = mock_response

        manager = BaseMultipleTurnConversationManager()
        user_id = "test_user"
        session_id = "session_123"
        user_message = "Hello"
        system_prompt = "You are a helpful assistant."
        print(f"Handling message for user_id: {user_id}, session_id: {session_id}, user_message: {user_message}, system_prompt:{system_prompt}")
        response = manager.handle_message(user_id, session_id, user_message, system_prompt)
        self.assertEqual(response, "Hi there!")
        
        history = manager.history_manager.get_history(user_id, session_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user_message"], user_message)
        self.assertEqual(history[0]["bot_response"], "Hi there!")

    """
    测试generate_response：对于一个空的历史记录集，该方法应生成回复。确认回复是否正确形成并返回给用户。
    """
    @patch('requests.post')
    def test_generate_response(self, mock_post):
        mock_response = {
            "choices": [
                {"message": {"content": "Hi there!"}}
            ]
        }
        mock_post.return_value.json.return_value = mock_response

        manager = BaseMultipleTurnConversationManager()
        user_message = "Hello"
        system_prompt = "You are a helpful assistant."
        history = []
        print(f"Generating response for user_message: {user_message} with empty history")
        response = manager.generate_response(user_message, history, system_prompt)
        self.assertEqual(response, "Hi there!")

    """
    测试generate_response_with_history：考虑了非空的历史记录情况时的回应生成功能。
    """
    @patch('requests.post')
    def test_generate_response_with_history(self, mock_post):
        mock_response = {
            "choices": [
                {"message": {"content": "Sure, let me tell you about West Lake."}}
            ]
        }
        mock_post.return_value.json.return_value = mock_response

        manager = BaseMultipleTurnConversationManager()
        user_message = "Tell me about West Lake."
        system_prompt = "You are a travel guide."
        history = [
            {"user_message": "Tell me a story about Hangzhou.", "bot_response": "Hangzhou is known for its beautiful West Lake."}
        ]
        print(f"Generating response for user_message: {user_message} with history: {history}")
        response = manager.generate_response(user_message, history, system_prompt)
        self.assertEqual(response, "Sure, let me tell you about West Lake.")

if __name__ == "__main__":
    unittest.main()
