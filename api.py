"""
### 解释
1. **导入 ConversationManager**：从 `conversation_manager.py` 导入 `ConversationManager` 类。
2. **创建 ConversationManager 实例**：用于管理会话和生成回复。
3. **模拟多轮对话**：
   - 发送第一轮用户消息并打印回复。
   - 发送第二轮用户消息并打印回复。
   - 发送第三轮用户消息并打印回复。
4. **多轮对话的上下文传递**：确保每轮对话的上下文信息能够正确传递，展示实际的问答过程。

运行这个脚本将展示用户与AI之间的三轮对话，每轮对话都关联前面的内容，确保对话的连贯性和上下文的连续性。
"""

from conversation_manager import ConversationManager

def multi_turn_conversation():
    conversation_manager = ConversationManager()
    user_id = "test_user"

    # 第一轮对话
    user_message1 = "给我讲一些有关汉服的故事吧"
    response1 = conversation_manager.handle_message(user_id, user_message1)
    print(f"用户: {user_message1}")
    print(f"AI: {response1}")

    # 第二轮对话
    user_message2 = "请根据上一个问题的回答写一个营销策划"
    response2 = conversation_manager.handle_message(user_id, user_message2)
    print(f"用户: {user_message2}")
    print(f"AI: {response2}")

    # 第三轮对话
    user_message3 = "请评价上一个问题中提到的营销策划"
    response3 = conversation_manager.handle_message(user_id, user_message3)
    print(f"用户: {user_message3}")
    print(f"AI: {response3}")
    
    # 查询历史对话记录
    # history = conversation_manager.history_manager.get_history(user_id)
    # print("History:", history)
    
if __name__ == "__main__":
    multi_turn_conversation()
