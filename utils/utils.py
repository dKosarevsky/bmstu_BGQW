import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import requests
import tempfile
import keras
import glob
import pafy
import cv2
import os

from PIL import Image, UnidentifiedImageError
from streamlit_cropper import st_cropper
from urllib.parse import urlparse
from skimage import transform
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
from matplotlib.patches import Rectangle, Circle
from random import choice, randint
from io import BytesIO
from numpy import asarray


FILE_TYPES = ["png", "bmp", "jpg", "jpeg"]
FILE_TYPES_V = ["mp4", "avi", "m4v", "webm"]
URLS = [
    "https://thispersondoesnotexist.com/image",
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

    st.image(img, width=600)

    return img


def gen_fake_image_url():
    fake_image_url = "https://this-person-does-not-exist.com/"
    image_url_0 = f"{fake_image_url}img/{requests.get(fake_image_url + 'en?new').json().get('name')}"
    image_url_1 = f"https://boredhumans.b-cdn.net/faces2/{randint(1, 994)}.jpg"
    image_url_2 = f"https://boredhumans.b-cdn.net/faces/{randint(1, 5785)}.jpg"
    return [image_url_0, image_url_1, image_url_2]


def upload_image():
    user_img = uploader(st.file_uploader("Загрузите изображение:", type=FILE_TYPES))

    user_url = validate_url(st.text_input(f"Ссылка на изображение {FILE_TYPES}: ", choice(URLS + gen_fake_image_url())))
    return get_image(user_img, user_url)


def upload_video():
    video = uploader(st.file_uploader("Загрузите видео с локального устройства:", type=FILE_TYPES_V), type_="video")
    if video:
        st.video(video)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video.read())
        return temp_file.name


def put_video_link():
    # video_url = validate_url(st.text_input(f"Ссылка на Видео {FILE_TYPES_V}: ", choice(URLS_V)))
    video_url = validate_url(st.text_input(f"Ссылка на Видео {FILE_TYPES_V}: ", "https://www.youtube.com/watch?v=cQ54GDm1eL0"))
    st.video(video_url)

    video = pafy.new(video_url)
    best = video.getbest(preftype="mp4")
    return best.url


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
    # st.image(face_filename)


def clear_dir(path):
    files_c = glob.glob(f"{path}/cropped/*")
    files_f = glob.glob(f"{path}/only_face/*")
    files = files_c + files_f
    for f in files:
        os.remove(f)


@st.cache(allow_output_mutation=True, ttl=3600)
def load_model():
    return keras.models.load_model("models/model.h5")


def transform_detect(image, model):
    np_image = np.array(image).astype('float32') / 255
    np_image = transform.resize(np_image, (224, 224, 3))
    np_image = np.expand_dims(np_image, axis=0)

    return model.predict(np_image)[0][0]


def is_fake(image, model, static=False):
    probability = transform_detect(image, model)

    if static:
        st.code(f"Вероятность того, что образ настоящий, равна: {probability:.5f}")

        if probability < 0.1:
            st.error("Крайне высокая вероятность того, что перед Вами дипфейк")

        elif probability < 0.5:
            st.warning("Высокая вероятность того, перед Вами дипфейк")

        else:
            st.write("Cкорее всего образ настоящий, однако не стоит доверять всему, что вы видите в Интернете.")
    else:
        return probability


def show_face_with_bb(frame):
    face_detector = MTCNN()
    faces = face_detector.detect_faces(frame)
    if faces:
        fig = plt.figure()
        data = asarray(frame)
        plt.axis("off")
        plt.imshow(data)
        ax = plt.gca()
        for face in faces:
            x, y, width, height = face['box']
            rect = Rectangle((x, y), width, height, fill=False, color='maroon')
            ax.add_patch(rect)
            for _, value in face['keypoints'].items():
                dot = Circle(value, radius=2, color='maroon')
                ax.add_patch(dot)
        st.pyplot(fig)


def extract_multiple_videos_faces(data, model):
    cap = cv2.VideoCapture(data)
    if not cap.isOpened():
        st.error("Ошибка Открытия Видеопотока или Файла")
        st.stop()
    while True:
        ret, frame = cap.read()
        if ret:
            proba = is_fake(frame, model)
            if proba < 0.5:
                st.code(f"Вероятность того, что видео настоящее, равна: {proba:.5f}")
                # st.image(frame)
                show_face_with_bb(frame)
                st.error("Высокая вероятность того, что перед Вами дипфейк")
                st.stop()
        else:
            break
    cv2.waitKey(50)  # 50msec (for debugging)
    cap.release()
    cv2.destroyAllWindows()
    st.write("Cкорее всего образ настоящий, однако не стоит доверять всему, что Вы видите в Интернете.")
