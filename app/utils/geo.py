import math


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_nearby_places(lat: float, lng: float, radius_km: float = 5) -> dict:
    return {
        "airports": _check_nearby_airports(lat, lng, radius_km),
        "malls": _check_nearby_malls(lat, lng, radius_km),
        "universities": _check_nearby_universities(lat, lng, radius_km),
        "hospitals": _check_nearby_hospitals(lat, lng, radius_km),
    }


def _check_nearby_airports(lat: float, lng: float, radius: float) -> bool:
    airports = [
        (-23.4356, -46.4731, "GRU"),
        (-23.6266, -46.6559, "CGH"),
        (-23.6329, -46.6633, "Congonhas"),
    ]
    for alat, alng, _ in airports:
        if haversine_distance(lat, lng, alat, alng) <= radius:
            return True
    return False


def _check_nearby_malls(lat: float, lng: float, radius: float) -> bool:
    malls = [
        (-23.5434, -46.6454, "Shopping Ibirapuera"),
        (-23.5650, -46.6500, "Shopping Paulista"),
        (-23.5577, -46.6614, "Shopping Cidade"),
    ]
    for mlat, mlng, _ in malls:
        if haversine_distance(lat, lng, mlat, mlng) <= radius:
            return True
    return False


def _check_nearby_universities(lat: float, lng: float, radius: float) -> bool:
    unis = [(-23.5610, -46.7316, "USP"), (-23.5477, -46.6365, "PUC")]
    for ulat, ulng, _ in unis:
        if haversine_distance(lat, lng, ulat, ulng) <= radius:
            return True
    return False


def _check_nearby_hospitals(lat: float, lng: float, radius: float) -> bool:
    hospitals = [(-23.5594, -46.6620, "Hospital Sírio"), (-23.5625, -46.6560, "Hospital Albert Einstein")]
    for hlat, hlng, _ in hospitals:
        if haversine_distance(lat, lng, hlat, hlng) <= radius:
            return True
    return False
