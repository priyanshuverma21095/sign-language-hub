from streamlit_webrtc import webrtc_streamer
import av

def callback(frame):
    return frame

webrtc_streamer(key="test", video_frame_callback=callback)
