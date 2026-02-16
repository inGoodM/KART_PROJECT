# core/params.py
from dataclasses import dataclass
import streamlit as st

@dataclass
class PurchaseParams:
    """
    Класс для всех параметров закупки — удобно использовать в расчётах.
    Все значения берутся из st.session_state, дефолты — из конфига.
    Легко расширять при добавлении новых параметров.
    """
    lead_time_weeks: int = 3
    cycle_weeks: int = 12
    trend_correction_pct: float = 0.0
    seasonality_factor: float = 1.0
    safety_stock_pct: float = 0.0

    @classmethod
    def from_session(cls):
        """
        Создаёт объект с актуальными значениями из st.session_state.
        Если значение отсутствует — берёт дефолт.
        """
        return cls(
            lead_time_weeks=st.session_state.get('sl_lead', cls.lead_time_weeks),
            cycle_weeks=st.session_state.get('sl_cycle', cls.cycle_weeks),
            trend_correction_pct=st.session_state.get('sl_corr', cls.trend_correction_pct),
            seasonality_factor=st.session_state.get('sl_season', cls.seasonality_factor),
            safety_stock_pct=st.session_state.get('sl_safe', cls.safety_stock_pct)
        )

    def to_dict(self) -> dict:
        """Возвращает параметры в виде словаря — удобно для сохранения/сериализации"""
        return {
            'lead_time_weeks': self.lead_time_weeks,
            'cycle_weeks': self.cycle_weeks,
            'trend_correction_pct': self.trend_correction_pct,
            'seasonality_factor': self.seasonality_factor,
            'safety_stock_pct': self.safety_stock_pct
        }

    def __str__(self):
        """Удобный вывод для отладки"""
        return (
            f"Параметры закупки:\n"
            f"  Lead time: {self.lead_time_weeks} нед.\n"
            f"  Цикл закупки: {self.cycle_weeks} нед.\n"
            f"  Коррекция тренда: {self.trend_correction_pct:+.1f}%\n"
            f"  Сезонность: x{self.seasonality_factor:.1f}\n"
            f"  Страховой запас: {self.safety_stock_pct:.1f}%"
        )