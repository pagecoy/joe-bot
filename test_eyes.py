import cv2

def test_camera():
    # 0 is usually the default camera. I have 1 because I used a webcam and my 0 was an inexistent camera
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Joe cannot open his eyes. Check cap variable and change the VideoCapture to 0")
        return

    print("Joe's eyes are opening... Press 'Q' to close them.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Vision Test', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()