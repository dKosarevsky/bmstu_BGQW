import streamlit as st

from utils.utils import (
    upload_video,
    put_video_link,
    upload_image,
    upload_crop,
    extract_multiple_videos_faces,
    is_fake,
    load_model
)


def header():
    st.set_page_config(
        page_title="GAN Deepfake Detection",
        page_icon="https://bmstu.ru/assets/images/favicon/favicon-16x16.png",
        layout="wide",
    )
    # st.set_page_config(initial_sidebar_state="collapsed")
    st.sidebar.image("img/logo.png", width=300)
    st.title("МГТУ им. Баумана")
    st.header("Кафедра ИУ7")
    st.markdown("**Выпускная квалификационная работа бакалавра**")
    st.markdown("**Тема:** Метод определения фальсифицированных видеозаписей с использованием генеративно-состязательных нейронных сетей (GAN Deepfake detection)")
    st.markdown("**Студент:** Дмитрий Петрович Косаревский")
    st.markdown("**Руководитель ВКР:** к.т.н., доцент Игорь Владимирович Рудаков")

    st.sidebar.markdown("# Враг у ворот.")
    st.sidebar.markdown("""
        Кибербезопасность сталкивается с новой угрозой, известной как дипфейки. 
        Злоумышленное использование синтетических видео, созданных искусственным интеллектом, 
        самого мощного кибероружия в истории, не за горами.
    """)
    st.sidebar.markdown("[project repo](https://github.com/dKosarevsky/bmstu_BGQW)")


def main():
    header()

    st.header("Детекция Дипфейка")
    activity = st.radio(
        "Выберите действие:", (
            "1. Загрузка видео.",
            "2. Видео по ссылке.",
            "3. Фото.",
            "4. Обработка фото.",
        ),
        index=0
    )[:1]

    model = load_model()

    if activity == "1":
        video = upload_video()
        if video and st.button("Запустить Детектор"):
            with st.spinner("Обработка ..."):
                extract_multiple_videos_faces(video, model)

    elif activity == "2":
        video_url = put_video_link()

        if video_url and st.button("Проверить Подлинность"):
            with st.spinner("Обработка ..."):
                extract_multiple_videos_faces(video_url, model)

    elif activity == "3":
        with st.spinner("Загрузка ..."):
            img = upload_image()
            if img:
                is_fake(img, model, static=True)

        st.markdown("---")
        st.button("Обновить Изображение")

    elif activity == "4":
        st.subheader("Обрезка Фото:")
        upload_crop()


if __name__ == "__main__":
    main()
