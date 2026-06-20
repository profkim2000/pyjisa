import random

def rps_game():
    # 선택지 리스트
    choices = ["가위", "바위", "보"]
    
    print("====================================")
    print("🤖 컴퓨터와 함께하는 가위바위보 게임! 🤖")
    print("====================================")
    print("(종료하고 싶다면 '종료'를 입력하세요.)\n")

    while True:
        # 컴퓨터의 무작위 선택
        computer_choice = random.choice(choices)
        
        # 사용자 입력 받기
        user_choice = input("가위, 바위, 보 중 하나를 선택하세요: ").strip()
        
        # 종료 조건 확인
        if user_choice == "종료":
            print("\n👋 게임을 종료합니다. 다음에 또 봐요!")
            break
            
        # 올바른 입력인지 검증
        if user_choice not in choices:
            print("🚨 잘못된 입력입니다! '가위', '바위', '보' 중에서만 입력해주세요.\n")
            continue
            
        print(f"👉 사용자: {user_choice} VS 컴퓨터: {computer_choice}")
        
        # 승패 판정 무직
        if user_choice == computer_choice:
            print("🤝 비겼습니다! 다시 대결합니다.\n")
        elif (user_choice == "가위" and computer_choice == "보") or \
             (user_choice == "바위" and computer_choice == "가위") or \
             (user_choice == "보" and computer_choice == "바위"):
            print("🎉 축하합니다! 당신이 이겼습니다! 🎉\n")
        else:
            print("💻 컴퓨터가 이겼습니다! 아쉽네요. 😢\n")

# 게임 실행
if __name__ == "__main__":
    rps_game()