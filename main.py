import streamlit as st

from utils.utils import upload_video, put_video_link, upload_image, upload_crop


def header():
    # st.set_page_config(initial_sidebar_state="collapsed")
    st.sidebar.image('logo.png', width=300)
    st.title("МГТУ им. Баумана")
    st.header("Кафедра ИУ7")
    st.markdown("**Выпускная квалификационная работа бакалавра**")
    st.markdown("**Тема:** Метод определения фальсифицированных видеозаписей с использованием генеративно-состязательных нейронных сетей (GAN Deepfake detection)")
    st.markdown("**Руководитель ВКР:** Рязанова Н.Ю.")
    st.markdown("**Студент:** Косаревский Д.П.")
    st.sidebar.markdown("[project repo](https://github.com/dKosarevsky/bmstu_BGQW)")


def main():
    header()

    st.header("Детекция Видео Дипфейка")
    activity = st.radio(
        "Выберите действие:", (
            "1. Загрузка видео.",
            "2. Видео по ссылке.",
            "3. Обработка фото.",
        ),
        index=0
    )[:1]

    if activity == "1":
        with st.form("video"):
            upload_video()
            st.form_submit_button("Загрузить")

    elif activity == "2":
        with st.form("video"):
            put_video_link()
            st.form_submit_button("Обновить")

    # elif activity == "3":
    #     with st.form("photo"):
    #         gray_image = upload_image()
    #         st.form_submit_button("Обновить")
    #
    #     st.subheader("Обрезать фото:")
    #     upload_crop()


if __name__ == "__main__":
    main()
