    # 창 크기 및 위치 설정
    screen_width = 1920  # 모니터 해상도에 맞게 설정하세요
    screen_height = 1080  # 모니터 해상도에 맞게 설정하세요
    window_name = 'Webcam'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, screen_width // 2, screen_height)
    cv2.moveWindow(window_name, 0, 0)