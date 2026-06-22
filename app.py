# app.py
import streamlit as st
import streamlit.components.v1 as components

import os
from pathlib import Path

st.set_page_config(page_title="Sign Language Hub", layout="wide", page_icon="🤟")


# =========================================================
# 🌈 GLOBAL THEME & STYLE SETUP
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
    background-color: #0f1218;
    color: #e5e5e5;
}

section.main {
    background: radial-gradient(circle at top left, #11151c, #0b0e13);
    border-radius: 15px;
    padding: 25px;
    box-shadow: inset 0 0 25px rgba(0, 173, 181, 0.1);
}

h1, h2, h3 {
    color: #00ADB5;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.stButton>button {
    background: linear-gradient(90deg, #00ADB5, #007C85);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 10px 25px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #06c4cf, #0199a4);
    box-shadow: 0 0 15px rgba(0,173,181,0.5);
    transform: translateY(-2px);
}

.stTextInput>div>div>input {
    border-radius: 8px;
    border: 1px solid #00adb530;
    background: #1c2129;
    color: #e5e5e5;
}

.stProgress > div > div > div {
    background-color: #00ADB5;
}

.stSidebar {
    background: linear-gradient(180deg, #101318, #0a0c10);
    border-right: 1px solid rgba(255,255,255,0.05);
}
.stSidebar h1, .stSidebar h2, .stSidebar h3 {
    color: #00ADB5;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@keyframes pulseGlow {
    0% { box-shadow: 0 0 15px rgba(0,173,181,0.2); }
    50% { box-shadow: 0 0 25px rgba(0,173,181,0.4); }
    100% { box-shadow: 0 0 15px rgba(0,173,181,0.2); }
}
div[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0b0e13 0%, #161b22 100%);
}
</style>
""", unsafe_allow_html=True)


# ---------------- Session state init ----------------
if "selected_tile" not in st.session_state:
    st.session_state.selected_tile = None
if "page" not in st.session_state:
    st.session_state.page = "Dictionary"  # default page

# =========================================================
# 🧭 MODERN, RELIABLE SIDEBAR NAVIGATION (no JS)
# =========================================================

# 1) Ensure session state is initialized (put near top of file once)
if "page" not in st.session_state:
    st.session_state.page = "Dictionary"

# 2) (Optional) read query param on first load to deep-link pages
qp = st.query_params
if "page" in qp and "_qp_loaded" not in st.session_state:
    val = qp.get("page")
    if isinstance(val, list):
        val = val[0]
    valid = {"Dictionary", "Text to Sign Language", "Emotion Detection", "ASL Gesture Recognition"}
    if val in valid:
        st.session_state.page = val
    st.session_state["_qp_loaded"] = True  # only once

# 3) Sidebar CSS to style radio as glowing tiles
st.markdown("""
<style>
/* Sidebar base */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1218, #161b22);
    border-right: 1px solid rgba(0,173,181,0.25);
    box-shadow: 2px 0 25px rgba(0,173,181,0.05);
    padding-top: 16px;
}

/* Title */
.sidebar-title {
    text-align: center;
    color: #00ADB5;
    font-family: 'Poppins', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin: 6px 0 12px 0;
}

/* Style the radio group to look like cards */
.sidebar-nav .stRadio > div {
    gap: 10px;
}
.sidebar-nav [role="radiogroup"] label {
    width: 100%;
    border-radius: 12px;
    padding: 12px 14px;
    border: 1px solid rgba(0,173,181,0.22);
    background: rgba(255,255,255,0.02);
    color: #e9eef2;
    cursor: pointer;
    transition: all .22s ease;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: inset 0 0 0 rgba(0,173,181,0.0);
}
.sidebar-nav [role="radiogroup"] label:hover {
    transform: translateX(4px);
    border-color: rgba(0,173,181,0.45);
    background: rgba(0,173,181,0.08);
    box-shadow: 0 0 14px rgba(0,173,181,0.12);
}
.sidebar-nav [role="radiogroup"] input {
    display: none; /* hide default radio bullets */
}

/* Active (checked) */
.sidebar-nav [role="radiogroup"] input:checked + div {
    color: #00E0EA !important;
    background: linear-gradient(90deg, rgba(0,173,181,0.28), rgba(0,173,181,0.1));
    border-color: rgba(0,173,181,0.55);
    box-shadow: inset 0 0 18px rgba(0,173,181,0.25);
}

/* Icon span */
.nav-icon {
    font-size: 1.15rem;
    width: 1.6rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 4) Render the sidebar with a styled radio
with st.sidebar:
    st.markdown("<div class='sidebar-title'> Sign Language Hub</div>", unsafe_allow_html=True)
    st.markdown("---")

    options = [
        "Dictionary",
        "Text to Sign Language",
        "Emotion Detection",
        "ASL Gesture Recognition",
    ]
    icons = {
        "Dictionary": "📚",
        "Text to Sign Language": "🗣️",
        "Emotion Detection": "🎭",
        "ASL Gesture Recognition": "✋",
    }

    # Build pretty option labels with icons
    option_labels = [f"{icons[o]}  {o}" for o in options]
    current_index = options.index(st.session_state.page)

    st.markdown("<div class='sidebar-nav'>", unsafe_allow_html=True)
    selected_label = st.radio(
        "Navigation",
        option_labels,
        index=current_index,
        label_visibility="collapsed",
        key="sidebar_nav_radio",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Map back from label to raw page value
    selected_clean = selected_label.split("  ", 1)[1] if "  " in selected_label else selected_label

    # If changed, update state, sync URL, and rerun for instant switch
    if selected_clean != st.session_state.page:
        st.session_state.page = selected_clean
        # (Optional) Sync the URL (?page=...)
        st.query_params.update({"page": selected_clean})
        st.rerun()





# ---------------- Helper functions ----------------
def list_images_in(folder_path, exts=(".jpg", ".jpeg", ".png", ".gif")):
    p = Path(folder_path)
    if not p.exists() or not p.is_dir():
        return []
    files = [str(x) for x in sorted(p.iterdir()) if x.suffix.lower() in exts]
    return files

def show_image_grid(image_paths, captions=None, cols_per_row=5):
    if not image_paths:
        st.info("No images found for this category.")
        return
    cols = st.columns(cols_per_row)
    for i, img in enumerate(image_paths):
        with cols[i % cols_per_row]:
            cap = None
            if captions and i < len(captions):
                cap = captions[i]
            st.image(img, caption=cap, use_container_width=True)

# ---------------- Categories ----------------
categories = {
    "Alphabets": "images/alphabeticon.png",
    "Numbers": "images/numbericon.png",
    "Animals": "images/animalicon.jpg",
    "Emotions": "images/emotionicon.png",
    "Family": "images/familyicon.png",
    "Colors": "images/coloricon.png"
}

# =========================================================
# 🧾 SIGN LANGUAGE DICTIONARY (Full Glow & Polished)
# =========================================================
if st.session_state.page == "Dictionary":

    # ---------- Inject Custom CSS ----------
    st.markdown("""
    <style>
        .dict-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #00ADB5;
            text-align: center;
            margin-bottom: 5px;
        }
        .dict-subtext {
            text-align: center;
            color: #EEEEEE;
            font-size: 1.1rem;
            margin-bottom: 35px;
        }
        .category-card {
            background-color: #222831;
            border-radius: 18px;
            box-shadow: 0 0 15px rgba(0,173,181,0.25);
            transition: all 0.3s ease;
            text-align: center;
            padding: 10px;
        }
        .category-card:hover {
            transform: translateY(-7px);
            box-shadow: 0 0 30px rgba(0,173,181,0.45);
        }
        .category-card img {
            border-radius: 15px;
            object-fit: cover;
            height: 160px;
            width: 100%;
            filter: brightness(85%);
            transition: all 0.3s ease;
        }
        .category-card:hover img {
            filter: brightness(60%) blur(0.5px);
        }
        .category-label {
            color: white;
            background: rgba(0,173,181,0.8);
            border-radius: 10px;
            padding: 5px;
            margin-top: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .back-btn {
            display: inline-block;
            background: #00ADB5;
            color: white;
            font-weight: 600;
            padding: 10px 22px;
            border-radius: 10px;
            margin-top: 25px;
            text-decoration: none;
            transition: 0.3s;
        }
        .back-btn:hover {
            background: #0199a4;
            transform: translateY(-2px);
        }

        /* Inner sign cards */
        .sign-card {
            background-color: #1B1F23;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,173,181,0.2);
            transition: all 0.3s ease;
            text-align: center;
            padding: 10px;
        }
        .sign-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 0 30px rgba(0,173,181,0.45);
        }
        .sign-card img {
            border-radius: 10px;
            height: 130px;
            width: 100%;
            object-fit: cover;
            filter: brightness(90%);
            transition: 0.3s;
        }
        .sign-card:hover img {
            filter: brightness(70%) blur(0.5px);
        }
        .sign-caption {
            margin-top: 8px;
            font-weight: 600;
            color: #EEEEEE;
            font-size: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------- Header ----------
    st.markdown('<div class="dict-title">🧏 Sign Language Dictionary</div>', unsafe_allow_html=True)
    st.markdown('<div class="dict-subtext">Click a category tile to explore signs 👇</div>', unsafe_allow_html=True)

    # ---------- Category Grid ----------
    cols_per_row = 3
    items = list(categories.items())

    for i in range(0, len(items), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, (cat_name, thumb_path) in enumerate(items[i:i + cols_per_row]):
            with cols[j]:
                if os.path.exists(thumb_path):
                    with st.container():
                        st.markdown('<div class="category-card">', unsafe_allow_html=True)
                        st.image(thumb_path, use_container_width=True)
                        st.markdown(f"<div class='category-label'>{cat_name}</div>", unsafe_allow_html=True)
                        if st.button(f"🔍 View {cat_name}", key=f"btn-{cat_name}", use_container_width=True):
                            st.session_state.selected_tile = cat_name
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning(f"Missing image for {cat_name}")

    st.write("---")

    # ---------- Handle Category Selection ----------
    selected = st.session_state.selected_tile
    if selected:
        st.header(f"🔎 {selected} Signs")

        def show_glowing_signs(imgs, captions, cols_per_row=5):
            """Render glowing sign cards instead of static images."""
            for i in range(0, len(imgs), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, img_path in enumerate(imgs[i:i + cols_per_row]):
                    with cols[j]:
                        st.markdown('<div class="sign-card">', unsafe_allow_html=True)
                        st.image(img_path, use_container_width=True)
                        caption = captions[i + j] if captions and i + j < len(captions) else ""
                        st.markdown(f"<div class='sign-caption'>{caption}</div>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

        if selected == "Alphabets":
            alph_folder = Path("images/alphabets")
            imgs, captions = [], []
            for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                for ext in (".jpg", ".jpeg", ".png", ".gif"):
                    candidate = alph_folder / f"{ch}{ext}"
                    if candidate.exists():
                        imgs.append(str(candidate))
                        captions.append(ch)
                        break
            if not imgs:
                st.info("No alphabet images found. Place A.jpg ... Z.jpg inside images/alphabets/")
            else:
                show_glowing_signs(imgs, captions, cols_per_row=5)

        elif selected == "Numbers":
            imgs = list_images_in("images/numbers")
            captions = [Path(p).stem for p in imgs] if imgs else None
            show_glowing_signs(imgs, captions, cols_per_row=6)

        elif selected == "Animals":
            imgs = list_images_in("images/animals")
            captions = [Path(p).stem.replace('_', ' ').title() for p in imgs]
            show_glowing_signs(imgs, captions, cols_per_row=4)

        elif selected == "Emotions":
            imgs = list_images_in("images/emotions")
            captions = [Path(p).stem.replace('_', ' ').title() for p in imgs]
            show_glowing_signs(imgs, captions, cols_per_row=4)

        elif selected == "Family":
            imgs = list_images_in("images/family")
            captions = [Path(p).stem.replace('_', ' ').title() for p in imgs]
            show_glowing_signs(imgs, captions, cols_per_row=4)

        elif selected == "Colors":
            imgs = list_images_in("images/colors")
            captions = [Path(p).stem.replace('_', ' ').title() for p in imgs]
            show_glowing_signs(imgs, captions, cols_per_row=6)

        if st.button("⬅ Back to categories"):
            st.session_state.selected_tile = None
            st.rerun()
    else:
        st.info("No category selected. Click a tile above to view its signs.")


# =========================================================
# ✍️ TEXT → SIGN LANGUAGE MODULE (Full version with manual mic control + animations)
# =========================================================
elif st.session_state.page == "Text to Sign Language":
    st.title("🎤 Text / Voice to Sign Language Converter")
    st.write("Speak or type below — your words will appear in **sign language visuals** 👇")

    import time

    # ✅ Animated Mic Component with Manual Start/Stop
    mic_component = """
    <style>
        #micContainer {
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            margin-bottom: 15px;
        }
        #micBtn {
            background: #00ADB5;
            border: none;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 28px;
            margin: 10px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(0,173,181,0.4);
        }
        #micBtn.listening {
            animation: pulse 1.3s infinite;
            background: #E53935;
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 10px rgba(229,57,53,0.5); }
            50% { transform: scale(1.2); box-shadow: 0 0 25px rgba(229,57,53,0.9); }
            100% { transform: scale(1); box-shadow: 0 0 10px rgba(229,57,53,0.5); }
        }
        #micStatus {
            font-family: sans-serif;
            margin-top: 8px;
            color: #EEEEEE;
            font-size: 16px;
        }
        #stopBtn {
            background: #393E46;
            border: none;
            color: white;
            padding: 10px 20px;
            margin-top: 8px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        #stopBtn:hover { background: #555B66; }
    </style>

    <div id="micContainer">
        <button id="micBtn">🎙️</button>
        <button id="stopBtn">⏹ Stop Listening</button>
        <div id="micStatus">Click mic to start listening</div>
    </div>

    <script>
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const micBtn = document.getElementById("micBtn");
    const stopBtn = document.getElementById("stopBtn");
    const micStatus = document.getElementById("micStatus");
    let recognitionActive = false;
    let recognition;

    if (!SpeechRecognition) {
        micStatus.innerText = "❌ Speech recognition not supported by your browser.";
    } else {
        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.continuous = true;  // ✅ keeps it running until manually stopped

        micBtn.onclick = () => {
            if (!recognitionActive) {
                recognition.start();
                recognitionActive = true;
                micBtn.classList.add("listening");
                micStatus.innerText = "🎧 Listening... Speak now";
            }
        };

        stopBtn.onclick = () => {
            if (recognitionActive) {
                recognition.stop();
                recognitionActive = false;
                micBtn.classList.remove("listening");
                micStatus.innerText = "🛑 Listening stopped manually";
            }
        };

        recognition.onresult = (event) => {
            const text = event.results[event.results.length - 1][0].transcript;
            const params = new URLSearchParams(window.location.search);
            params.set("speech", text);
            window.parent.location.search = params.toString();
            micStatus.innerText = "✅ Recognized: " + text;
        };

        recognition.onerror = (event) => {
            micStatus.innerText = "⚠️ Error: " + event.error;
            micBtn.classList.remove("listening");
            recognitionActive = false;
        };

        recognition.onend = () => {
            if (recognitionActive) {
                recognition.start();  // auto-restart if not manually stopped
            } else {
                micBtn.classList.remove("listening");
            }
        };
    }
    </script>
    """

    components.html(mic_component, height=220)

    # 🔍 Capture recognized text via query params
    query_params = st.query_params
    speech_text = query_params.get("speech", [None])[0]

    if speech_text:
        st.session_state["speech_text"] = speech_text
        st.query_params.clear()
        st.rerun()

    # ✅ User input (manual or from mic)
    user_input = st.text_input("Recognized / Typed Text:", key="speech_text")

    alphabet_folder = Path("images/alphabets")

    # ---------- Convert Text to Sign Images (Now with fade-in effect) ----------
    if user_input:
        st.markdown("### 👇 Sign Language Output")

        # CSS for fade-in and border style
        st.markdown("""
        <style>
        [data-testid="stImage"] img {
            animation: fadeIn 0.6s ease forwards;
            border: 2px solid #00ADB5;
            border-radius: 12px;
            background: #1B1F24;
            padding: 5px;
            margin: 6px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        </style>
        """, unsafe_allow_html=True)

        container = st.container()
        cols = container.columns(10)
        i = 0

        for char in user_input.upper():
            if char == " ":
                with cols[i % 10]:
                    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                i += 1
                continue

            if not char.isalnum():
                continue

            img_path = None
            for ext in (".jpg", ".png", ".jpeg", ".gif"):
                possible = alphabet_folder / f"{char}{ext}"
                if possible.exists():
                    img_path = str(possible)
                    break

            with cols[i % 10]:
                if img_path:
                    st.image(img_path, caption=char, use_container_width=True)
                else:
                    st.warning(f"{char}?")

            i += 1
            if i % 10 == 0:
                cols = container.columns(10)



# =========================================================
# 🎭 EMOTION DETECTION MODULE — Clean, Glowing, and with Green Face Box
# =========================================================
elif st.session_state.page == "Emotion Detection":
    import cv2
    import numpy as np
    import time
    from tensorflow.keras.models import model_from_json
    from PIL import Image

    # ---------------------- CSS ----------------------
    st.markdown("""
    <style>
    .emotion-header {
        text-align: center;
        font-size: 2rem;
        color: #00E0EA;
        text-shadow: 0 0 12px rgba(0,173,181,0.8);
        margin-bottom: 1rem;
    }
    .mode-box {
        background: linear-gradient(145deg, rgba(0,173,181,0.15), rgba(255,255,255,0.05));
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 15px rgba(0,173,181,0.08);
    }
    .camera-frame {
        border-radius: 15px;
        border: 2px solid rgba(0,173,181,0.4);
        box-shadow: 0 0 20px rgba(0,173,181,0.3);
        overflow: hidden;
    }
    .emotion-card {
        text-align: center;
        padding: 20px 25px;
        border-radius: 12px;
        margin-top: 1.5rem;
        background: rgba(15, 20, 25, 0.7);
        box-shadow: 0 0 20px rgba(0,173,181,0.25);
        animation: pulseGlow 3s infinite;
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(0,173,181,0.25); }
        50% { box-shadow: 0 0 25px rgba(0,173,181,0.5); }
        100% { box-shadow: 0 0 10px rgba(0,173,181,0.25); }
    }
    .emoji {
        font-size: 3.5rem;
        line-height: 1.2;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='emotion-header'>🎭 Emotion Detection Hub</div>", unsafe_allow_html=True)
    st.write("Choose between **Real-time** or **Snapshot** mode to recognize your emotions visually and interactively!")

    # ---------------------- Load Model ----------------------
    @st.cache_resource
    def load_emotion_model():
        with open("model_fer.json", "r") as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json)
        model.load_weights("model_fer.weights.h5")
        return model

    model = load_emotion_model()
    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    emoji_map = {
        'Angry': '😠',
        'Disgust': '🤢',
        'Fear': '😨',
        'Happy': '😄',
        'Sad': '😢',
        'Surprise': '😲',
        'Neutral': '😐'
    }

    # ---------------------- Mode Selection ----------------------
    st.markdown("<div class='mode-box'>", unsafe_allow_html=True)
    mode = st.radio("🎥 Select Mode", ["Real-Time Detection", "Snapshot Detection"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------- REAL-TIME MODE ----------------------
    if mode == "Real-Time Detection":
        st.subheader("🟢 Live Emotion Recognition")
        st.write("Click **Start Camera** to begin real-time facial emotion tracking.")

        start = st.button("▶ Start Camera", use_container_width=True)
        stop = st.button("⏹ Stop Camera", use_container_width=True)

        FRAME_WINDOW = st.empty()
        RESULT_CARD = st.empty()

        if start and not stop:
            cap = cv2.VideoCapture(0)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.warning("Unable to access webcam.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.resize(gray, (48, 48))
                gray = gray / 255.0
                gray = np.expand_dims(np.expand_dims(gray, -1), 0)

                preds = model.predict(gray, verbose=0)[0]
                emotion = emotions[np.argmax(preds)]
                emoji = emoji_map[emotion]

                # Show emotion label on frame
                cv2.putText(frame, emotion, (30, 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 255), 3)
                FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)

                # Glowing card below
                RESULT_CARD.markdown(
                    f"""
                    <div class='emotion-card'>
                        <div class='emoji'>{emoji}</div>
                        <h3>{emotion}</h3>
                    </div>
                    """, unsafe_allow_html=True
                )

                if stop:
                    break
                time.sleep(0.1)

            cap.release()
            cv2.destroyAllWindows()
            st.success("✅ Camera stopped successfully.")

        else:
            st.info("Click **Start Camera** to begin real-time emotion recognition.")

    # ---------------------- SNAPSHOT MODE (with Green Box) ----------------------
    elif mode == "Snapshot Detection":
        st.subheader("📸 Single Image Emotion Recognition")
        st.write("Capture a photo to detect your current emotion instantly!")

        frame = st.camera_input("Take a Picture")

        if frame is not None:
            img = Image.open(frame)
            img = np.array(img.convert('RGB'))

            # Load Haar Cascade for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(48, 48))

            # Prepare default (in case no face is found)
            gray_resized = cv2.resize(gray, (48, 48))
            gray_resized = gray_resized / 255.0
            gray_resized = np.expand_dims(np.expand_dims(gray_resized, -1), 0)

            emotion = "Neutral"
            emoji = "😐"

            if len(faces) > 0:
                # Pick the largest detected face
                (x, y, w, h) = sorted(faces, key=lambda b: b[2] * b[3], reverse=True)[0]
                face_crop = gray[y:y + h, x:x + w]
                face_crop = cv2.resize(face_crop, (48, 48))
                face_crop = face_crop / 255.0
                face_crop = np.expand_dims(np.expand_dims(face_crop, -1), 0)

                preds = model.predict(face_crop)[0]
                emotion = emotions[np.argmax(preds)]
                emoji = emoji_map[emotion]

                # Draw green box around detected face
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(img, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                # Predict using entire image if no face found
                preds = model.predict(gray_resized)[0]
                emotion = emotions[np.argmax(preds)]
                emoji = emoji_map[emotion]

            # Emotion card
            st.markdown(
                f"""
                <div class='emotion-card'>
                    <div class='emoji'>{emoji}</div>
                    <h3>{emotion}</h3>
                </div>
                """, unsafe_allow_html=True
            )

            # Display image with bounding box
            st.image(img, caption=f"{emoji} Predicted: {emotion}", use_container_width=True)




# =========================================================
# =========================================================
# 🤟 ASL GESTURE RECOGNITION MODULE — Premium Glowing UI (Real-Time + Snapshot)
# =========================================================
elif st.session_state.page == "ASL Gesture Recognition":
    import cv2
    import mediapipe as mp
    import numpy as np
    import pickle
    import time
    from PIL import Image

    # ---------------------- CSS ----------------------
    st.markdown("""
    <style>
    .asl-header {
        text-align: center;
        font-size: 2rem;
        color: #00E0EA;
        text-shadow: 0 0 12px rgba(0,173,181,0.8);
        margin-bottom: 1rem;
    }
    .mode-box {
        background: linear-gradient(145deg, rgba(0,173,181,0.15), rgba(255,255,255,0.05));
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 15px rgba(0,173,181,0.08);
    }
    .camera-frame {
        border-radius: 15px;
        border: 2px solid rgba(0,173,181,0.4);
        box-shadow: 0 0 25px rgba(0,173,181,0.3);
        overflow: hidden;
    }
    .result-card {
        text-align: center;
        padding: 20px 30px;
        border-radius: 12px;
        margin-top: 1.5rem;
        background: rgba(15, 20, 25, 0.7);
        box-shadow: 0 0 25px rgba(0,173,181,0.3);
        animation: pulseGlow 3s infinite;
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(0,173,181,0.25); }
        50% { box-shadow: 0 0 25px rgba(0,173,181,0.55); }
        100% { box-shadow: 0 0 10px rgba(0,173,181,0.25); }
    }
    .gesture-icon {
        font-size: 3.5rem;
        line-height: 1.3;
        color: #00E0EA;
    }
    .gesture-letter {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------------- Header ----------------------
    st.markdown("<div class='asl-header'>🤟 ASL Gesture Recognition Hub</div>", unsafe_allow_html=True)
    st.write("Use **Real-time** mode for continuous recognition or **Snapshot** mode for single-frame predictions.")

    # ---------------------- Load Model ----------------------
    @st.cache_resource
    def load_asl_model():
        model_dict = pickle.load(open("model.p", "rb"))
        return model_dict["model"]

    model = load_asl_model()
    labels_dict = {i: chr(65 + i) for i in range(26)}

    # ---------------------- Mediapipe Setup ----------------------
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    # ---------------------- Mode Selection ----------------------
    st.markdown("<div class='mode-box'>", unsafe_allow_html=True)
    mode = st.radio("✋ Select Mode", ["Real-Time Recognition", "Snapshot Recognition"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------------
    # 🟢 REAL-TIME MODE
    # -------------------------------------------------
    if mode == "Real-Time Recognition":
        st.subheader("🟢 Live Hand Gesture Recognition")
        st.write("Click **Start Camera** to begin continuous gesture detection.")

        start = st.button("▶ Start Camera", use_container_width=True)
        stop = st.button("⏹ Stop Camera", use_container_width=True)

        FRAME_WINDOW = st.empty()
        RESULT_CARD = st.empty()

        if start and not stop:
            cap = cv2.VideoCapture(0)

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.warning("Unable to access webcam.")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                data_aux, x_, y_ = [], [], []
                predicted_char = None

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for lm in hand_landmarks.landmark:
                            x_.append(lm.x)
                            y_.append(lm.y)
                        for lm in hand_landmarks.landmark:
                            data_aux.append(lm.x - min(x_))
                            data_aux.append(lm.y - min(y_))

                        # Draw landmarks
                        mp_drawing.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0,255,255), thickness=2, circle_radius=2),
                            mp_drawing.DrawingSpec(color=(0,150,255), thickness=2)
                        )

                    # Predict gesture if valid
                    if len(data_aux) == 42:
                        prediction = model.predict([np.asarray(data_aux)])
                        predicted_char = labels_dict[int(prediction[0])]

                        # Display letter on video
                        cv2.putText(frame, predicted_char, (30, 70),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4, cv2.LINE_AA)

                # Show camera feed
                FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)

                # Show glowing result card
                if predicted_char:
                    RESULT_CARD.markdown(
                        f"""
                        <div class='result-card'>
                            <div class='gesture-icon'>🧠</div>
                            <div class='gesture-letter'>{predicted_char}</div>
                            <p style='color:#aaa; font-size:0.9rem;'>Detected Sign</p>
                        </div>
                        """, unsafe_allow_html=True
                    )

                if stop:
                    break
                time.sleep(0.08)

            cap.release()
            cv2.destroyAllWindows()
            st.success("✅ Camera stopped successfully.")
        else:
            st.info("Click **Start Camera** to begin real-time recognition.")

    # -------------------------------------------------
    # 🟣 SNAPSHOT MODE
    # -------------------------------------------------
    elif mode == "Snapshot Recognition":
        st.subheader("📸 Single Frame Recognition")
        st.write("Capture a hand sign once to recognize it instantly!")

        img_file = st.camera_input("Show your ASL sign")

        if img_file is not None:
            img = Image.open(img_file)
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            data_aux, x_, y_ = [], [], []
            predicted_char = None

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for lm in hand_landmarks.landmark:
                        x_.append(lm.x)
                        y_.append(lm.y)
                    for lm in hand_landmarks.landmark:
                        data_aux.append(lm.x - min(x_))
                        data_aux.append(lm.y - min(y_))

                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if len(data_aux) == 42:
                    prediction = model.predict([np.asarray(data_aux)])
                    predicted_char = labels_dict[int(prediction[0])]

                    st.markdown(
                        f"""
                        <div class='result-card'>
                            <div class='gesture-letter'>{predicted_char}</div>
                            <p style='color:#aaa; font-size:0.9rem;'>Detected Sign</p>
                        </div>
                        """, unsafe_allow_html=True
                    )

            st.image(frame, caption="Detected Hand Landmarks", channels="BGR", use_container_width=True)
