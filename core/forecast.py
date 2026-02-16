# core/forecast.py
from core.params import PurchaseParams

def calculate_kpi(params: PurchaseParams, base_demand: int = 1000, unit_price: int = 1500) -> dict:
    """
    Простой расчёт KPI на основе параметров.
    base_demand — базовый спрос за неделю (условный)
    unit_price — условная цена за единицу товара (1500 руб)
    """
    # Базовый спрос на весь цикл закупки
    base_forecast = base_demand * params.cycle_weeks

    # Корректировка тренда
    trend_adjusted = base_forecast * (1 + params.trend_correction_pct / 100)

    # Учёт сезонности
    seasonal_adjusted = trend_adjusted * params.seasonality_factor

    # Страховой запас в штуках
    safety_stock_units = seasonal_adjusted * (params.safety_stock_pct / 100)

    # Рекомендуемый объём закупки
    recommended_volume = seasonal_adjusted + safety_stock_units

    # Примерная стоимость закупки
    estimated_cost = recommended_volume * unit_price

    return {
        "forecast_demand": round(seasonal_adjusted),
        "recommended_volume": round(recommended_volume),
        "safety_stock_units": round(safety_stock_units),
        "trend_adjustment": round(params.trend_correction_pct, 1),
        "estimated_cost": round(estimated_cost)
    }