"""
### 说明

1. **TestSessionState**: 测试 `SessionState` 类的创建和初始值，并打印创建会话的用户 ID。
2. **TestConversationHistory**: 测试 `ConversationHistory` 类中添加消息的功能，并打印添加消息的用户 ID 和消息内容。
3. **TestSessionManager**: 测试 `SessionManager` 类的会话创建和获取功能，并打印相关的操作信息。
4. **TestHistoryManager**: 测试 `HistoryManager` 类的添加历史记录和获取历史记录功能，并打印相关的操作信息。
5. **TestConversationManager**:
   - `test_handle_message`: 测试 `handle_message` 方法，并打印处理消息的用户 ID 和消息内容。
   - `test_generate_response`: 测试 `generate_response` 方法，并打印生成回复的用户消息。
   - `test_generate_response_with_history`: 测试带有历史记录的 `generate_response` 方法，并打印生成回复的用户消息和历史记录。

通过运行这个测试脚本，您可以在测试过程中看到更多的调试信息，帮助更好地理解每个测试步骤的具体内容。
"""

import unittest
from unittest.mock import patch
from datetime import datetime
from conversation_manager import ConversationManager, SessionState, ConversationHistory, SessionManager, HistoryManager
import json

class TestSessionState(unittest.TestCase):
    def test_session_creation(self):
        user_id = "test_user"
        session = SessionState(user_id)
        print(f"Creating session for user_id: {user_id}")
        self.assertEqual(session.user_id, user_id)
        self.assertIsNotNone(session.session_id)
        self.assertIsInstance(session.start_time, datetime)
        self.assertEqual(session.context, [])

class TestConversationHistory(unittest.TestCase):
    def test_add_message(self):
        history = ConversationHistory()
        user_id = "test_user"
        message = {"user_message": "Hello", "bot_response": "Hi"}
        print(f"Adding message to history for user_id: {user_id}")
        history.add_message(user_id, message)
        self.assertIn(user_id, history.histories)
        self.assertEqual(history.histories[user_id][0], message)

class TestSessionManager(unittest.TestCase):
    def test_start_new_session(self):
        manager = SessionManager()
        user_id = "test_user"
        print(f"Starting new session for user_id: {user_id}")
        session = manager.start_new_session(user_id)
        self.assertIn(user_id, manager.sessions)
        self.assertEqual(manager.sessions[user_id], session)

    def test_get_session(self):
        manager = SessionManager()
        user_id = "test_user"
        print(f"Getting session for user_id: {user_id}")
        session = manager.get_session(user_id)
        self.assertEqual(manager.sessions[user_id], session)

class TestHistoryManager(unittest.TestCase):
    def test_add_to_history(self):
        manager = HistoryManager()
        user_id = "test_user"
        user_message = "Hello"
        bot_response = "Hi"
        print(f"Adding to history for user_id: {user_id}, user_message: {user_message}, bot_response: {bot_response}")
        manager.add_to_history(user_id, user_message, bot_response)
        history = manager.get_history(user_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user_message"], user_message)
        self.assertEqual(history[0]["bot_response"], bot_response)
        self.assertIn("timestamp", history[0])

class TestConversationManager(unittest.TestCase):
    @patch('requests.post')
    def test_handle_message(self, mock_post):
        mock_response = {
            "choices": [
                {"message": {"content": "Hi there!"}}
            ]
        }
        mock_post.return_value.json.return_value = mock_response

        manager = ConversationManager()
        user_id = "test_user"
        user_message = "Hello"
        print(f"Handling message for user_id: {user_id}, user_message: {user_message}")
        response = manager.handle_message(user_id, user_message)
        self.assertEqual(response, "Hi there!")
        
        history = manager.history_manager.get_history(user_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user_message"], user_message)
        self.assertEqual(history[0]["bot_response"], "Hi there!")

    @patch('requests.post')
    def test_generate_response(self, mock_post):
        mock_response = {
            "choices": [
                {"message": {"content": "Hi there!"}}
            ]
        }
        mock_post.return_value.json.return_value = mock_response

        manager = ConversationManager()
        user_message = "Hello"
        history = []
        print(f"Generating response for user_message: {user_message} with empty history")
        response = manager.generate_response(user_message, history)
        self.assertEqual(response, "Hi there!")

    @patch('requests.post')
    def test_generate_response_with_history(self, mock_post):
        mock_response = {
            "choices": [
                {"message": {"content": "Sure, let me tell you about West Lake."}}
            ]
        }
        mock_post.return_value.json.return_value = mock_response

        manager = ConversationManager()
        user_message = "Tell me about West Lake."
        history = [
            {"user_message": "Tell me a story about Hangzhou.", "bot_response": "Hangzhou is known for its beautiful West Lake."}
        ]
        print(f"Generating response for user_message: {user_message} with history: {history}")
        response = manager.generate_response(user_message, history)
        self.assertEqual(response, "Sure, let me tell you about West Lake.")

if __name__ == "__main__":
    unittest.main()