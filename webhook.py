from flask import Blueprint, request, jsonify
from db import save_user  # DB 저장 함수 임포트

webhook = Blueprint("webhook", __name__)

session_data = {}  # 예시: 메모리 세션 (실제 구현에선 Redis 추천)

@webhook.route("/webhook", methods=["POST"])
def kakao_webhook():
    data = request.get_json()
    user_id = data.get("userRequest", {}).get("user", {}).get("id")
    params = data.get("action", {}).get("params", {})

    region = params.get("지역")
    phone = params.get("핸드폰 번호")

    # 사용자별로 세션 데이터 저장
    if user_id not in session_data:
        session_data[user_id] = {}

    if region:
        session_data[user_id]["region"] = region
    if phone:
        session_data[user_id]["phone"] = phone

    user_region = session_data[user_id].get("region")
    user_phone = session_data[user_id].get("phone")

    if user_region and user_phone:
        save_user(user_id, user_region, user_phone)
        session_data.pop(user_id)  # 저장 끝났으면 세션 삭제

        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": f"{user_region} 지역과 {user_phone} 번호로 설정 완료! 내일부터 날씨 알려드릴게요 ☀️"
                    }
                }]
            }
        })
    else:
        # 아직 값이 부족한 경우
        if not user_region:
            prompt = "지역을 입력해 주세요."
        elif not user_phone:
            prompt = "핸드폰 번호를 입력해 주세요."

        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": prompt
                    }
                }]
            }
        })
