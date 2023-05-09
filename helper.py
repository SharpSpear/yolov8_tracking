import cv2
import streamlit as st
import pafy
import settings

def display_tracker_options():
    display_tracker = st.radio('Display Tracker', ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio('Tracker', ('bytetrack.yaml', 'botsort.yaml'))
        return is_display_tracker, tracker_type
    return is_display_tracker, None

def _display_detected_frames(conf, model, st_frame, image, is_display_tracking, tracker):
    image = cv2.resize(image, (720, int(720*9/16)))
    if is_display_tracking:
        res = model.track(image, conf=conf, tracker=tracker)
    else:
        res = model.predict(image, conf=conf)
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                    caption='Detected Video',
                    channels='BGR',
                    use_column_width=True)

def play_stored_video(conf, model):
    source_vid = st.sidebar.selectbox('Choose a video...', settings.VIDEO_DICT.keys())
    is_display_tracker, tracker = display_tracker_options()
    with open(settings.VIDEO_DICT.get(source_vid), 'rb') as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)
    if st.sidebar.button('Detect Video Objects'):
        try:
            vid_cap = cv2.VideoCapture(str(settings.VIDEO_DICT.get(source_vid)))
            st_frame = st.empty()
            while(vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, is_display_tracker, tracker)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error('Error loading video: ' + str(e))

def play_youtube_video(conf, model):
    source_youtube = st.sidebar.text_input('YouTube Video URL')
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            video = pafy.new(source_youtube)
            best = video.getbest(preftype='mp4')
            vid_cap = cv2.VideoCapture(best.url)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, is_display_tracker, tracker)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error('Error loading video: ' + str(e))