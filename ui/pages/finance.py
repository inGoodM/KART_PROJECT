import streamlit as st
import pandas as pd
import plotly.express as px
from ui.components.elements import render_detailed_group_card

def show_finance_page():
    st.caption("Оценка эффективности капитала и прогноз окупаемости")

    # --- БЛОК 1: 8 ФИНАНСОВЫХ КАРТОЧЕК ---
    # Первый ряд
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_detailed_group_card("ROI Прогноз", "185%", "#10b981", "trend", [
            ("Чистая прибыль", "+420к ₽"), ("На вложенный 1₽", "1.85 ₽")
        ])
    with c2:
        render_detailed_group_card("Упущенная прибыль", "580,000 ₽", "#ef4444", "alert", [
            ("Из-за дефицита", "14 дн."), ("Потеря маржи", "215к ₽")
        ])
    with c3:
        render_detailed_group_card("Здоровье склада", "78%", "#8b5cf6", "layers", [
            ("Ликвидный сток", "85%"), ("Неликвид (3мес+)", "15%")
        ])
    with c4:
        render_detailed_group_card("Burn Rate (Дни)", "45 дней", "#ec4899", "stats", [
            ("Запас прочности", "Высокий"), ("Покрытие костов", "Маржой")
        ])

    # Второй ряд
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        render_detailed_group_card("Ближайший платеж", "1.2 млн ₽", "#f59e0b", "wallet", [
            ("Дата", "24.02.2025"), ("Поставщик", "Innovation Lab")
        ])
    with c6:
        render_detailed_group_card("Окупаемость партии", "62%", "#6366f1", "refresh", [
            ("Точка безуб.", "через 18 дн."), ("Продано штук", "415/700")
        ])
    with c7:
        render_detailed_group_card("Курсовой риск", "Средний", "#64748b", "percent", [
            ("Чувствит. маржи", "-4.2%"), ("При росте курса", "+5%")
        ])
    with c8:
        render_detailed_group_card("Оборачиваемость", "24 дня", "#0ea5e9", "truck", [
            ("Цикл капитала", "1.2 мес."), ("Цель", "20 дней")
        ])

    st.divider()

    # --- БЛОК 2: ПУЗЫРЬКОВАЯ МАТРИЦА ---
    st.subheader("Матрица: Деньги vs Оборачиваемость")
    
    # Тестовые данные для визуализации
    matrix_data = pd.DataFrame({
        "Категория": ["Feeto Care", "Innovation", "Упаковка", "Расходники", "Аппараты", "Наборы"],
        "Время на складе (дни)": [15, 45, 120, 25, 90, 10],
        "Замороженные деньги (₽)": [1200000, 850000, 300000, 150000, 2100000, 950000],
        "Маржинальность (%)": [42, 55, 20, 35, 65, 52]
    })

    fig = px.scatter(
        matrix_data,
        x="Время на складе (дни)",
        y="Замороженные деньги (₽)",
        size="Маржинальность (%)",
        color="Категория",
        hover_name="Категория",
        size_max=50,
        height=500,
        template="plotly_white"
    )

    # Добавляем разделители зон (квадранты)
    fig.add_vline(x=60, line_dash="dash", line_color="#cbd5e1")
    fig.add_hline(y=1000000, line_dash="dash", line_color="#cbd5e1")

    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Верхний правый квадрант — зона риска (много денег лежат долго). Верхний левый — зона фокуса (высокий оборот капитала).")