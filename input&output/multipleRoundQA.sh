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