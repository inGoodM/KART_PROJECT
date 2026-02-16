import streamlit as st
from ui.styles import inject_css

# Импортируем константы из config.py
from config import SLIDER_COLORS, PARAM_CONFIG, PAGES, APP_TITLE, APP_NAME

# ─── НАСТРОЙКА СТРАНИЦЫ ──────────────────────────────────────────────────────

st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Применяем стили из ui/styles.py
inject_css()

# ─── СОСТОЯНИЕ ───────────────────────────────────────────────────────────────

def init_session_state():
    if 'active_page' not in st.session_state:
        st.session_state.active_page = "Обзор и KPI"

    for param in PARAM_CONFIG:
        key = param["key"]
        if key not in st.session_state:
            st.session_state[key] = param.get("default", 0)

def reset_params():
    for param in PARAM_CONFIG:
        st.session_state[param["key"]] = param.get("default", 0)

init_session_state()

# ─── ПАНЕЛЬ ПАРАМЕТРОВ ───────────────────────────────────────────────────────

def render_purchase_parameters():
    with st.container(border=True):
        col_header, col_reset = st.columns([0.9, 0.1])
        with col_header:
            st.markdown("### :material/tune: **Параметры закупки**")
        with col_reset:
            if st.button(":material/refresh: Сброс", key="btn_reset"):
                reset_params()
                st.rerun()

        cols = st.columns(len(PARAM_CONFIG))
        for col, param in zip(cols, PARAM_CONFIG):
            with col:
                kwargs = {
                    "label":      param["label"],
                    "min_value":  param["min"],
                    "max_value":  param["max"],
                    "value":      st.session_state[param["key"]],
                    "key":        param["key"],
                    "format":     param.get("format"),
                }
                if "step" in param:
                    kwargs["step"] = param["step"]

                st.slider(**kwargs)
                st.caption(param["caption"])

# ─── САЙДБАР ─────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown(f"### **{APP_NAME}**")
        st.markdown("---")

        for page_id, cfg in PAGES.items():
            if page_id in ["Контрагенты", "Матрица сезонности"]:
                st.markdown("---")

            is_active = st.session_state.active_page == page_id
            if st.button(
                label = f"{cfg['icon']}  {page_id}",
                use_container_width = True,
                type = "primary" if is_active else "secondary"
            ):
                st.session_state.active_page = page_id
                st.rerun()

        st.markdown("---")

render_sidebar()

# ─── ОСНОВНОЙ КОНТЕНТ ────────────────────────────────────────────────────────

active = st.session_state.active_page
cfg = PAGES.get(active, {})

st.markdown(f"## {active}")
st.caption(cfg.get("caption", ""))

if cfg.get("show_params", False):
    render_purchase_parameters()

# Подключаем страницы из ui/pages
if active == "Обзор и KPI":
    from ui.pages.overview import show_overview_page
    show_overview_page()
elif active == "Товары и прогноз":
    st.info("Детализация по товарам и расчеты (таблицы/графики)")
elif active == "Финансы":
    st.info("Финансовое планирование (cash flow, графики)")
elif active == "Маркетинг":
    st.info("Влияние маркетинга на прогноз")
elif active == "Контрагенты":
    st.info("Управление контрагентами (таблицы, формы)")
elif active == "Матрица сезонности":
    st.info("Матрица сезонности (heatmaps)")
elif active == "Источник данных":
    st.info("Настройка источников (API keys, подключения)")