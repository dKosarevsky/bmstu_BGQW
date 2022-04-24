import streamlit as st

from utils.utils import upload_video, upload_image



def header():
    # st.set_page_config(initial_sidebar_state="collapsed")
    st.sidebar.image('logo.png', width=300)
    st.header("МГТУ им. Баумана. Кафедра ИУ7")
    st.markdown("**Выпускная квалификационная работа бакалавра**")
    st.markdown("**Тема:** Метод определения фальсифицированных видеозаписей с использованием генеративно-состязательных нейронных сетей. (GAN Deepfake detection)")
    st.markdown("**Руководитель ВКР:** Рязанова Н.Ю.")
    st.markdown("**Студент:** Косаревский Д.П.")
    st.sidebar.markdown("[project repo](https://github.com/dKosarevsky/bmstu_BGQW)")


def main():
    header()

    activity = st.radio(
        "Выберите действие:", (
            "1. Детекция видео.",
            "2. Детекция фото.",
        ),
        index=0
    )[:1]

    if activity == "1":
        with st.form("video"):
            upload_video()
            st.form_submit_button("Загрузить")

    elif activity == "2":
        with st.form("photo"):
            gray_image = upload_image()
            st.form_submit_button("Обновить")


if __name__ == "__main__":
    main()

