import streamlit as st
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta

from ui.components.elements import render_recommendation_card


def show_inventory_page():
    st.caption("Детализация по товарам и расчётам")

    # Переключатель режимов
    modes = ["Прогноз по товарам", "Прогноз по группам", "По контрагентам", "Маркетинг"]

    if "inventory_mode" not in st.session_state:
        st.session_state.inventory_mode = modes[0]

    cols = st.columns(4)
    for i, mode in enumerate(modes):
        is_active = st.session_state.inventory_mode == mode
        if cols[i].button(
            mode,
            width='stretch',
            type="primary" if is_active else "secondary",
            key=f"mode_btn_{i}"
        ):
            st.session_state.inventory_mode = mode
            st.rerun()

    st.divider()

    current = st.session_state.inventory_mode

    # Демо-данные товаров
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
            "Пакет зип-лок 10×15"
        ],
        "Остаток": [20, 10, 21, 45, 1200],
        "Рекоменд. закупка": [85, 185, 140, 90, 0],
        "Бюджет (₽)": [127500, 277500, 210000, 135000, 0]
    }

    df = pd.DataFrame(data)

    # Демо-данные продаж по артикулам (19 месяцев)
    all_sales = {
        "7723": [55, 48, 42, 38, 45, 60, 75, 82, 78, 65, 58, 52, 50, 52, 68, 72, 78, 105, 110],
        "30085": [60, 55, 50, 45, 52, 68, 80, 85, 82, 70, 62, 55, 52, 55, 70, 75, 82, 110, 115],
        "8015": [45, 40, 35, 32, 40, 55, 70, 75, 72, 60, 52, 45, 42, 45, 60, 65, 70, 95, 100],
        "7714": [70, 65, 60, 55, 65, 80, 90, 95, 92, 80, 70, 65, 60, 62, 75, 80, 85, 110, 115],
        "9901": [1200, 1150, 1100, 1050, 1120, 1250, 1300, 1350, 1320, 1250, 1180, 1100, 1050, 1100, 1200, 1250, 1300, 1400, 1450]
    }

    # Даты и русские месяцы
    start_date = datetime(2025, 1, 1)
    months = []
    for i in range(19):
        d = start_date + relativedelta(months=i)
        month_ru = d.strftime("%b %Y").replace(
            "Jan", "Янв").replace("Feb", "Фев").replace("Mar", "Мар").replace("Apr", "Апр"
        ).replace("May", "Май").replace("Jun", "Июн").replace("Jul", "Июл").replace("Aug", "Авг"
        ).replace("Sep", "Сен").replace("Oct", "Окт").replace("Nov", "Ноя").replace("Dec", "Дек")
        months.append(month_ru)

    if current == "Прогноз по товарам":
        left, right = st.columns([2.5, 1])

        with left:
            # Динамическое название графика
            if st.session_state.get("selected_sku"):
                selected_row = df[df["Артикул"] == st.session_state.selected_sku].iloc[0]
                st.markdown(f"""
                **{selected_row['Артикул']}**  
                **{selected_row['Наименование']}**  
                **{selected_row['Категория']}**
                """)
            else:
                st.markdown("**График продаж и прогноза**")

            # График
            if st.session_state.get("selected_sku"):
                sku = st.session_state.selected_sku
                if sku in all_sales:
                    sales = all_sales[sku]

                    chart_data = pd.DataFrame({
                        "Месяц": months,
                        "Продажи": sales
                    }).set_index("Месяц")

                    st.line_chart(
                        chart_data,
                        height=420,
                        width='stretch',
                        x_label="Месяц",
                        y_label="Продажи (шт)"
                    )

                    st.caption("Текущий месяц: Фев 2026")
                else:
                    st.info("Нет данных по этому товару")
            else:
                st.info("Выберите товар в таблице ниже для просмотра графика")

        with right:
            render_recommendation_card({
                "total": 547,
                "trend": 7.2,
                "outflow": 55
            })

        st.markdown("### Детализация")

        # Автоматический выбор первого товара при первой загрузке
        if "selected_sku" not in st.session_state or st.session_state.selected_sku is None:
            st.session_state.selected_sku = df["Артикул"].iloc[0]

        # Кнопка скачивания данных для заказа (только актуальные данные)
        @st.cache_data
        def generate_order_csv():
            order_df = df[["Категория", "Артикул", "Наименование", "Остаток", "Рекоменд. закупка", "Бюджет (₽)"]].copy()
            order_df["Бюджет (₽)"] = order_df["Бюджет (₽)"].apply(lambda x: f"{x:,} ₽")
            return order_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Скачать данные для заказа (CSV)",
            data=generate_order_csv(),
            file_name="данные_для_заказа.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )

        # Раскрывающиеся категории с selectbox
        for cat in df["Категория"].unique():
            with st.expander(f"{cat}"):
                cat_df = df[df["Категория"] == cat].copy()
                cat_df["Бюджет (₽)"] = cat_df["Бюджет (₽)"].apply(lambda x: f"{x:,} ₽")

                # Selectbox для выбора товара внутри категории
                sku_list = ["Выберите товар"] + cat_df["Артикул"].tolist()
                selected_sku = st.selectbox(
                    "Выберите товар для графика",
                    sku_list,
                    key=f"select_{cat.replace('/', '_')}"
                )

                if selected_sku != "Выберите товар":
                    st.session_state.selected_sku = selected_sku
                    st.rerun()

                # Таблица товаров
                st.dataframe(
                    cat_df[["Артикул", "Наименование", "Остаток", "Рекоменд. закупка", "Бюджет (₽)"]],
                    use_container_width=True,
                    hide_index=True
                )

    elif current == "Прогноз по группам":
        st.info("Агрегация по категориям / подкатегориям (в разработке)")

    elif current == "По контрагентам":
        st.info("Анализ по поставщикам (в разработке)")

    elif current == "Маркетинг":
        st.info("Учёт акций и промо (в разработке)")

    else:
        st.error(f"Неизвестный режим: {current}")