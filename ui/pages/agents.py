import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ui.components.elements import render_detailed_group_card

def show_agents_page():
    st.caption("Стратегический анализ клиентской базы и лояльности")

    # --- БЛОК 1: СТРАТЕГИЧЕСКИЕ КАРТОЧКИ ---
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        render_detailed_group_card("LTV (Средний)", "142,000 ₽", "#10b981", "payments", [
            ("Категория А", "420к ₽"), ("Динамика", "+12%")
        ])
    with c2:
        render_detailed_group_card("Retention Rate", "68%", "#6366f1", "sync_alt", [
            ("Повторные", "42 чел."), ("Удержание", "Высокое")
        ])
    with c3:
        render_detailed_group_card("Индекс NPS", "72", "#8b5cf6", "thumb_up", [
            ("Промоутеры", "82%"), ("Критики", "5%")
        ])
    with c4:
        render_detailed_group_card("Доля 'Одного заказа'", "18%", "#ef4444", "person_remove", [
            ("Новички", "12 чел."), ("Цель", "< 15%")
        ])
    with c5:
        render_detailed_group_card("Ср. время жизни", "14 мес.", "#0ea5e9", "hourglass_empty", [
            ("Цикл связи", "420 дн."), ("Категория А", "28 мес.")
        ])

    st.divider()

    # --- БЛОК 2: МАТРИЦА ЛОЯЛЬНОСТИ (SCATTER PLOT) ---
    st.subheader("Матрица сегментации: Лояльность vs Выручка")
    
    # Данные для матрицы
    matrix_data = pd.DataFrame({
        "Контрагент": ["Салон Эстетика", "Центр Подологии", "ИП Иванова", "Beauty Store", "Клиника МедАрт", "Nail Studio", "Pro-Skin"],
        "Частота заказов (в год)": [12, 8, 24, 4, 6, 18, 2],
        "Общая выручка (₽)": [1200000, 850000, 310000, 2100000, 920000, 450000, 150000],
        "Сегмент": ["VIP", "Лояльный", "Мастер (частый)", "Кит (редкий)", "Лояльный", "Мастер (частый)", "Спящий"],
        "NPS": [90, 85, 95, 40, 70, 80, 50]
    })

    fig_matrix = px.scatter(
        matrix_data,
        x="Частота заказов (в год)",
        y="Общая выручка (₽)",
        size="NPS",
        color="Сегмент",
        hover_name="Контрагент",
        size_max=40,
        template="plotly_white",
        height=500
    )
    # Зонирование
    fig_matrix.add_vline(x=10, line_dash="dash", line_color="#cbd5e1")
    fig_matrix.add_hline(y=1000000, line_dash="dash", line_color="#cbd5e1")
    
    st.plotly_chart(fig_matrix, use_container_width=True)
    

    # --- БЛОК 3: WATERFALL И ПАРЕТО ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Динамика базы (Waterfall)")
        # Waterfall: Новые, Вернувшиеся, Потерянные
        fig_waterfall = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["absolute", "relative", "relative", "total"],
            x = ["База (нач)", "Новые", "Отток", "База (кон)"],
            textposition = "outside",
            y = [100, 25, -12, 0],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        fig_waterfall.update_layout(height=350, template="plotly_white", margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col_right:
        st.markdown("### Анализ концентрации (Парето)")
        # Линия накопленной выручки
        pareto_data = pd.DataFrame({
            "Клиенты %": [0, 20, 40, 60, 80, 100],
            "Выручка %": [0, 65, 82, 91, 97, 100]
        })
        fig_pareto = px.line(pareto_data, x="Клиенты %", y="Выручка %", markers=True)
        fig_pareto.add_hline(y=80, line_dash="dot", line_color="red", annotation_text="Граница 80%")
        fig_pareto.update_layout(height=350, template="plotly_white", margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig_pareto, use_container_width=True)
        

    st.info("💡 **Аналитика:** 20% ваших клиентов (категория Кит/VIP) генерируют 82% выручки. Снижение NPS в сегменте 'Кит' (Beauty Store) — критический риск для следующего месяца.")