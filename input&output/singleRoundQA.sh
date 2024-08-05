curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chinese-llama-alpaca-2",
    "messages": [
      {"role": "user","content": "给我讲一些有关杭州的故事吧"}
    ]
  }'