from multi_turn_dialogue_manager import BaseMultipleTurnConversationManager
from datetime import datetime, timedelta
import time


if __name__ == "__main__":
    
    conversation_manager = BaseMultipleTurnConversationManager()
    user_id = "test_user"
    session_id = "session_123"
    max_context_length = 4000

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

    # 定义睡眠时间2分钟
    sleep_duration = timedelta(minutes=2)

    # 计算总秒数并睡眠
    time.sleep(sleep_duration.total_seconds())

    # 查询历史对话记录
    history = conversation_manager.history_manager.get_history(user_id, session_id)
    print("History:", history)