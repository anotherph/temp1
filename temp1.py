import cv2
import asyncio
import threading

# 비동기 함수 a 정의
async def async_function_a():
    print("Function a is called.")
    # await asyncio.sleep(0)  # 실제 비동기 작업이 있을 때 대체

    await asyncio.sleep(5)  # 1초 동안 대기
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

    # while cap.isOpened() and not stop_requested:
    while not stop_requested:
        # print(stop_requested)
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Webcam', frame)

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
