#!/usr/bin/env python3
import json
import re
import urllib.request
import os
import datetime
import unicodedata

NAME_MAP = {
    "mexico": "Mexico",
    "africa do sul": "Africa do Sul",
    "south africa": "Africa do Sul",
    "rsa": "Africa do Sul",
    "korea republic": "Coreia do Sul",
    "south korea": "Coreia do Sul",
    "republic of korea": "Coreia do Sul",
    "coreia do sul": "Coreia do Sul",
    "kor": "Coreia do Sul",
    "czech republic": "Rep. Tcheca",
    "czechia": "Rep. Tcheca",
    "republic tcheca": "Rep. Tcheca",
    "cze": "Rep. Tcheca",
    "canada": "Canada",
    "can": "Canada",
    "bosnia and herzegovina": "Bosnia",
    "bosnia herzegovina": "Bosnia",
    "bosnia": "Bosnia",
    "bih": "Bosnia",
    "qatar": "Catar",
    "qat": "Catar",
    "switzerland": "Suica",
    "sui": "Suica",
    "brazil": "Brasil",
    "brasil": "Brasil",
    "bra": "Brasil",
    "morocco": "Marrocos",
    "mar": "Marrocos",
    "haiti": "Haiti",
    "hai": "Haiti",
    "scotland": "Escocia",
    "sco": "Escocia",
    "united states": "EUA",
    "usa": "EUA",
    "united states of america": "EUA",
    "us": "EUA",
    "paraguay": "Paraguai",
    "par": "Paraguai",
    "australia": "Australia",
    "aus": "Australia",
    "turkey": "Turquia",
    "turkiye": "Turquia",
    "tur": "Turquia",
    "germany": "Alemanha",
    "ger": "Alemanha",
    "curacao": "Curacao",
    "cur": "Curacao",
    "cote divoire": "Costa do Marfim",
    "cote d ivoire": "Costa do Marfim",
    "ivory coast": "Costa do Marfim",
    "civ": "Costa do Marfim",
    "ecuador": "Equador",
    "ecu": "Equador",
    "netherlands": "Holanda",
    "ned": "Holanda",
    "holland": "Holanda",
    "japan": "Japao",
    "jpn": "Japao",
    "sweden": "Suecia",
    "swe": "Suecia",
    "tunisia": "Tunisia",
    "tun": "Tunisia",
    "belgium": "Belgica",
    "bel": "Belgica",
    "egypt": "Egito",
    "egy": "Egito",
    "iran": "Ira",
    "ir iran": "Ira",
    "irn": "Ira",
    "new zealand": "Nova Zelandia",
    "nzl": "Nova Zelandia",
    "spain": "Espanha",
    "esp": "Espanha",
    "cape verde": "Cabo Verde",
    "cpv": "Cabo Verde",
    "saudi arabia": "Arabia Saudita",
    "ksa": "Arabia Saudita",
    "ksa": "Arabia Saudita",
    "uruguay": "Uruguai",
    "uru": "Uruguai",
    "france": "Franca",
    "fra": "Franca",
    "senegal": "Senegal",
    "sen": "Senegal",
    "iraq": "Iraque",
    "irq": "Iraque",
    "norway": "Noruega",
    "nor": "Noruega",
    "argentina": "Argentina",
    "arg": "Argentina",
    "algeria": "Argelia",
    "alg": "Argelia",
    "dza": "Argelia",
    "austria": "Austria",
    "aut": "Austria",
    "jordan": "Jordania",
    "jor": "Jordania",
    "portugal": "Portugal",
    "por": "Portugal",
    "dr congo": "Congo",
    "democratic republic of congo": "Congo",
    "congo dr": "Congo",
    "congo": "Congo",
    "cod": "Congo",
    "uzbekistan": "Uzbequistao",
    "uzb": "Uzbequistao",
    "colombia": "Colombia",
    "col": "Colombia",
    "england": "Inglaterra",
    "eng": "Inglaterra",
    "croatia": "Croacia",
    "cro": "Croacia",
    "ghana": "Gana",
    "gha": "Gana",
    "panama": "Panama",
    "pan": "Panama",
}

JOGOS = [
    {"t1": "Mexico", "t2": "Africa do Sul"},
    {"t1": "Coreia do Sul", "t2": "Rep. Tcheca"},
    {"t1": "Rep. Tcheca", "t2": "Africa do Sul"},
    {"t1": "Mexico", "t2": "Coreia do Sul"},
    {"t1": "Africa do Sul", "t2": "Coreia do Sul"},
    {"t1": "Mexico", "t2": "Rep. Tcheca"},
    {"t1": "Canada", "t2": "Bosnia"},
    {"t1": "Catar", "t2": "Suica"},
    {"t1": "Suica", "t2": "Bosnia"},
    {"t1": "Canada", "t2": "Catar"},
    {"t1": "Suica", "t2": "Canada"},
    {"t1": "Bosnia", "t2": "Catar"},
    {"t1": "Brasil", "t2": "Marrocos"},
    {"t1": "Haiti", "t2": "Escocia"},
    {"t1": "Escocia", "t2": "Marrocos"},
    {"t1": "Brasil", "t2": "Haiti"},
    {"t1": "Escocia", "t2": "Brasil"},
    {"t1": "Marrocos", "t2": "Haiti"},
    {"t1": "EUA", "t2": "Paraguai"},
    {"t1": "Australia", "t2": "Turquia"},
    {"t1": "Turquia", "t2": "Paraguai"},
    {"t1": "EUA", "t2": "Australia"},
    {"t1": "Turquia", "t2": "EUA"},
    {"t1": "Paraguai", "t2": "Australia"},
    {"t1": "Alemanha", "t2": "Curacao"},
    {"t1": "Costa do Marfim", "t2": "Equador"},
    {"t1": "Alemanha", "t2": "Costa do Marfim"},
    {"t1": "Equador", "t2": "Curacao"},
    {"t1": "Equador", "t2": "Alemanha"},
    {"t1": "Curacao", "t2": "Costa do Marfim"},
    {"t1": "Holanda", "t2": "Japao"},
    {"t1": "Suecia", "t2": "Tunisia"},
    {"t1": "Tunisia", "t2": "Japao"},
    {"t1": "Holanda", "t2": "Suecia"},
    {"t1": "Japao", "t2": "Suecia"},
    {"t1": "Tunisia", "t2": "Holanda"},
    {"t1": "Belgica", "t2": "Egito"},
    {"t1": "Ira", "t2": "Nova Zelandia"},
    {"t1": "Belgica", "t2": "Ira"},
    {"t1": "Nova Zelandia", "t2": "Egito"},
    {"t1": "Egito", "t2": "Ira"},
    {"t1": "Nova Zelandia", "t2": "Belgica"},
    {"t1": "Espanha", "t2": "Cabo Verde"},
    {"t1": "Arabia Saudita", "t2": "Uruguai"},
    {"t1": "Espanha", "t2": "Arabia Saudita"},
    {"t1": "Uruguai", "t2": "Cabo Verde"},
    {"t1": "Cabo Verde", "t2": "Arabia Saudita"},
    {"t1": "Uruguai", "t2": "Espanha"},
    {"t1": "Franca", "t2": "Senegal"},
    {"t1": "Iraque", "t2": "Noruega"},
    {"t1": "Franca", "t2": "Iraque"},
    {"t1": "Noruega", "t2": "Senegal"},
    {"t1": "Franca", "t2": "Noruega"},
    {"t1": "Senegal", "t2": "Iraque"},
    {"t1": "Argentina", "t2": "Argelia"},
    {"t1": "Austria", "t2": "Jordania"},
    {"t1": "Argentina", "t2": "Austria"},
    {"t1": "Jordania", "t2": "Argelia"},
    {"t1": "Argelia", "t2": "Austria"},
    {"t1": "Jordania", "t2": "Argentina"},
    {"t1": "Portugal", "t2": "Congo"},
    {"t1": "Uzbequistao", "t2": "Colombia"},
    {"t1": "Portugal", "t2": "Uzbequistao"},
    {"t1": "Colombia", "t2": "Congo"},
    {"t1": "Colombia", "t2": "Portugal"},
    {"t1": "Congo", "t2": "Uzbequistao"},
    {"t1": "Inglaterra", "t2": "Croacia"},
    {"t1": "Gana", "t2": "Panama"},
    {"t1": "Inglaterra", "t2": "Gana"},
    {"t1": "Panama", "t2": "Croacia"},
    {"t1": "Panama", "t2": "Inglaterra"},
    {"t1": "Croacia", "t2": "Gana"},
]

RESULTADOS_FIXOS = {
    "0": [2, 0],
    "1": [2, 1],
    "6": [1, 1],
    "18": [4, 1],
}


def normalize(name):
    s = unicodedata.normalize('NFD', name.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z ]', '', s).strip()
    mapped = NAME_MAP.get(s)
    if mapped:
        return mapped
    for key, val in NAME_MAP.items():
        if key in s or s in key:
            return val
    return s


def find_jogo(t1, t2):
    for idx, j in enumerate(JOGOS):
        if j["t1"] == t1 and j["t2"] == t2:
            return idx, False
        if j["t1"] == t2 and j["t2"] == t1:
            return idx, True
    return None, None


def main():
    results = dict(RESULTADOS_FIXOS)

    key = os.environ.get("FOOTBALL_DATA_KEY", "")
    if key:
        try:
            url = "https://api.football-data.org/v4/competitions/WC/matches?status=FINISHED"
            req = urllib.request.Request(url, headers={"X-Auth-Token": key})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
                count = 0
                for m in data.get("matches", []):
                    t1 = normalize(m.get("homeTeam", {}).get("name", ""))
                    t2 = normalize(m.get("awayTeam", {}).get("name", ""))
                    g1 = m.get("score", {}).get("fullTime", {}).get("home")
                    g2 = m.get("score", {}).get("fullTime", {}).get("away")
                    if g1 is None or g2 is None:
                        continue
                    idx, inv = find_jogo(t1, t2)
                    if idx is not None:
                        results[str(idx)] = [g2, g1] if inv else [g1, g2]
                        count = count + 1
                        print("Jogo " + str(idx) + ": " + t1 + " x " + t2 + " = " + str(g1) + "x" + str(g2))
                print("Total via API: " + str(count) + " jogos")
        except Exception as e:
            print("API erro: " + str(e))
    else:
        print("Sem chave API, usando apenas resultados fixos")

    os.makedirs("data", exist_ok=True)
    output = {
        "resultados": {
            "fase1": results,
            "oitavas": {},
            "quartas": {},
            "semi": {},
            "final": {}
        },
        "updated_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    with open("data/results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("results.json atualizado com " + str(len(results)) + " jogos!")


if __name__ == "__main__":
    main()
