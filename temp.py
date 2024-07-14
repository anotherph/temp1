import cv2
import asyncio
import threading

# 비동기 함수 a 정의
async def async_function_a():
    print("Function a is called.")
    await asyncio.sleep(0)  # 실제 비동기 작업이 있을 때 대체

# 비동기 함수 호출을 위한 래퍼
def run_async_function_a(loop):
    asyncio.run_coroutine_threadsafe(async_function_a(), loop)

# 메인 함수 정의
def main():
    # OpenCV 웹캠 초기화
    cap = cv2.VideoCapture(0)

    # 이벤트 루프 가져오기
    loop = asyncio.get_event_loop()

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Webcam', frame)

        frame_count += 1
        if frame_count % 30 == 0:
            # 비동기 함수 호출을 위한 쓰레딩 사용
            threading.Thread(target=run_async_function_a, args=(loop,)).start()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 프로그램 실행
if __name__ == "__main__":
    main()
