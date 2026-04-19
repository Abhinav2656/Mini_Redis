FROM python:3.10-slim

RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY value_types.h basic_hashmap.h lru_cache.h server_main.cpp server.py requirements.txt ./

RUN g++ -o mini_redis server_main.cpp

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host","0.0.0.0", "--port", "8000"]
