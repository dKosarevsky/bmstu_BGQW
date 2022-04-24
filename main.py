import streamlit as st

# st.set_page_config(initial_sidebar_state="collapsed")
st.sidebar.image('logo.png', width=300)


def header():
    st.header("МГТУ им. Баумана. Кафедра ИУ7")
    st.markdown("**Выпускная квалификационная работа бакалавра**")
    st.markdown("**Тема:** Метод определения фальсифицированных видеозаписей с использованием генеративно-состязательных нейронных сетей. (GAN Deepfake detection)")
    st.markdown("**Руководитель ВКР:** Рязанова Н.Ю.")
    st.markdown("**Студент:** Косаревский Д.П.")
    st.sidebar.markdown("[project repo](https://github.com/dKosarevsky/bmstu_BGQW)")


def main():
    activity = st.sidebar.radio(
        "Выберите действие:", (
            "1. ___.",
            "2. ___.",
            "3. ___.",
        ),
        index=0
    )[:1]
    header()

    if activity == "1":
        st.write(1)

    elif activity == "2":
        st.write(2)

    elif activity == "3":
        st.write(3)


if __name__ == "__main__":
    main()

