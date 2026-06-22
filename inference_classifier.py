import sys, types, os

# --- 🚫 Prevent Mediapipe from importing TensorFlow modules ---
fake_tasks = types.ModuleType("mediapipe.tasks")
fake_tasks.python = types.ModuleType("mediapipe.tasks.python")
sys.modules['mediapipe.tasks'] = fake_tasks
sys.modules['mediapipe.tasks.python'] = fake_tasks.python
os.environ["MEDIAPIPE_DISABLE_TF_IMPORT"] = "1"

import pickle
import cv2
import mediapipe as mp
import numpy as np

# --- Load trained Random Forest model ---
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# --- Initialize Mediapipe Hand Tracking ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# --- Label dictionary (A–Z) ---
labels_dict = {i: chr(65 + i) for i in range(26)}

# --- Start webcam ---
win_name = 'ASL Recognition'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)  # create named window once
cap = cv2.VideoCapture(0)  # change index if needed

print("🎥 Webcam started — press 'q' or click the window ❌ to quit")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("⚠️ No frame from camera; exiting.")
            break

        frame = cv2.flip(frame, 1)  # mirror view
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        data_aux = []
        x_, y_ = [], []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    x_.append(lm.x); y_.append(lm.y)

                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min(x_))
                    data_aux.append(lm.y - min(y_))

            if len(data_aux) == 42:
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) + 10
                y2 = int(max(y_) * H) + 10

                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(frame, predicted_character, (x1, y1 - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        cv2.imshow(win_name, frame)

        # --- exit conditions ---
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            print("🛑 'q' pressed, exiting...")
            break

        # if window was closed via the ❌, either VISIBLE becomes 0 or props return -1
        visible = cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE)
        autosize = cv2.getWindowProperty(win_name, cv2.WND_PROP_AUTOSIZE)
        if visible < 1 or autosize < 0:
            print("❌ Window closed manually.")
            break

finally:
    # robust cleanup
    if 'cap' in locals() and cap is not None:
        cap.release()
    try:
        cv2.destroyWindow(win_name)
    except:
        pass
    # flush GUI events on Windows so the window actually disappears
    for _ in range(5):
        cv2.waitKey(1)
    print("👋 Webcam closed.")

