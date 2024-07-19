# 多轮对话接口

## 开发思路
1. 我要解决一个什么应用场景下的问题，为了解决这个问题我需要实现哪些功能模块，每个模块负责完成哪一部分的功能
2. 开发模块（GPT完成）
3. 测试模块（GPT完成）

## Roadmap
下面是一些可能需要进行修改和扩展的地方：

模型推理部分
- 增加会话状态：在每一轮对话开始时，需要判断用户是否进入了新的会话，并将用户的会话状态保存下来。这样，在下一轮对话中，你就可以根据用户的会话状态来生成合适的回答。 
- 每一轮问答中添加上下文信息：在每一轮对话中，需要添加上下文信息，以便模型能够更好地理解用户的意图。例如，在每一轮对话开始时，需要为模型提供上一轮对话的回答、用户的历史搜索记录等信息。 

模型精调部分
- 增加多轮对话的训练集：如果要训练一个多轮对话模型，需要增加多轮对话的训练集，以便模型能够更好地学习多轮对话的特征。这可能需要重新训练模型，并使用多轮对话的数据进行评估。 
- 修改评估指标：在多轮对话中，需要修改评估指标，以便更好地评估模型的性能。例如，你可以使用BLEU等指标来评估多轮对话的效果。


## 为什么不使用langchain

因为不知道langchain的底层是怎么实现的
学习langchain的类和函数的具体用法需要的时间成本高
要花大量到时间去学习，查找最佳实践
在查找的过程中，人的思路是混乱
做事写代码，思路清晰最重要
不如从头开始开发

- 怎么和vllm兼容
- 怎么管理历史对话
- 怎么管理会话窗口


## 使用案例

```python
conversation_manager = ConversationManager()

# 进行多轮对话
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
history = conversation_manager.history_manager.get_history(user_id)
print("History:", history)
```


## 底层vllms大模型接口调用规范

**单轮**
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chinese-llama-alpaca-2",
    "messages": [
      {"role": "user","content": "给我讲一些有关杭州的故事吧"}
    ]
  }'
```

```json
{
    "id": "cmpl-8fc1b6356cf64681a41a8739445a8cf8",
    "object": "chat.completion",
    "created": 1690872695,
    "model": "chinese-llama-alpaca-2",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "好的，请问您对杭州有什么特别的偏好吗？"
            }
        }
    ]
}
```

**多轮**
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chinese-llama-alpaca-2",
    "messages": [
      {"role": "user","content": "给我讲一些有关杭州的故事吧"},
      {"role": "assistant","content": "好的，请问您对杭州有什么特别的偏好吗？"},
      {"role": "user","content": "我比较喜欢和西湖，可以给我讲一下西湖吗"}
    ],
    "repetition_penalty": 1.0
  }'
```

```json
{
    "id": "cmpl-02bf36497d3543c980ca2ae8cc4feb63",
    "object": "chat.completion",
    "created": 1690872676,
    "model": "chinese-llama-alpaca-2",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "是的，西湖是杭州最著名的景点之一，它被誉为“人间天堂”。 <\\s>"
            }
        }
    ]
}
```
