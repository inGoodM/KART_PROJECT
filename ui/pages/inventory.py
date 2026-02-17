import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ui.components.elements import render_recommendation_card, render_group_metric_card

def show_inventory_page():
    st.caption("Детализация по товарам и расчётам")

    # 1. ПЕРЕКЛЮЧАТЕЛЬ РЕЖИМОВ
    modes = ["Прогноз по товарам", "Прогноз по группам", "По контрагентам", "Маркетинг"]
    if "inventory_mode" not in st.session_state:
        st.session_state.inventory_mode = modes[0]

    cols = st.columns(4)
    for i, mode in enumerate(modes):
        is_active = st.session_state.inventory_mode == mode
        if cols[i].button(
            mode,
            use_container_width=True,
            type="primary" if is_active else "secondary",
            key=f"mode_btn_{i}"
        ):
            st.session_state.inventory_mode = mode
            st.rerun()

    st.divider()
    current = st.session_state.inventory_mode

    # 2. ДАННЫЕ (Общие для страницы)
    data = {
        "Категория": [
            "Косметика и препараты/Feeto Care", "Косметика и препараты/Feeto Care",
            "Косметика и препараты/Innovation", "Косметика и препараты/Innovation",
            "Раздаточные и упаковочные материалы"
        ],
        "Артикул": ["7723", "30085", "8015", "7714", "9901"],
        "Наименование": [
            "Крем Red & Itchy 150 мл", "Масло восстановление 50 мл",
            "Cell Booster 250 мл", "Питательный крем для рук 100 мл",
            "Пакет зип-лок 10x15"
        ],
        "Остаток": [20, 10, 21, 45, 1200],
        "Рекоменд. закупка": [85, 185, 140, 90, 0],
        "Бюджет (руб)": [127500, 277500, 210000, 135000, 0]
    }
    df = pd.DataFrame(data)

    # 3. ЛОГИКА ОКНА "ПРОГНОЗ ПО ТОВАРАМ"
    if current == "Прогноз по товарам":
        all_sales = {
            "7723": [55, 48, 42, 38, 45, 60, 75, 82, 78, 65, 58, 52, 50, 52, 68, 72, 78, 105, 110],
            "30085": [60, 55, 50, 45, 52, 68, 80, 85, 82, 70, 62, 55, 52, 55, 70, 75, 82, 110, 115],
            "8015": [45, 40, 35, 32, 40, 55, 70, 75, 72, 60, 52, 45, 42, 45, 60, 65, 70, 95, 100],
            "7714": [70, 65, 60, 55, 65, 80, 90, 95, 92, 80, 70, 65, 60, 62, 75, 80, 85, 110, 115],
            "9901": [1200, 1150, 1100, 1050, 1120, 1250, 1300, 1350, 1320, 1250, 1180, 1100, 1050, 1100, 1200, 1250, 1300, 1400, 1450]
        }
        
        start_date = datetime(2025, 1, 1)
        months = []
        month_map = {"Jan": "Янв", "Feb": "Фев", "Mar": "Мар", "Apr": "Апр", "May": "Май", "Jun": "Июн", "Jul": "Июл", "Aug": "Авг", "Sep": "Сен", "Oct": "Окт", "Nov": "Ноя", "Dec": "Дек"}
        for i in range(19):
            d = start_date + relativedelta(months=i)
            months.append(f"{month_map[d.strftime('%b')]} {d.year}")

        if "selected_sku" not in st.session_state:
            st.session_state.selected_sku = df["Артикул"].iloc[0]

        left, right = st.columns([2.5, 1])
        with left:
            sku = st.session_state.selected_sku
            selected_row = df[df["Артикул"] == sku].iloc[0]
            st.markdown(f"**{selected_row['Артикул']}** — {selected_row['Наименование']}")
            chart_df = pd.DataFrame({"Месяц": months, "Продажи": all_sales.get(sku, [0]*19)}).set_index("Месяц")
            st.line_chart(chart_df, height=350, use_container_width=True)

        with right:
            render_recommendation_card({"total": int(selected_row["Рекоменд. закупка"]), "trend": 7.2, "outflow": 55})

        st.markdown("### Детализация")
        def update_sku(key):
            st.session_state.selected_sku = st.session_state[key]

        for cat in df["Категория"].unique():
            with st.expander(cat, expanded=(cat == selected_row["Категория"])):
                cat_df = df[df["Категория"] == cat].copy()
                options = ["Выберите товар"] + cat_df["Артикул"].tolist()
                st.selectbox("Артикул:", options, index=options.index(sku) if sku in options else 0, key=f"sel_{cat}", on_change=update_sku, args=(f"sel_{cat}",))
                cat_df["Бюджет (руб)"] = cat_df["Бюджет (руб)"].apply(lambda x: f"{x:,} руб")
                st.dataframe(cat_df[["Артикул", "Наименование", "Остаток", "Рекоменд. закупка", "Бюджет (руб)"]], use_container_width=True, hide_index=True)

    # 4. НОВАЯ ЛОГИКА: ПРОГНОЗ ПО ГРУППАМ
    elif current == "Прогноз по группам":
        # Метрики по группам
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_group_metric_card("Наборы", "420 наб.", "Комплектация", "85%", "#4f46e5", "layers")
        with m2:
            render_group_metric_card("Розница", "1.2 млн ₽", "Темп роста", "+12.4%", "#0ea5e9", "cart")
        with m3:
            render_group_metric_card("Оптовики", "3.8 млн ₽", "Ср. отгрузка", "450 шт", "#10b981", "truck")
        with m4:
            render_group_metric_card("Дефицит", "12 SKU", "Упущенная выр.", "450к ₽", "#ef4444", "alert-triangle")

        st.write("")
        
        # Визуализация спроса по группам
        left, right = st.columns([2, 1])
        with left:
            st.markdown("#### Сравнение спроса по каналам")
            group_chart_data = pd.DataFrame({
                "Группа": ["Розница", "Опт", "Наборы"],
                "Факт (Янв)": [850, 1200, 400],
                "Прогноз (Фев)": [980, 1450, 420]
            }).set_index("Группа")
            st.bar_chart(group_chart_data, height=300)
            
        
        with right:
            st.markdown("#### Доля в бюджете закупки")
            budget_dist = pd.DataFrame({
                "Группа": ["Розница", "Опт", "Наборы"],
                "Бюджет": [450000, 1200000, 300000]
            })
            # Используем встроенный чарт для круговой диаграммы если нужно, или просто таблицу
            st.dataframe(budget_dist, use_container_width=True, hide_index=True)

        st.markdown("### Сводная таблица по группам")
        group_summary = pd.DataFrame({
            "Группа": ["Наборы", "Розница", "Опт"],
            "Товаров в группе": [15, 142, 85],
            "Текущий запас (дн)": [12, 24, 45],
            "Прогноз (мес)": ["420 наб", "5,200 ед", "12,400 ед"],
            "Сумма закупки": ["300,000 ₽", "450,000 ₽", "1,200,000 ₽"]
        })
        st.dataframe(group_summary, use_container_width=True, hide_index=True)

    elif current == "По контрагентам":
        st.info("Анализ по поставщикам в разработке")
    elif current == "Маркетинг":
        st.info("Учёт акций в разработке")