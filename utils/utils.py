from PIL import Image, UnidentifiedImageError
from streamlit_cropper import st_cropper
from urllib.parse import urlparse
from random import choice
from io import BytesIO

import streamlit as st
import numpy as np
import requests
import tempfile
import cv2
import os

FILE_TYPES = ["png", "bmp", "jpg", "jpeg"]
FILE_TYPES_V = ["mp4", "avi", "mov", "ogv", "m4v", "webm"]
URLS = [
    "https://i.ibb.co/LP1RGH5/download-1.jpg",
    "https://i.ibb.co/qg77xcc/obama.webp",
    "https://i.ibb.co/JdKLwnR/4928.webp",
]
URLS_V = [
    "https://www.youtube.com/watch?v=eseGwoxiqNs",
    "https://www.youtube.com/watch?v=wrHXA2cSpNU",
    "https://www.youtube.com/watch?v=oxXpB9pSETo",
    "https://www.youtube.com/watch?v=cQ54GDm1eL0",
]


def upload_crop():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    img_file = st.file_uploader(label='Загрузите файл:', type=FILE_TYPES)
    realtime_update = st.checkbox(label="Обновлять в Реальном Времени", value=True)
    box_color = st.color_picker(label="Цвет Окна", value='#0000FF')
    aspect_choice = st.radio(label="Выберите Соотношение Сторон:", options=["1:1", "16:9", "4:3", "2:3", "Свободное"])
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    aspect_ratio = aspect_dict[aspect_choice]

    if img_file:
        img = Image.open(img_file)
        if not realtime_update:
            st.write("Дабл-клик для обновления")
        cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color, aspect_ratio=aspect_ratio)

        st.write("Предпросмотр")
        _ = cropped_img.thumbnail((640, 640))
        st.image(cropped_img)


def uploader(file):
    show_file = st.empty()
    if not file:
        show_file.info("допустимые расширения: " + ", ".join(FILE_TYPES))
        return False
    return file


def validate_url(url):
    result = urlparse(url)
    if all([result.scheme, result.netloc]):
        return url
    else:
        st.error("Не похоже на ссылку с изображением, повторите ввод.")
        st.stop()


def get_image(user_img, user_url):
    img = None
    if user_img is not False:
        img = Image.open(user_img)
    else:
        response = requests.get(user_url)
        try:
            img = Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            st.error("Что-то пошло не так... Попробуйте другую ссылку или загрузите изображение со своего устройства.")
            st.stop()

    arr = np.uint8(img)
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

    c1, c2 = st.columns(2)
    with c1:
        st.write("Исходное изображение:")
        st.image(img, width=300)

    with c2:
        st.write("Оттенки серого:")
        st.image(gray, width=300)

    return img, gray


def upload_image():
    user_img = uploader(st.file_uploader("Загрузите изображение:", type=FILE_TYPES))

    user_url = validate_url(st.text_input(f"Ссылка на изображение {FILE_TYPES}: ", choice(URLS)))
    _, gray_image = get_image(user_img, user_url)
    return gray_image


def upload_video():
    video = st.file_uploader("Загрузите видео с локального устройства:", type=FILE_TYPES_V)
    if video:
        st.video(video)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video.read())
        vf = cv2.VideoCapture(temp_file.name)
        st.write(vf)


def put_video_link():
    st.write("Допустимы различные ссылки, поддерживаемые HTML5, включая YouTube.")

    video_url = validate_url(st.text_input(f"Ссылка на изображение {FILE_TYPES_V}: ", choice(URLS_V)))
    st.video(video_url)
