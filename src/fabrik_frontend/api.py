import requests

BASE_URL = "http://128.140.85.215:8888"
HEADERS = {}


# --- read endpoints (no key required) ---

def get_teile():
    r = requests.get(f"{BASE_URL}/teile", timeout=5)
    r.raise_for_status()
    return r.json()

def get_produkte():
    r = requests.get(f"{BASE_URL}/produkte", timeout=5)
    r.raise_for_status()
    return r.json()

def get_stueckliste(produkt_id: int):
    r = requests.get(f"{BASE_URL}/stueckliste/{produkt_id}", timeout=5)
    r.raise_for_status()
    return r.json()

def get_bestellwarnungen():
    r = requests.get(f"{BASE_URL}/bestellwarnungen", timeout=5)
    r.raise_for_status()
    return r.json()


# --- write endpoints (API key required) ---

def post_wareneingang(teil_id: int, menge: int, notiz: str = ""):
    payload = {"teil_id": teil_id, "menge": menge, "notiz": notiz or None}
    r = requests.post(f"{BASE_URL}/wareneingang", json=payload, headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()

def post_produktion(produkt_id: int, menge: int):
    payload = {"produkt_id": produkt_id, "menge": menge}
    r = requests.post(f"{BASE_URL}/produktion", json=payload, headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()

def post_lagerausgang(produkt_id: int, menge: int, notiz: str = ""):
    payload = {"produkt_id": produkt_id, "menge": menge, "notiz": notiz or None}
    r = requests.post(f"{BASE_URL}/lagerausgang", json=payload, headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()

def put_teil_bestand(teil_id: int, bestand: int):
    payload = {"bestand": bestand}
    r = requests.put(f"{BASE_URL}/teile/{teil_id}", json=payload, headers=HEADERS, timeout=5)
    r.raise_for_status()
    return r.json()
