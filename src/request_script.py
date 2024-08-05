import requests
import json

# API 服务的URL
base_url = 'http://127.0.0.1:5000'

# 开始一个新会话
def start_session(user_id):
    response = requests.post(f'{base_url}/start_session', json={'user_id': user_id})
    return response.json()['session_id']

# 发送消息并获取响应
def send_message(user_id, session_id, user_message, system_prompt):
    payload = {
        'user_id': user_id,
        'session_id': session_id,
        'user_message': user_message,
        'system_prompt': system_prompt
    }
    response = requests.post(f'{base_url}/message', json=payload)
    return response.json()['response']

# 获取会话历史
def get_history(user_id, session_id):
    params = {
        'user_id': user_id,
        'session_id': session_id
    }
    response = requests.get(f'{base_url}/history', params=params)
    return response.json()['history']

if __name__ == '__main__':
    user_id = 'test_user'
    session_id = start_session(user_id)
    
    system_prompt = "你现在是一个历史学家，请给出详细的历史故事。"
    user_message = "给我讲一些有关汉服的故事吧"
    response = send_message(user_id, session_id, user_message, system_prompt)
    print("Bot:", response)
    
    system_prompt = "你现在是一个营销专家，请提供详细的营销策划。"
    user_message = "请根据上一个问题的回答写一个营销策划"
    response = send_message(user_id, session_id, user_message, system_prompt)
    print("Bot:", response)
    
    system_prompt = "你现在是一个商业评论家，请评价营销策划。"
    user_message = "请评价上一个问题中提到的营销策划"
    response = send_message(user_id, session_id, user_message, system_prompt)
    print("Bot:", response)
    
    history = get_history(user_id, session_id)
    print("History:", history)
