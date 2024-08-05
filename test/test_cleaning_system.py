import time
from datetime import timedelta
import sys
import os
sys.path.append("..")  
from src.multi_turn_dialogue_manager import BaseMultipleTurnConversationManager
import yaml


# 从配置文件读取对话存续时间
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

conversation_lifetime = timedelta(minutes=config['conversation']['cleaning']['lifetime'])

# 测试脚本
def test_conversation_manager():
    conversation_manager = BaseMultipleTurnConversationManager()

    user_id = "test_user"
    session_id = "session_123"
   
    # 添加几条对话记录
    system_prompt = "你现在是一个历史学家，请给出详细的历史故事。"
    user_message = "给我讲一些有关汉服的故事吧"
    response = conversation_manager.handle_message(user_id, session_id, user_message, system_prompt)
    # print("Bot:", response)
   
    time.sleep(2)
   
    system_prompt = "你现在是一个营销专家，请提供详细的营销策划。"
    user_message = "请根据上一个问题的回答写一个营销策划"
    response = conversation_manager.handle_message(user_id, session_id, user_message, system_prompt)
    # print("Bot:", response)
   
    time.sleep(2)
   
    system_prompt = "你现在是一个商业评论家，请评价营销策划。"
    user_message = "请评价上一个问题中提到的营销策划"
    response = conversation_manager.handle_message(user_id, session_id, user_message, system_prompt)
    # print("Bot:", response)
   
    # 查询历史对话记录
    history = conversation_manager.history_manager.get_history(user_id, session_id)
    print("History before cleanup:", history)
   
    # 模拟等待超过对话存续时间
    time.sleep((conversation_lifetime + timedelta(seconds=10)).total_seconds())
   
    # 查询历史对话记录
    history = conversation_manager.history_manager.get_history(user_id, session_id)
    print("History after cleanup:", history)
   
    # 验证清理功能
    assert len(history) == 0, "History should be empty after cleanup"

    print("Test passed: History cleaned up correctly")

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    test_conversation_manager()
