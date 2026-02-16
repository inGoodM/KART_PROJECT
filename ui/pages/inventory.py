import streamlit as st
import pandas as pd
from ui.components.elements import render_recommendation_card

# Безопасный импорт plotly
try:
    import plotly.graph_objects as go
except ImportError:
    go = None

def show_inventory_page():
    st.header("Товары и прогноз")
    
    # Кнопки в ряд
    cols = st.columns(4)
    buttons = ["Прогноз по товарам", "Прогноз по группам", "По контрагентам", "Маркетинг"]
    for i, b in enumerate(buttons):
        cols[i].button(b, use_container_width=True, type="primary" if i==0 else "secondary")

    st.divider()

    col_l, col_r = st.columns([2.5, 1])
    
    with col_l:
        st.subheader("График прогноза")
        if go:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=[40, 35, 30, 25, 45, 60, 80], line=dict(color='#2563eb', width=3)))
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Установите plotly: pip install plotly")

    with col_r:
        render_recommendation_card({
            "total": 85, "trend": 45, "outflow": 55
        })

    # Таблица с рублем
    st.markdown("### Детализация")
    df = pd.DataFrame({
        "Артикул": ["7723", "30085"],
        "Наименование": ["Крем Red & Itchy", "Масло восстановление"],
        "Остаток": [20, 10],
        "Закупка": [85, 185],
        "Бюджет (₽)": ["127,500 ₽", "277,500 ₽"]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)