import streamlit as st

from utils.utils import upload_video, put_video_link, upload_image, upload_crop, extract_multiple_videos_faces


def header():
    st.set_page_config(
        page_title="GAN Deepfake Detection",
        page_icon="https://bmstu.ru/assets/images/favicon/favicon-16x16.png",
        layout="wide",
    )
    # st.set_page_config(initial_sidebar_state="collapsed")
    st.sidebar.image('logo.png', width=300)
    st.title("МГТУ им. Баумана")
    st.header("Кафедра ИУ7")
    st.markdown("**Выпускная квалификационная работа бакалавра**")
    st.markdown("**Тема:** Метод определения фальсифицированных видеозаписей с использованием генеративно-состязательных нейронных сетей (GAN Deepfake detection)")
    st.markdown("**Руководитель ВКР:** Рязанова Н.Ю.")
    st.markdown("**Студент:** Косаревский Д.П.")

    st.sidebar.markdown("# Враг у ворот.")
    st.sidebar.markdown("""
        Кибербезопасность сталкивается с новой угрозой, известной как дипфейки. 
        Злоумышленное использование синтетических видео, созданных искусственным интеллектом, 
        самого мощного кибероружия в истории не за горами.
    """)
    st.sidebar.markdown("[project repo](https://github.com/dKosarevsky/bmstu_BGQW)")


def main():
    header()

    st.header("Детекция Видео Дипфейка")
    activity = st.radio(
        "Выберите действие:", (
            "1. Загрузка видео.",
            "2. Видео по ссылке.",
            # "3. Обработка фото.",
        ),
        index=0
    )[:1]

    if activity == "1":
        with st.form("video"):
            video = upload_video()
            if video:
                extract_multiple_videos_faces(video)
            st.form_submit_button("Загрузить")

    elif activity == "2":
        # with st.form("video"):
        video_url = put_video_link()
        if video_url:
            extract_multiple_videos_faces(video_url)
            # st.form_submit_button("Обновить")

    # elif activity == "3":
    #     with st.form("photo"):
    #         gray_image = upload_image()
    #         st.form_submit_button("Обновить")
    #
    #     st.subheader("Обрезать фото:")
    #     upload_crop()


if __name__ == "__main__":
    main()
