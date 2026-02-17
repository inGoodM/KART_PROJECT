import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ui.components.elements import render_recommendation_card, render_detailed_group_card

def show_inventory_page():
    st.caption("Детализация по товарам и расчётам")

    modes = ["Прогноз по товарам", "Прогноз по группам", "По контрагентам"]
    if "inventory_mode" not in st.session_state:
        st.session_state.inventory_mode = modes[0]

    cols = st.columns(4)
    for i, mode in enumerate(modes):
        if cols[i].button(mode, use_container_width=True, type="primary" if st.session_state.inventory_mode == mode else "secondary", key=f"m_btn_{i}"):
            st.session_state.inventory_mode = mode
            st.rerun()

    st.divider()
    current = st.session_state.inventory_mode

    # Общие данные для таблиц
    data = {
        "Категория": ["Косметика/Feeto Care", "Косметика/Feeto Care", "Косметика/Innovation", "Косметика/Innovation", "Упаковка"],
        "Артикул": ["7723", "30085", "8015", "7714", "9901"],
        "Наименование": ["Крем Red & Itchy", "Масло восстановление", "Cell Booster", "Крем для рук", "Пакет зип-лок"],
        "Остаток": [20, 10, 21, 45, 1200],
        "Рекоменд. закупка": [85, 185, 140, 90, 0],
        "Бюджет (руб)": [127500, 277500, 210000, 135000, 0]
    }
    df = pd.DataFrame(data)

    if current == "Прогноз по товарам":
        # Полностью сохраненная логика детализации
        if "selected_sku" not in st.session_state: st.session_state.selected_sku = df["Артикул"].iloc[0]
        l, r = st.columns([2.5, 1])
        sku = st.session_state.selected_sku
        selected_row = df[df["Артикул"] == sku].iloc[0]
        with l:
            st.markdown(f"**{selected_row['Артикул']}** — {selected_row['Наименование']}")
            st.line_chart([45, 52, 68, 72, 80, 95, 110], height=350)
        with r:
            render_recommendation_card({"total": int(selected_row["Рекоменд. закупка"]), "trend": 7.2})
        
        st.markdown("### Детализация")
        def update_sku(key): st.session_state.selected_sku = st.session_state[key]
        for cat in df["Категория"].unique():
            with st.expander(cat, expanded=(cat == selected_row["Категория"])):
                cat_df = df[df["Категория"] == cat].copy()
                options = ["Выберите товар"] + cat_df["Артикул"].tolist()
                st.selectbox("Артикул:", options, index=options.index(sku) if sku in options else 0, key=f"sel_{cat}", on_change=update_sku, args=(f"sel_{cat}",))
                cat_df["Бюджет (руб)"] = cat_df["Бюджет (руб)"].apply(lambda x: f"{x:,} ₽")
                st.dataframe(cat_df, use_container_width=True, hide_index=True)

    elif current == "Прогноз по группам":
        col_left, col_right = st.columns([2.2, 0.8])

        with col_left:
            cards_data = [
                ("Наборы: Статус", "420 наб.", "#4f46e5", "layers", [("Горлышко", "Крем 150мл"), ("Эффект", "+185 наборов")]),
                ("Оптимизация: Аналоги", "245,000 ₽", "#10b981", "refresh", [("Заработок", "112,000 ₽"), ("Экономия", "45,000 ₽")]),
                ("Упущенная выручка", "580,000 ₽", "#ef4444", "alert", [("Дефицит", "14 дн."), ("В наборах", "215,000 ₽")]),
                ("Потери: Каналы", "Опт > Розница", "#f59e0b", "stats", [("Оптовые", "310,000 ₽"), ("Розница", "270,000 ₽")]),
                ("Потенциал (Прогноз)", "6.4 млн ₽", "#0ea5e9", "trend", [("След. месяц", "+15.4%"), ("ROI закупки", "1.8 ₽")]),
                ("Маржинальность", "42% ср.", "#ec4899", "percent", [("Наборы", "52%"), ("Розница", "38%"), ("Опт", "24%")]),
                ("Оптовый Pipeline", "2.1 млн ₽", "#8b5cf6", "truck", [("Резерв", "1,400 шт"), ("Дефицит розн.", "400 шт")]),
                ("Бюджет: План", "1.95 млн ₽", "#2563eb", "wallet", [("Наборы (60%)", "1.1 млн ₽"), ("Покрытие", "85%")]),
                ("Складская логика", "42 SKU", "#64748b", "box", [("Не закупать", "8 SKU"), ("Оптимизация", "Найдено")])
            ]

            for i in range(0, 9, 3):
                r_cols = st.columns(3)
                for j in range(3):
                    with r_cols[j]:
                        render_detailed_group_card(*cards_data[i+j])

        with col_right:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Стратегия роста выручки")
            
            # Информационная плашка для быстрого понимания
            st.info("Анализ того, как внутренние ресурсы и новая закупка влияют на оборот.")
            
            # Данные графика с учетом твоего предложения
            chart_df = pd.DataFrame({
                "Сценарий": [
                    "Как есть", 
                    "Аналоги + Наборы", 
                    "После закупки"
                ],
                "Выручка (млн)": [3.2, 4.1, 6.4] 
            }).set_index("Сценарий")
            
            st.bar_chart(chart_df, height=450)
            
            # Короткое описание финансового смысла
            st.markdown("""
            <div style="font-size: 0.8rem; color: #64748b; line-height: 1.4;">
                • <b>Аналоги + Наборы</b>: рост выручки на +0.9 млн ₽ за счет оптимизации текущего склада (без новых вложений).<br><br>
                • <b>После закупки</b>: выход на максимум (6.4 млн ₽) при закрытии всех дефицитов внешним бюджетом.
            </div>
            """, unsafe_allow_html=True)

    elif current == "По контрагентам":
        st.info("В разработке")