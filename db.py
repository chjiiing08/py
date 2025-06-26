import pymysql

# 데이터베이스 연결 정보
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Chj152824!",  # 네 비밀번호로 바꿔!
    "db": "weather",
    "charset": "utf8mb4"
}

def connect():
    # DB에 연결해주는 함수
    return pymysql.connect(**DB_CONFIG)

def save_user(user_id, region, phone):
    conn = connect()
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO users (user_id, region, phone)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE region=%s, phone=%s
        """
        # 사용자 정보 저장, 이미 있으면 지역과 번호 업데이트
        cursor.execute(sql, (user_id, region, phone, region, phone))
        conn.commit()  # 변경사항 저장
    except Exception as e:
        print("DB 오류 발생:", e)
    finally:
        conn.close()

def get_users():
    conn = connect()
    try:
        cursor = conn.cursor()
        sql = "SELECT phone, region FROM users"
        cursor.execute(sql)
        users = cursor.fetchall()  # 저장된 사용자들 정보 가져오기
        return users
    except Exception as e:
        print("DB 오류 발생:", e)
        return []
    finally:
        conn.close()
