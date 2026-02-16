# ui/styles.py
import streamlit as st
from config import SLIDER_COLORS, PARAM_CONFIG

def inject_css():
    """
    Применяет кастомные стили для слайдеров, кнопок и меток.
    Убирает красный цвет прогресс-бара, оставляет разноцветные точки.
    """
    css = """
    <style>
    /* 1. Дорожка (незаполненная часть) — серый */
    div[data-baseweb="slider"] > div[aria-hidden="true"] {
        background-color: #dee2e6 !important;
        background-image: none !important;
    }

    /* 2. Заполненная часть (progress bar) — полностью прозрачная → убираем красный навсегда */
    div[data-baseweb="slider"] [aria-valuenow] > div,
    div[data-baseweb="slider"] [aria-valuenow] > div > div,
    div[data-baseweb="slider"] [role="slider"] ~ div > div > div,
    div[data-baseweb="slider"] [aria-valuenow] > div:first-child {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* 3. Разноцветные точки (thumbs) — цвета по порядку параметров */
    """

    for i, param in enumerate(PARAM_CONFIG):
        key = param["key"]
        color = SLIDER_COLORS[i % len(SLIDER_COLORS)]
        css += f"""
    .st-key-{key} [role="slider"] {{
        background-color: {color} !important;
        border: 2px solid {color} !important;
        box-shadow: 0 0 0 3px {color}33 !important;
        outline: none !important;
    }}
        """

    css += """
    /* 4. Метки значений (3 нед., 0%, x1.0 и т.д.) — тёмный цвет */
    div[data-baseweb="slider"] [data-testid*="stThumbValue"] {
        color: #31333F !important;
        background: transparent !important;
    }

    /* 5. Подписи под слайдерами */
    div[data-baseweb="slider"] div[role="presentation"] {
        color: #31333F !important;
    }

    /* 6. Активные кнопки сайдбара — светлый стиль без красного */
    button[kind="primary"],
    button[kind="primary"]:hover,
    button[kind="primary"]:focus,
    button[kind="primary"]:active,
    button[kind="primary"]:focus-visible {
        background-color: #f0f2f6 !important;
        color: #31333F !important;
        border: 1px solid #d1d5db !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* 7. Убираем красный фокус/обводку везде */
    *:focus,
    *:focus-visible {
        outline: none !important;
        box-shadow: none !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)