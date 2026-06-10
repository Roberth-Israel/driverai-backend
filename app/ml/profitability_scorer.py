class ProfitabilityScorer:
    def calculate_score(
        self,
        demand_intensity: float,
        average_earnings_per_km: float,
        average_wait_time: float,
        competition_level: int,
        surge_multiplier: float,
        distance_from_driver: float = 0,
        traffic_level: int = 0,
    ) -> int:
        demand_score = demand_intensity * 25
        earnings_score = min(average_earnings_per_km * 15, 25)
        wait_score = max(0, 15 - average_wait_time * 2)
        competition_score = max(0, 15 - competition_level * 3)
        surge_score = min((surge_multiplier - 1) * 20, 10)

        if distance_from_driver > 0:
            distance_factor = max(0, 1 - (distance_from_driver / 20))
        else:
            distance_factor = 1.0

        if traffic_level > 0:
            traffic_penalty = traffic_level * 2
        else:
            traffic_penalty = 0

        score = (demand_score + earnings_score + wait_score +
                 competition_score + surge_score) * distance_factor - traffic_penalty

        return max(0, min(100, int(round(score))))

    def get_score_rating(self, score: int) -> str:
        if score >= 80: return "Excelente"
        if score >= 60: return "Boa"
        if score >= 40: return "Média"
        if score >= 20: return "Baixa"
        return "Evitar"

    def get_score_color(self, score: int) -> str:
        if score >= 80: return "#4CAF50"
        if score >= 60: return "#FF9800"
        if score >= 40: return "#FFC107"
        if score >= 20: return "#8BC34A"
        return "#F44336"
