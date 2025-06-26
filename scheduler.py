import schedule
import time
from weather import get_weather
from aligo_api import send_friend_talk
from fortune import luck
from message_builder import build_message
from db import get_users  # db.py에서 실제 DB 함수 불러오기

# 지역 코드 매핑
region_xy = {
    "서울": (60, 127), "부산": (98, 76), "대구": (89, 90), "인천": (55, 124),
    "광주": (58, 74), "대전": (67, 100), "울산": (102, 84), "세종": (66, 103),
    "경기도": (60, 120), "강원도": (73, 134), "충북": (69, 107), "충남": (68, 100),
    "전북": (64, 89), "전남": (51, 67), "경북": (87, 106), "경남": (91, 77), "제주": (52, 38)
}

def job():
    users = get_users()  # DB에서 전화번호, 지역명 가져오기
    for user in users:
        phone, region = user  # db.get_users()가 (phone, region) 튜플을 반환한다고 가정
        if region not in region_xy:
            print(f"[WARN] 등록되지 않은 지역: {region}")
            continue

        nx, ny = region_xy[region]

        weather_data = get_weather(region, nx, ny)
        if isinstance(weather_data, str):
            print(f"[ERROR] {weather_data}")
            continue

        tmx = weather_data.get("tmx")
        tmn = weather_data.get("tmn")
        pop = weather_data.get("pop")

        lucky = luck()

        message = build_message(region, tmx, tmn, pop, lucky)

        res = send_friend_talk("사용자", phone, message)
        if res.get("result_code") == "1":
            print(f"[SUCCESS] 메시지 전송 성공: {phone}")
        else:
            print(f"[FAIL] 메시지 전송 실패: {phone} | {res.get('message')}")

schedule.every().day.at("08:00").do(job)
schedule.every(1).minutes.do(job)  # 테스트용

if __name__ == "__main__":
    print("✅ 스케줄러 실행 중 (매일 08:00 친구톡 발송)")
    while True:
        schedule.run_pending()
        time.sleep(30)
