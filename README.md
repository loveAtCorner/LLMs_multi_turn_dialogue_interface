# 大模型多轮对话接口实现


## 项目配置

本项目，使用 vllms 启动 openai 格式的大模型接口服务（格式规范可以参考 input&output 文件夹下的接口调用样例）
在此基础上，开发了多轮对话的功能


## Roadmap（开发路径）

- 增加会话状态：
  - 在每一轮对话开始时，会通过 user_id 和 session_id 来确定当前对话的状态，创建一个会话实例，用于区别不同用户在不同时间打开的会话窗口
- 增加历史对话管理：
  - 每一轮新的会话状态下，用户所有的问答内容都会被保存在历史对话管理器中。
  - 历史对话管理器会定期清理过期的历史对话，以保证内存使用效率。
- 集成多轮对话管理：
  - 根据用户的会话状态，从历史对话中检索该用户的历史对话信息，整合后与大语言模型服务交互
  - 根据大模型服务的上下文长度限制，裁剪历史对话内容，保留最近的对话记录


## 为什么不使用langchain

因为不知道langchain的底层是怎么实现的
学习langchain的类和函数的具体用法需要的时间成本高
要花大量到时间去学习，查找最佳实践
不如从头开始开发，一方面缩短了开发周期，一方面梳理了开发思路
参考文章
[]()


## 使用案例

```python
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
```
