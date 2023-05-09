from pathlib import Path
import streamlit as st
from ultralytics import YOLO
import settings
import helper

st.set_page_config(
    page_title='Object Tracking using YOLOv8',
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('Object Tracking using YOLOv8')

st.sidebar.header('ML Model Config')

model_type = st.sidebar.radio(
    'Select Task', ['Detection', 'Segmentation']
)
confidence = float(st.sidebar.slider(
    'Select Model Confidence', 25, 100, 40)) / 100


if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTION_MODEL)
    
try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)
    
st.sidebar.header('Image/Video Config')
soruce_radio = st.sidebar.radio(
    'Select Source', settings.SOURCES_LIST
)

if soruce_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)
elif soruce_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)
else:
    st.error('Please select a valid source type!')