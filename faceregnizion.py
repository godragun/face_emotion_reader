
import cv2
import numpy as np
import urllib.request
from deepface import DeepFace

# === CONFIGURATION ===
USE_ESP32_CAM = False  # Change to True to use ESP32-CAM instead of laptop camera
ESP32_CAM_URL = 'http://192.168.196.131/capture'  # Change IP as needed

# === INITIALIZE CAMERA ===
if not USE_ESP32_CAM:
    cap = cv2.VideoCapture(0)

while True:
    if USE_ESP32_CAM:
        try:
            img_resp = urllib.request.urlopen(ESP32_CAM_URL)
            img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_np, -1)
        except:
            print("Failed to fetch from ESP32-CAM.")
            continue
    else:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access laptop camera.")
            break

    frame = cv2.flip(frame, 1)
    try:
        # Analyze emotions
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # Get bounding box and emotion label
        dominant_emotion = result[0]['dominant_emotion']
        region = result[0]['region']
        x, y, w, h = region['x'], region['y'], region['w'], region['h']

        # Draw rectangle and emotion text
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(frame, dominant_emotion.capitalize(), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    except Exception as e:
        print("Detection error:", e)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if not USE_ESP32_CAM:
    cap.release()
cv2.destroyAllWindows()
