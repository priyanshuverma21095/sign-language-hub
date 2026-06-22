import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageTk
import tkinter as tk

# ---------------------------
# 1️⃣ Load Model
# ---------------------------
print("Loading model...")
with open("model_fer.json", "r") as json_file:
    model_json = json_file.read()

model = model_from_json(model_json)
model.load_weights("model_fer.weights.h5")
print("✅ Model loaded successfully!")

# ---------------------------
# 2️⃣ Load Haar Cascade
# ---------------------------
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# ---------------------------
# 3️⃣ Emotion Detection Logic
# ---------------------------
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def detect_emotions():
    ret, frame = cap.read()
    if not ret:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        img_pixels = image.img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255.0

        predictions = model.predict(img_pixels)
        max_index = int(np.argmax(predictions[0]))
        predicted_emotion = emotions[max_index]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, predicted_emotion, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Convert frame for Tkinter display
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    video_label.after(10, detect_emotions)

# ---------------------------
# 4️⃣ Tkinter GUI Setup
# ---------------------------
window = tk.Tk()
window.title("Real-Time Emotion Detection")
window.geometry("900x700")

video_label = tk.Label(window)
video_label.pack()

close_button = tk.Button(window, text="Close", command=window.destroy)
close_button.pack()

cap = cv2.VideoCapture(0)
detect_emotions()
window.mainloop()

cap.release()
cv2.destroyAllWindows()
