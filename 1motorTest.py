import time
from dynamixel_sdk import * # --- 설정값 (내 환경에 맞게 확인) ---
DEVICENAME          = '/dev/ttyACM0'  # 리눅스/맥: 보통 ttyACM0, 윈도우: COM3, COM4 등
BAUDRATE            = 1000000         # 터틀봇3 모터 기본 통신속도 (1000000 아니면 57600)
DXL_ID              = 1               # 왼쪽 바퀴 ID: 1, 오른쪽 바퀴 ID: 2
PROTOCOL_VERSION    = 2.0

# --- 초기화 (딱 한 번만 실행되는 부분) ---
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 1. 포트 열기
if not portHandler.openPort():
    print("포트를 열 수 없습니다! 케이블 연결을 확인하세요.")
    quit()

# 2. 통신 속도 맞추기
if not portHandler.setBaudRate(BAUDRATE):
    print("통신 속도 설정 실패! BAUDRATE를 확인하세요.")
    quit()

# 3. 토크 켜기 (모터에 힘 주기)
# 주소 64번(Torque Enable)에 1(ON)을 보냄
packetHandler.write1ByteTxRx(portHandler, DXL_ID, 64, 1)
print("모터 연결 성공! 이제 움직입니다.")

# --- 실제 동작 코드 ---

try:
    while True:
        # [동작 1] 위치 2000으로 이동
        print("위치 2000으로 이동")
        packetHandler.write4ByteTxRx(portHandler, DXL_ID, 116, 2000) # 116번은 목표 위치 주소
        time.sleep(2)

        # [동작 2] 위치 0으로 이동
        print("위치 0으로 이동")
        packetHandler.write4ByteTxRx(portHandler, DXL_ID, 116, 0)
        time.sleep(2)

except KeyboardInterrupt:
    # 종료 시 토크 끄기 (힘 빼기)
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, 64, 0)
    portHandler.closePort()
    print("종료")
