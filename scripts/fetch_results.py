#!/usr/bin/env python3
import json, re, urllib.request, os, datetime, unicodedata

NAME_MAP = {
    "mexico": "México",
    "south africa": "África do Sul",
    "africa do sul": "África do Sul",
    "korea republic": "Coreia do Sul",
    "south korea": "Coreia do Sul",
    "republic of korea": "Coreia do Sul",
    "czech republic": "Rep. Tcheca",
    "czechia": "Rep. Tcheca",
    "canada": "Canadá",
    "bosnia and herzegovina": "Bósnia",
    "bosnia herzegovina": "Bósnia",
    "bosnia-herzegovina": "Bósnia",
    "bosniaherzegovina": "Bósnia",
    "bosnia": "Bósnia",
    "qatar": "Catar",
    "switzerland": "Suíça",
    "brazil": "Brasil",
    "morocco": "Marrocos",
    "haiti": "Haiti",
    "scotland": "Escócia",
    "united states": "EUA",
    "united states of america": "EUA",
    "usa": "EUA",
    "estados unidos": "EUA",
    "paraguay": "Paraguai",
    "australia": "Austrália",
    "turkey": "Turquia",
    "turkiye": "Turquia",
    "germany": "Alemanha",
    "curacao": "Curaçao",
    "cote d ivoire": "Costa do Marfim",
    "ivory coast": "Costa do Marfim",
    "ecuador": "Equador",
    "netherlands": "Holanda",
    "paises baixos": "Holanda",
    "holland": "Holanda",
    "japan": "Japão",
    "sweden": "Suécia",
    "tunisia": "Tunísia",
    "belgium": "Bélgica",
    "egypt": "Egito",
    "iran": "Irã",
    "ir iran": "Irã",
    "new zealand": "Nova Zelândia",
    "spain": "Espanha",
    "cape verde": "Cabo Verde",
    "cape verde islands": "Cabo Verde",
    "saudi arabia": "Arábia Saudita",
    "uruguay": "Uruguai",
    "france": "França",
    "senegal": "Senegal",
    "iraq": "Iraque",
    "norway": "Noruega",
    "argentina": "Argentina",
    "algeria": "Argélia",
    "austria": "Áustria",
    "jordan": "Jordânia",
    "portugal": "Portugal",
    "dr congo": "RD Congo",
    "congo dr": "RD Congo",
    "democratic republic of congo": "RD Congo",
    "congo": "RD Congo",
    "uzbekistan": "Uzbequistão",
    "colombia": "Colômbia",
    "england": "Inglaterra",
    "croatia": "Croácia",
    "ghana": "Gana",
    "panama": "Panamá",
}

JOGOS_GRUPOS = [
    {"t1":"México","t2":"África do Sul"},
    {"t1":"Coreia do Sul","t2":"Rep. Tcheca"},
    {"t1":"Rep. Tcheca","t2":"África do Sul"},
    {"t1":"México","t2":"Coreia do Sul"},
    {"t1":"África do Sul","t2":"Coreia do Sul"},
    {"t1":"México","t2":"Rep. Tcheca"},
    {"t1":"Canadá","t2":"Bósnia"},
    {"t1":"Catar","t2":"Suíça"},
    {"t1":"Suíça","t2":"Bósnia"},
    {"t1":"Canadá","t2":"Catar"},
    {"t1":"Suíça","t2":"Canadá"},
    {"t1":"Bósnia","t2":"Catar"},
    {"t1":"Brasil","t2":"Marrocos"},
    {"t1":"Haiti","t2":"Escócia"},
    {"t1":"Escócia","t2":"Marrocos"},
    {"t1":"Brasil","t2":"Haiti"},
    {"t1":"Escócia","t2":"Brasil"},
    {"t1":"Marrocos","t2":"Haiti"},
    {"t1":"EUA","t2":"Paraguai"},
    {"t1":"Austrália","t2":"Turquia"},
    {"t1":"Turquia","t2":"Paraguai"},
    {"t1":"EUA","t2":"Austrália"},
    {"t1":"Turquia","t2":"EUA"},
    {"t1":"Paraguai","t2":"Austrália"},
    {"t1":"Alemanha","t2":"Curaçao"},
    {"t1":"Costa do Marfim","t2":"Equador"},
    {"t1":"Alemanha","t2":"Costa do Marfim"},
    {"t1":"Equador","t2":"Curaçao"},
    {"t1":"Equador","t2":"Alemanha"},
    {"t1":"Curaçao","t2":"Costa do Marfim"},
    {"t1":"Holanda","t2":"Japão"},
    {"t1":"Suécia","t2":"Tunísia"},
    {"t1":"Tunísia","t2":"Japão"},
    {"t1":"Holanda","t2":"Suécia"},
    {"t1":"Japão","t2":"Suécia"},
    {"t1":"Tunísia","t2":"Holanda"},
    {"t1":"Bélgica","t2":"Egito"},
    {"t1":"Irã","t2":"Nova Zelândia"},
    {"t1":"Bélgica","t2":"Irã"},
    {"t1":"Nova Zelândia","t2":"Egito"},
    {"t1":"Egito","t2":"Irã"},
    {"t1":"Nova Zelândia","t2":"Bélgica"},
    {"t1":"Espanha","t2":"Cabo Verde"},
    {"t1":"Arábia Saudita","t2":"Uruguai"},
    {"t1":"Espanha","t2":"Arábia Saudita"},
    {"t1":"Uruguai","t2":"Cabo Verde"},
    {"t1":"Cabo Verde","t2":"Arábia Saudita"},
    {"t1":"Uruguai","t2":"Espanha"},
    {"t1":"França","t2":"Senegal"},
    {"t1":"Iraque","t2":"Noruega"},
    {"t1":"França","t2":"Iraque"},
    {"t1":"Noruega","t2":"Senegal"},
    {"t1":"França","t2":"Noruega"},
    {"t1":"Senegal","t2":"Iraque"},
    {"t1":"Argentina","t2":"Argélia"},
    {"t1":"Áustria","t2":"Jordânia"},
    {"t1":"Argentina","t2":"Áustria"},
    {"t1":"Jordânia","t2":"Argélia"},
    {"t1":"Argélia","t2":"Áustria"},
    {"t1":"Jordânia","t2":"Argentina"},
    {"t1":"Portugal","t2":"RD Congo"},
    {"t1":"Uzbequistão","t2":"Colômbia"},
    {"t1":"Portugal","t2":"Uzbequistão"},
    {"t1":"Colômbia","t2":"RD Congo"},
    {"t1":"Colômbia","t2":"Portugal"},
    {"t1":"RD Congo","t2":"Uzbequistão"},
    {"t1":"Inglaterra","t2":"Croácia"},
    {"t1":"Gana","t2":"Panamá"},
    {"t1":"Inglaterra","t2":"Gana"},
    {"t1":"Panamá","t2":"Croácia"},
    {"t1":"Panamá","t2":"Inglaterra"},
    {"t1":"Croácia","t2":"Gana"},
]

JOGOS_DEZESSEIS = [
    {"t1":"África do Sul","t2":"Canadá"},
    {"t1":"Brasil","t2":"Japão"},
    {"t1":"Alemanha","t2":"Paraguai"},
    {"t1":"Países Baixos","t2":"Marrocos"},
    {"t1":"Costa do Marfim","t2":"Noruega"},
    {"t1":"França","t2":"Suécia"},
    {"t1":"México","t2":"Equador"},
    {"t1":"Inglaterra","t2":"RD Congo"},
    {"t1":"Bélgica","t2":"Senegal"},
    {"t1":"Estados Unidos","t2":"Bósnia"},
    {"t1":"Espanha","t2":"Áustria"},
    {"t1":"Portugal","t2":"Croácia"},
    {"t1":"Suíça","t2":"Argélia"},
    {"t1":"Austrália","t2":"Egito"},
    {"t1":"Argentina","t2":"Cabo Verde"},
    {"t1":"Colômbia","t2":"Gana"},
]

# Mapeamento adicional para nomes nos jogos do mata-mata
# (podem diferir dos grupos — ex: "Holanda" nos grupos vs "Países Baixos" no mata-mata)
MATA_MATA_NAME_FIX = {
    "Holanda": "Países Baixos",
    "EUA": "Estados Unidos",
}

STAGE_MAP = {
    "LAST_32": "dezesseis",
    "ROUND_OF_32": "dezesseis",
    "ROUND_OF_16": "oitavas",
    "LAST_16": "oitavas",
    "QUARTER_FINALS": "quartas",
    "LAST_8": "quartas",
    "SEMI_FINALS": "semi",
    "LAST_4": "semi",
    "THIRD_PLACE": "terceiro",
    "FINAL": "final",
}

def normalize(name):
    s = unicodedata.normalize('NFD', name.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.replace("-", " ")
    s = re.sub(r'[^a-z ]', '', s).strip()
    return NAME_MAP.get(s, name)

def find_in_list(jogos, t1, t2):
    # busca direta
    for idx, j in enumerate(jogos):
        if j["t1"] == t1 and j["t2"] == t2:
            return idx, False
        if j["t1"] == t2 and j["t2"] == t1:
            return idx, True
    # busca sem acento (fallback)
    def sem_acento(s):
        s = unicodedata.normalize('NFD', s.lower())
        return ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    t1n, t2n = sem_acento(t1), sem_acento(t2)
    for idx, j in enumerate(jogos):
        j1n, j2n = sem_acento(j["t1"]), sem_acento(j["t2"])
        if j1n == t1n and j2n == t2n:
            return idx, False
        if j1n == t2n and j2n == t1n:
            return idx, True
    return None, None

def main():
    os.makedirs("data", exist_ok=True)
    existing = {}
    try:
        with open("data/results.json", "r", encoding="utf-8") as f:
            existing = json.load(f).get("resultados", {})
    except Exception:
        pass

    results = {
        "fase1":     existing.get("fase1", {}),
        "dezesseis": existing.get("dezesseis", {}),
        "oitavas":   existing.get("oitavas", {}),
        "quartas":   existing.get("quartas", {}),
        "semi":      existing.get("semi", {}),
        "terceiro":  existing.get("terceiro", {}),
        "final":     existing.get("final", {}),
    }

    key = os.environ.get("FOOTBALL_DATA_KEY", "")
    if not key:
        print("Sem chave de API — mantendo dados existentes")
    else:
        try:
            url = "https://api.football-data.org/v4/competitions/WC/matches?status=FINISHED"
            req = urllib.request.Request(url, headers={"X-Auth-Token": key})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())

            count = 0
            missed = []
            stages_vistos = set()
            for m in data.get("matches", []):
                stage = m.get("stage", "")
                stages_vistos.add(stage)
                t1 = normalize(m.get("homeTeam", {}).get("name", ""))
                t2 = normalize(m.get("awayTeam", {}).get("name", ""))
                score = m.get("score", {})
                duration = score.get("duration", "REGULAR")
                if duration == "PENALTY_SHOOTOUT":
                    # Jogo foi a penaltis: regularTime + extraTime = placar correto
                    reg = score.get("regularTime", {})
                    ext = score.get("extraTime", {})
                    r1 = reg.get("home", 0) or 0
                    r2 = reg.get("away", 0) or 0
                    e1 = ext.get("home", 0) or 0
                    e2 = ext.get("away", 0) or 0
                    g1 = r1 + e1
                    g2 = r2 + e2
                elif duration == "EXTRA_TIME":
                    # Jogo foi a prorrogacao mas nao a penaltis: fullTime ja e correto
                    ft = score.get("fullTime", {})
                    g1 = ft.get("home")
                    g2 = ft.get("away")
                else:
                    # Jogo terminou no tempo normal: fullTime e correto
                    ft = score.get("fullTime", {})
                    g1 = ft.get("home")
                    g2 = ft.get("away")
                if g1 is None or g2 is None:
                    continue

                if stage == "GROUP_STAGE":
                    idx, inv = find_in_list(JOGOS_GRUPOS, t1, t2)
                    if idx is not None:
                        results["fase1"][str(idx)] = [g2, g1] if inv else [g1, g2]
                        count += 1
                    else:
                        missed.append("GRUPO: " + t1 + " x " + t2)

                elif stage in STAGE_MAP:
                    fase_id = STAGE_MAP[stage]
                    print("  MATA-MATA " + stage + ": " + t1 + " x " + t2 + " = " + str(g1) + "x" + str(g2))
                    if fase_id == "dezesseis":
                        # aplica fix de nomes para o mata-mata
                        t1m = MATA_MATA_NAME_FIX.get(t1, t1)
                        t2m = MATA_MATA_NAME_FIX.get(t2, t2)
                        idx, inv = find_in_list(JOGOS_DEZESSEIS, t1m, t2m)
                        if idx is not None:
                            results[fase_id][str(idx)] = [g2, g1] if inv else [g1, g2]
                            count += 1
                        else:
                            missed.append("DEZESSEIS: " + t1 + " x " + t2)
                    else:
                        match_id = str(m.get("id", ""))
                        results[fase_id][match_id] = {"t1": t1, "t2": t2, "g1": g1, "g2": g2}
                        count += 1

            print("API ok: " + str(count) + " jogos atualizados")
            print("  STAGES vistos na API: " + ", ".join(sorted(stages_vistos)))
            for miss in missed:
                print("  MISS: " + miss)

        except Exception as e:
            print("API erro: " + str(e))

    with open("data/results.json", "w", encoding="utf-8") as f:
        json.dump({
            "resultados": results,
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }, f, ensure_ascii=False, indent=2)
    print("results.json atualizado!")

if __name__ == "__main__":
    main()
