# config.py
# Все глобальные константы приложения — цвета, параметры, страницы и т.д.
# Расширяй здесь при добавлении новых функций/параметров

# Цвета для ползунков (по порядку PARAM_CONFIG)
SLIDER_COLORS = [
    "#4B6BFB",  # Синий — sl_lead
    "#7C3AED",  # Фиолетовый — sl_cycle
    "#10B981",  # Зеленый — sl_corr
    "#F59E0B",  # Оранжевый — sl_season
    "#6B7280",  # Серый — sl_safe
]

# Конфигурация всех параметров закупки (слайдеры)
PARAM_CONFIG = [
    {
        "key": "sl_lead",
        "label": "Срок текущей поставки",
        "min": 1,
        "max": 12,
        "default": 3,
        "format": "%d нед.",
        "caption": 'Когда приедет "Довоз"'
    },
    {
        "key": "sl_cycle",
        "label": "Срок след. закупки",
        "min": 4,
        "max": 52,
        "default": 12,
        "format": "%d нед.",
        "caption": "На какой срок закупаем"
    },
    {
        "key": "sl_corr",
        "label": "% Продаж (Коррекция)",
        "min": -50,
        "max": 50,
        "default": 0,
        "format": "%d%%",
        "caption": "Ручное изменение тренда"
    },
    {
        "key": "sl_season",
        "label": "Сезонность",
        "min": 0.5,
        "max": 2.0,
        "default": 1.0,
        "step": 0.1,
        "format": "x%.1f",
        "caption": "Сила сезонных колебаний"
    },
    {
        "key": "sl_safe",
        "label": "Страховой запас",
        "min": 0,
        "max": 50,
        "default": 0,
        "format": "%d%%",
        "caption": "% от потребности"
    },
]

# Страницы приложения (навигация)
PAGES = {
    "Обзор и KPI": {
        "icon": ":material/analytics:",
        "caption": "Аналитическая сводка и ключевые показатели",
        "show_params": True
    },
    "Товары и прогноз": {
        "icon": ":material/inventory_2:",
        "caption": "Детализация по товарам и расчеты",
        "show_params": True
    },
    "Финансы": {
        "icon": ":material/payments:",
        "caption": "Финансовое планирование закупок",
        "show_params": True
    },
    "Маркетинг": {
        "icon": ":material/campaign:",
        "caption": "Маркетинговые активности и влияние на спрос",
        "show_params": True
    },
    "Контрагенты": {
        "icon": ":material/groups:",
        "caption": "Управление поставщиками и контрагентами",
        "show_params": False
    },
    "Матрица сезонности": {
        "icon": ":material/calendar_view_month:",
        "caption": "Визуализация сезонных паттернов",
        "show_params": False
    },
    "Источник данных": {
        "icon": ":material/source:",
        "caption": "Настройка API и внешних соединений",
        "show_params": False
    },
}

# Общие настройки приложения
APP_TITLE = "KART | Система управления"
APP_NAME = "KART SYSTEM"

CATEGORIES = [
    "Все категории",
    "Косметика и препараты/Clear & Matte",
    "Косметика и препараты/Feeto Care",
    "Косметика и препараты/Innovation",
    "Косметика и препараты/M-Balance",
    "Косметика и препараты/Natural Medicare",
    "Косметика и препараты/Professional Feet",
    "Косметика и препараты/Timeless",
    "Косметика и препараты/Unicare",
    "Инструменты и расходники/Колпачки",
    "Пробники",
    "SHELC/Bodycare Professional",
    "Одежда для мастеров",
    "Раздаточные и упаковочные материалы"
]