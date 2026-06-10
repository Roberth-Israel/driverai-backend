import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional


class DemandPredictor:
    def __init__(self):
        self.model_loaded = False

    async def predict_zone_demand(
        self,
        zone_id: str,
        historical_data: List[dict],
        weather: Optional[dict] = None,
        events: Optional[List[dict]] = None,
    ) -> dict:
        now = datetime.utcnow()
        day_of_week = now.weekday()
        hour = now.hour
        is_weekend = day_of_week >= 5
        is_rush_hour = (7 <= hour <= 9) or (17 <= hour <= 19)

        base_demand = self._calculate_base_demand(historical_data, day_of_week, hour)
        weather_factor = self._weather_factor(weather)
        event_factor = self._event_factor(events)
        time_factor = 1.3 if is_rush_hour else (0.8 if 0 <= hour <= 5 else 1.0)
        weekend_factor = 0.9 if is_weekend else 1.1

        current_demand = base_demand * weather_factor * event_factor * time_factor * weekend_factor

        return {
            "current_demand": round(min(current_demand, 1.0), 4),
            "predicted_15m": round(min(current_demand * 1.05, 1.0), 4),
            "predicted_30m": round(min(current_demand * (1.1 if is_rush_hour else 0.95), 1.0), 4),
            "predicted_60m": round(min(self._long_term_prediction(base_demand, hour), 1.0), 4),
            "confidence": 0.85 if self.model_loaded else 0.65,
        }

    def _calculate_base_demand(self, historical: List[dict], day: int, hour: int) -> float:
        if not historical:
            return 0.5

        recent = [h.get("demand", 0.5) for h in historical[-30:]]
        if not recent:
            return 0.5

        weights = np.linspace(0.5, 1.0, len(recent))
        weighted_avg = np.average(recent, weights=weights)
        return float(weighted_avg)

    def _weather_factor(self, weather: Optional[dict]) -> float:
        if not weather:
            return 1.0

        condition = weather.get("condition", "").lower()
        rain_intensity = weather.get("rain_intensity", 0)

        if "heavy_rain" in condition or rain_intensity > 5:
            return 1.4
        if "rain" in condition or rain_intensity > 0:
            return 1.2
        if "clear" in condition or "sunny" in condition:
            return 1.0
        if "cloud" in condition:
            return 0.95
        return 1.0

    def _event_factor(self, events: Optional[List[dict]]) -> float:
        if not events:
            return 1.0

        factor = 1.0
        for event in events:
            impact = event.get("impact", "low")
            if impact == "high":
                factor += 0.3
            elif impact == "medium":
                factor += 0.15
            else:
                factor += 0.05
        return min(factor, 2.0)

    def _long_term_prediction(self, base_demand: float, current_hour: int) -> float:
        hourly_pattern = {
            0: 0.3, 1: 0.2, 2: 0.15, 3: 0.15, 4: 0.2, 5: 0.3,
            6: 0.5, 7: 0.7, 8: 0.85, 9: 0.8, 10: 0.7, 11: 0.75,
            12: 0.8, 13: 0.75, 14: 0.7, 15: 0.7, 16: 0.75,
            17: 0.9, 18: 0.95, 19: 0.9, 20: 0.85, 21: 0.75,
            22: 0.6, 23: 0.45,
        }

        next_hour = (current_hour + 1) % 24
        pattern_factor = hourly_pattern.get(next_hour, 0.5)
        return base_demand * (pattern_factor / hourly_pattern.get(current_hour, 0.5))
