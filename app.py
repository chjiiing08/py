from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Flask 서버 정상 작동 중입니다!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 받은 Webhook 메시지:", data)
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render는 여기서 지정한 포트를 사용
    app.run(host='0.0.0.0', port=port)
