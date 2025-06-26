import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Render!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render가 PORT 환경변수로 전달
    app.run(host='0.0.0.0', port=port)
