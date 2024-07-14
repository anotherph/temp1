import cv2
import asyncio
import threading
import numpy as np

# 비동기 함수 a 정의
async def async_function_a():
    print("Function a is starting.")
    await asyncio.sleep(1)  # 1초 동안 대기
    print("Function a is done.")

# 이벤트 루프를 별도 스레드에서 실행
def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# 비동기 함수 호출을 위한 래퍼
def call_async_function(loop):
    asyncio.run_coroutine_threadsafe(async_function_a(), loop)

# 메인 함수 정의
def main():
    # OpenCV 웹캠 초기화
    cap = cv2.VideoCapture(0)

    # 새로운 이벤트 루프 생성
    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_event_loop, args=(new_loop,))
    t.start()

    frame_count = 0
    stop_requested = False

    # 창 크기 및 위치 설정
    screen_width = 1920  # 모니터 해상도에 맞게 설정하세요
    screen_height = 1080  # 모니터 해상도에 맞게 설정하세요
    window_name = 'Webcam'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, screen_width, screen_height)

    # 프레임 위치 및 크기 설정
    section_width = screen_width // 3
    frame_width = section_width
    frame_height = screen_height

    # 미리보기 이미지 읽기 (예시: 'image.jpg' 파일)
    image = cv2.imread('image.jpg')
    image = cv2.resize(image, (section_width, screen_height))

    while cap.isOpened() and not stop_requested:
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 크기 조정
        frame = cv2.resize(frame, (frame_width, frame_height))

        # 배경 이미지 생성
        background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

        # 배경 이미지에 프레임 추가 (첫 번째 영역)
        background[0:frame_height, 0:frame_width] = frame

        # 배경 이미지에 텍스트 추가 (두 번째 영역)
        text = "Your text here"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        color = (255, 255, 255)
        thickness = 3
        text_position = (frame_width + 50, screen_height // 2)

        cv2.putText(background, text, text_position, font, font_scale, color, thickness)

        # 배경 이미지에 이미지 추가 (세 번째 영역)
        background[0:frame_height, 2 * frame_width:3 * frame_width] = image

        # 결과를 화면에 표시
        cv2.imshow(window_name, background)

        frame_count += 1
        if frame_count % 30 == 0:
            # 비동기 함수 호출
            call_async_function(new_loop)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_requested = True

    cap.release()
    cv2.destroyAllWindows()

    # 이벤트 루프 중지 요청
    new_loop.call_soon_threadsafe(new_loop.stop)
    t.join()

# 프로그램 실행
if __name__ == "__main__":
    main()
