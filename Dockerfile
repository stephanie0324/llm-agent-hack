FROM python:3.11-slim

# 安裝系統套件
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 建立工作目錄
WORKDIR /app

# 複製 app/ 目錄中的所有檔案到容器的 /app 目錄
COPY app/ /app/

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r /app/requirements.txt  --timeout=120

# 預設執行 Streamlit 應用
CMD ["streamlit", "run", "/app/travel_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
