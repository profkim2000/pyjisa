import time
from datetime import datetime

try:
    while True:
        # 현재 시간 가져오기 (년-월-일 시:분:초 형식)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # \r (캐리지 리턴)을 사용하여 커서를 줄 맨 앞으로 이동하고 시간을 출력합니다.
        # end=""를 주어 줄바꿈이 일어나지 않도록 합니다.
        print(f"\r현재 시간: {now}", end="", flush=True)
        
        # 1초 동안 대기
        time.sleep(1)

except KeyboardInterrupt:
    # 사용자가 Ctrl + C를 누르면 안전하게 종료합니다.
    print("\n👋 시계를 종료합니다.")