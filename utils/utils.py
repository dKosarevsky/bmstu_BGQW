import streamlit as st
import numpy as np
import requests
import pathlib
import tempfile
import glob
import pafy
import cv2
import os

from PIL import Image, UnidentifiedImageError
from streamlit_cropper import st_cropper
from urllib.parse import urlparse
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
from random import choice
from io import BytesIO


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


def uploader(file, type_="foto"):
    show_file = st.empty()
    if not file:
        show_file.info("допустимые расширения: " + ", ".join(FILE_TYPES_V if type_ == "video" else FILE_TYPES))
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
    video = uploader(st.file_uploader("Загрузите видео с локального устройства:", type=FILE_TYPES_V), type_="video")
    if video:
        st.video(video)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video.read())
        return temp_file.name


def put_video_link():
    st.write("Допустимы различные ссылки, поддерживаемые HTML5, включая YouTube.")

    video_url = validate_url(st.text_input(f"Ссылка на изображение {FILE_TYPES_V}: ", choice(URLS_V)))
    st.video(video_url)

    video = pafy.new(video_url)
    best = video.getbest(preftype="mp4")
    return best.url  # TODO add None handler


def draw_image_with_boxes(filename, result_list, face_filename):
    data = pyplot.imread(filename)
    for i in range(len(result_list)):
        x1, y1, width, height = result_list[i]["box"]
        x2, y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(result_list), i+1)
        pyplot.axis("off")
        pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.savefig(face_filename)
    pyplot.show()
    st.image(face_filename)


def clear_dir(path):
    files_c = glob.glob(f"{path}/cropped/*")
    files_f = glob.glob(f"{path}/only_face/*")
    files = files_c + files_f
    for f in files:
        os.remove(f)


def extract_multiple_videos_faces(filenames):
    i = 1
    cap = cv2.VideoCapture(filenames)
    if not cap.isOpened():
        st.error("Ошибка Открытия Видеопотока или Файла")

    path = os.path.join(pathlib.Path().resolve(), "images")
    clear_dir(path)
    fmt = ".jpg"
    while True:
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(os.path.join(path, "cropped", str(i) + fmt), frame)
            filename = os.path.join(path, "cropped", str(i) + fmt)

            pixels = pyplot.imread(filename)
            detector = MTCNN()
            faces = detector.detect_faces(pixels)
            face_filename_crp = os.path.join(path, "only_face", str(i) + fmt)
            draw_image_with_boxes(filename, faces, face_filename_crp)

            i += 1

        else:
            break
    cv2.waitKey(50)  # 50msec (for debugging)
    cap.release()
    cv2.destroyAllWindows()
