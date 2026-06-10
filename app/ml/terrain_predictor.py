"""
Predictor de adequação do terreno para suspensão do veículo.
Analisa elevação, tipo de superfície e rugosidade estimada.
"""
import math
import random
from typing import List, Dict


class TerrainPredictor:
    def __init__(self):
        self.model_loaded = False

    def predict(
        self,
        origem_lat: float,
        origem_lng: float,
        dest_lat: float,
        dest_lng: float,
        vehicle_type: str = "sedan",
    ) -> Dict:
        elevation_change = self._estimate_elevation(origem_lat, origem_lng, dest_lat, dest_lng)
        roughness = self._estimate_roughness(origem_lat, origem_lng, dest_lat, dest_lng)
        surface_type = self._classify_surface(origem_lat, origem_lng, dest_lat, dest_lng)
        distance = self._haversine(origem_lat, origem_lng, dest_lat, dest_lng)

        vehicle_factors = {
            "sedan": 1.0,
            "hatch": 1.1,
            "suv": 0.6,
            "pickup": 0.5,
            "van": 0.8,
        }
        vehicle_factor = vehicle_factors.get(vehicle_type, 1.0)

        surface_scores = {
            "asfalto": 0.1,
            "asfalto_irregular": 0.4,
            "misto": 0.5,
            "paralelepipedo": 0.7,
            "terra": 0.9,
        }
        surface_score = surface_scores.get(surface_type, 0.5)

        impact_score = (
            elevation_change * 0.3 +
            roughness * 0.3 +
            surface_score * 0.25 +
            (distance / 50) * 0.1 +
            (distance > 15 and surface_score > 0.5) * 0.05
        ) * vehicle_factor

        impact_score = max(0.0, min(1.0, impact_score))
        adequado = impact_score < 0.55
        confidence = max(0.6, 1.0 - impact_score * 0.4)

        if impact_score < 0.25:
            alerta = None
            recomendacao = "Terreno excelente. Sem impacto na suspensão."
        elif impact_score < 0.45:
            alerta = None
            recomendacao = "Terreno adequado. Desgaste normal da suspensão."
        elif impact_score < 0.55:
            alerta = "Atenção: trecho com irregularidades leves"
            recomendacao = "Reduza a velocidade em ruas esburacadas."
        elif impact_score < 0.70:
            alerta = "⚠️ Terreno irregular. Impacto no amortecedor."
            recomendacao = "Evite velocidade acima de 40 km/h neste trecho."
        else:
            alerta = "🚫 Estrada de terra/off-road. Risco para suspensão."
            recomendacao = "Considere rotas alternativas para preservar a suspensão."

        return {
            "adequado": adequado,
            "confidence": round(confidence, 4),
            "alerta": alerta,
            "tipo_terreno": self._surface_label(surface_type),
            "impact_score": round(impact_score, 4),
            "recomendacao": recomendacao,
            "elevation_change_m": round(elevation_change, 1),
            "roughness_index": round(roughness, 4),
            "surface_type": surface_type,
            "vehicle_factor": vehicle_factor,
        }

    def get_route_segments(
        self,
        origem_lat: float,
        origem_lng: float,
        dest_lat: float,
        dest_lng: float,
        num_segments: int = 5,
    ) -> List[Dict]:
        segments = []
        for i in range(num_segments):
            frac = i / num_segments
            next_frac = (i + 1) / num_segments

            lat1 = origem_lat + (dest_lat - origem_lat) * frac
            lng1 = origem_lng + (dest_lng - origem_lng) * frac
            lat2 = origem_lat + (dest_lat - origem_lat) * next_frac
            lng2 = origem_lng + (dest_lng - origem_lng) * next_frac

            seg_result = self.predict(lat1, lng1, lat2, lng2)
            segments.append({
                "segment": i + 1,
                "adequado": seg_result["adequado"],
                "tipo_terreno": seg_result["tipo_terreno"],
                "impact_score": seg_result["impact_score"],
                "alerta": seg_result["alerta"],
            })

        return segments

    def _estimate_elevation(self, lat1, lng1, lat2, lng2) -> float:
        mid_lat = (lat1 + lat2) / 2
        mid_lng = (lng1 + lng2) / 2

        elevation = (
            math.sin(mid_lat * math.pi / 180 * 4) * 60 +
            math.cos(mid_lng * math.pi / 180 * 3) * 40 +
            random.uniform(-5, 5)
        )
        return abs(elevation)

    def _estimate_roughness(self, lat1, lng1, lat2, lng2) -> float:
        seed = abs((lat1 * 1000 + lng2 * 1000)) % 100
        rng = random.Random(int(seed))

        base = rng.random()
        distance = self._haversine(lat1, lng1, lat2, lng2)
        urban_factor = 0.3 if distance < 5 else 0.5

        return min(1.0, base * 0.7 + urban_factor * 0.3)

    def _classify_surface(self, lat1, lng1, lat2, lng2) -> str:
        distance = self._haversine(lat1, lng1, lat2, lng2)
        mid_lat = (lat1 + lat2) / 2

        is_urban = abs(mid_lat - (-23.5)) < 0.5
        is_long_route = distance > 10

        if is_urban and not is_long_route:
            return random.choices(
                ["asfalto", "asfalto_irregular", "misto", "paralelepipedo"],
                weights=[0.6, 0.2, 0.15, 0.05],
            )[0]
        elif is_long_route:
            return random.choices(
                ["asfalto", "asfalto_irregular", "misto", "terra"],
                weights=[0.5, 0.2, 0.2, 0.1],
            )[0]
        else:
            return random.choices(
                ["asfalto", "asfalto_irregular", "misto", "paralelepipedo", "terra"],
                weights=[0.4, 0.2, 0.2, 0.1, 0.1],
            )[0]

    def _surface_label(self, surface_type: str) -> str:
        labels = {
            "asfalto": "Asfalto",
            "asfalto_irregular": "Asfalto Irregular",
            "misto": "Misto",
            "paralelepipedo": "Paralelepípedo",
            "terra": "Terra/Off-road",
        }
        return labels.get(surface_type, "Desconhecido")

    def _haversine(self, lat1, lng1, lat2, lng2) -> float:
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) *
             math.cos(math.radians(lat2)) *
             math.sin(dlng / 2) ** 2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
