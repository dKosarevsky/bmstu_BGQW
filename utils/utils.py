from PIL import Image, UnidentifiedImageError
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
FILE_TYPES_V = ["mp4", "avi", "mov", "mkv"]
URLS = [
    "https://i.ibb.co/LP1RGH5/download-1.jpg",
    "https://i.ibb.co/qg77xcc/obama.webp"
    "https://i.ibb.co/JdKLwnR/4928.webp"
]


def uploader(file):
    show_file = st.empty()
    if not file:
        show_file.info("valid file extension: " + ", ".join(FILE_TYPES))
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
    video = st.file_uploader("Загрузите видео:", type=FILE_TYPES_V)
    if video:
        st.video(video)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video.read())
        vf = cv2.VideoCapture(temp_file.name)
        st.write(vf)
