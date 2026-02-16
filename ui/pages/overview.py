import streamlit as st
from config import CATEGORIES
from ui.components.elements import render_kpi_card, render_category_distribution, render_deficit_item, SVG_ICONS

def show_overview_page():
    st.subheader("Ключевые показатели")

    selected_category = st.selectbox(
        "Категория для расчёта KPI",
        options=CATEGORIES, index=0, key="kpi_category_selector"
    )

    # Имитация данных для отображения
    data = {"stock": 7984, "incoming": 13330, "plan": 3341, "deficit": 84, "money": 31971000}

    # 1. Ряд карточек KPI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Общий остаток", f"{data['stock']:,} шт.", "На складе", "#4B6BFB", SVG_ICONS["box"])
    with col2:
        render_kpi_card("Ожидается", f"+{data['incoming']:,} шт.", "В пути до 09.03", "#7C3AED", SVG_ICONS["truck"])
    with col3:
        render_kpi_card("План закупки", f"{data['plan']:,} шт.", "+16% к запасам", "#10B981", SVG_ICONS["cart"])
    with col4:
        render_kpi_card("Дефицит", f"{data['deficit']} SKU", "Риск обнуления", "#EF4444", SVG_ICONS["alert"])

    st.markdown(f"<p style='text-align:center; color:#6c757d; margin: 20px 0;'>Аналитический срез: <b>{selected_category}</b></p>", unsafe_allow_html=True)
    st.markdown("---")

    # 2. Нижние блоки аналитики
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        # Заголовок Анализ запасов
        st.markdown(f'''<div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4B6BFB" stroke-width="2">{SVG_ICONS["stats"]}</svg>
            <h3 style="margin:0;">Анализ запасов</h3></div>''', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.write("**Соотношение к несгораемому минимуму (1.5 мес.)**")
            st.markdown("""
                <div style="background:#e9ecef; border-radius:10px; height:18px; width:100%; margin: 10px 0;">
                    <div style="background: linear-gradient(90deg, #4B6BFB, #7C3AED); width:75%; height:18px; border-radius:10px; display:flex; align-items:center; justify-content:center;">
                        <span style="color:white; font-size:0.7rem; font-weight:bold;">75%</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Чистый блок Капитала с SVG иконкой вместо эмодзи
            st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px; padding:12px; background:#f0f7ff; border-radius:8px; border:1px solid #d0e3ff; color:#1e40af; margin-bottom:20px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1e40af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{SVG_ICONS["wallet"]}</svg>
                    <span style="font-weight:600;">Капитал в запасах: {data['money']:,} ₽</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("**По подкатегориям**")
            render_category_distribution("Professional Feet", 4281, "6,421,500", 53, "#4B6BFB")
            render_category_distribution("Innovation", 2074, "3,111,000", 26, "#7C3AED")

    with right_col:
        # Заголовок Дефициты
        st.markdown(f'''<div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2">{SVG_ICONS["alert"]}</svg>
            <h3 style="margin:0;">Товары в дефиците</h3></div>''', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.caption("Категории с критическим остатком")
            with st.expander("Professional Feet (2 SKU)", expanded=True):
                render_deficit_item("Масло восстанавливающее 50мл", "30085", "180 шт.")
                render_deficit_item("Крем для сухих стоп 150мл", "7723", "28 шт.")
            
            with st.expander("Unicare (1 SKU)"):
                render_deficit_item("Cell Booster 250мл", "8015", "21 шт.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Перейти к полному списку", use_container_width=True):
                st.session_state.active_page = "Товары и прогноз"
                st.rerun()