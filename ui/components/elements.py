import streamlit as st

# Полный словарь иконок с запасом по именам ключей
SVG_ICONS = {
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>',
    "truck": '<rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>',
    "cart": '<circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>',
    "alert-triangle": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>',
    "stats": '<line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>',
    "wallet": '<rect x="2" y="5" width="20" height="14" rx="2" ry="2"></rect><path d="M16 11h.01"></path>',
    "trend": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline>'
}

def render_kpi_card(title, value, subtitle, color, icon_svg):
    """Карточка KPI — теперь точно работает с overview.py"""
    st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #f1f5f9; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                <div>
                    <div style="color: #64748b; font-size: 0.85rem; font-weight: 500;">{title}</div>
                </div>
                <div style="color: {color};">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{icon_svg}</svg>
                </div>
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #1e293b; margin-bottom: 4px;">{value}</div>
            <div style="color: #10b981; font-size: 0.8rem; font-weight: 500;">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)

def render_category_distribution(name, count, amount, percentage, color):
    """Отрисовка категорий с 5 аргументами"""
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px; background: #f8fafc; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {color};">
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #1e293b; font-size: 0.9rem;">{name}</div>
                <div style="color: #64748b; font-size: 0.8rem;">{count} ед. — {amount} ₽</div>
            </div>
            <div style="font-weight: 700; color: {color};">{percentage}%</div>
        </div>
    """, unsafe_allow_html=True)

def render_recommendation_card(d):
    """Карточка для новой страницы инвентаризации"""
    st.markdown(f"""
        <div style="background: white; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0;">
            <div style="color: #1e293b; font-weight: 700; margin-bottom: 16px;">Рекомендация к заказу</div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 2.8rem; font-weight: 800; color: #2563eb;">{d.get('total', 0)}</span>
                <span style="font-size: 1.2rem; font-weight: 600; color: #2563eb;"> шт</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.9rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #64748b;">Тренд (3 мес):</span>
                    <span style="font-weight: 700;">{d.get('trend', 0)} шт/мес</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; padding-top: 16px; border-top: 2px solid #f1f5f9; color: #1e3a8a;">
                    <span style="font-weight: 800;">ИТОГО НАДО:</span>
                    <span style="font-weight: 900; font-size: 1.2rem;">{d.get('total', 0)}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_deficit_item(*args, **kwargs):
    """Гибкая заглушка для элементов дефицита"""
    st.write(f"Элемент: {args[0] if args else ''}")