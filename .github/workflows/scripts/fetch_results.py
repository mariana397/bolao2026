Cola isso no corpo do arquivo:

```python
#!/usr/bin/env python3
import json, re, urllib.request, os, datetime

NAME_MAP = {
    "mexico":"México","south africa":"África do Sul","africa do sul":"África do Sul",
    "korea republic":"Coreia do Sul","south korea":"Coreia do Sul",
    "czech republic":"Rep. Tcheca","czechia":"Rep. Tcheca",
    "canada":"Canadá","bosnia and herzegovina":"Bósnia",
    "qatar":"Catar","switzerland":"Suíça",
    "brazil":"Brasil","morocco":"Marrocos",
    "haiti":"Haiti","scotland":"Escócia",
    "united states":"EUA","usa":"EUA",
    "paraguay":"Paraguai","australia":"Austrália",
    "turkey":"Turquia","germany":"Alemanha",
    "curacao":"Curaçao","cote d'ivoire":"Costa do Marfim",
    "ivory coast":"Costa do Marfim","ecuador":"Equador",
    "netherlands":"Holanda","japan":"Japão",
    "sweden":"Suécia","tunisia":"Tunísia",
    "belgium":"Bélgica","egypt":"Egito",
    "iran":"Irã","new zealand":"Nova Zelândia",
    "spain":"Espanha","cape verde":"Cabo Verde",
    "saudi arabia":"Arábia Saudita","uruguay":"Uruguai",
    "france":"França","senegal":"Senegal",
    "iraq":"Iraque","norway":"Noruega",
    "argentina":"Argentina","algeria":"Argélia",
    "austria":"Áustria","jordan":"Jordânia",
    "portugal":"Portugal","dr congo":"Congo","congo":"Congo",
    "uzbekistan":"Uzbequistão","colombia":"Colômbia",
    "england":"Inglaterra","croatia":"Croácia",
    "ghana":"Gana","panama":"Panamá",
}

JOGOS = [
    {"t1":"México","t2":"África do Sul"},{"t1":"Coreia do Sul","t2":"Rep. Tcheca"},
    {"t1":"Rep. Tcheca","t2":"África do Sul"},{"t1":"México","t2":"Coreia do Sul"},
    {"t1":"África do Sul","t2":"Coreia do Sul"},{"t1":"México","t2":"Rep. Tcheca"},
    {"t1":"Canadá","t2":"Bósnia"},{"t1":"Catar","t2":"Suíça"},
    {"t1":"Suíça","t2":"Bósnia"},{"t1":"Canadá","t2":"Catar"},
    {"t1":"Suíça","t2":"Canadá"},{"t1":"Bósnia","t2":"Catar"},
    {"t1":"Brasil","t2":"Marrocos"},{"t1":"Haiti","t2":"Escócia"},
    {"t1":"Escócia","t2":"Marrocos"},{"t1":"Brasil","t2":"Haiti"},
    {"t1":"Escócia","t2":"Brasil"},{"t1":"Marrocos","t2":"Haiti"},
    {"t1":"EUA","t2":"Paraguai"},{"t1":"Austrália","t2":"Turquia"},
    {"t1":"Turquia","t2":"Paraguai"},{"t1":"EUA","t2":"Austrália"},
    {"t1":"Turquia","t2":"EUA"},{"t1":"Paraguai","t2":"Austrália"},
    {"t1":"Alemanha","t2":"Curaçao"},{"t1":"Costa do Marfim","t2":"Equador"},
    {"t1":"Alemanha","t2":"Costa do Marfim"},{"t1":"Equador","t2":"Curaçao"},
    {"t1":"Equador","t2":"Alemanha"},{"t1":"Curaçao","t2":"Costa do Marfim"},
    {"t1":"Holanda","t2":"Japão"},{"t1":"Suécia","t2":"Tunísia"},
    {"t1":"Tunísia","t2":"Japão"},{"t1":"Holanda","t2":"Suécia"},
    {"t1":"Japão","t2":"Suécia"},{"t1":"Tunísia","t2":"Holanda"},
    {"t1":"Bélgica","t2":"Egito"},{"t1":"Irã","t2":"Nova Zelândia"},
    {"t1":"Bélgica","t2":"Irã"},{"t1":"Nova Zelândia","t2":"Egito"},
    {"t1":"Egito","t2":"Irã"},{"t1":"Nova Zelândia","t2":"Bélgica"},
    {"t1":"Espanha","t2":"Cabo Verde"},{"t1":"Arábia Saudita","t2":"Uruguai"},
    {"t1":"Espanha","t2":"Arábia Saudita"},{"t1":"Uruguai","t2":"Cabo Verde"},
    {"t1":"Cabo Verde","t2":"Arábia Saudita"},{"t1":"Uruguai","t2":"Espanha"},
    {"t1":"França","t2":"Senegal"},{"t1":"Iraque","t2":"Noruega"},
    {"t1":"França","t2":"Iraque"},{"t1":"Noruega","t2":"Senegal"},
    {"t1":"França","t2":"Noruega"},{"t1":"Senegal","t2":"Iraque"},
    {"t1":"Argentina","t2":"Argélia"},{"t1":"Áustria","t2":"Jordânia"},
    {"t1":"Argentina","t2":"Áustria"},{"t1":"Jordânia","t2":"Argélia"},
    {"t1":"Argélia","t2":"Áustria"},{"t1":"Jordânia","t2":"Argentina"},
    {"t1":"Portugal","t2":"Congo"},{"t1":"Uzbequistão","t2":"Colômbia"},
    {"t1":"Portugal","t2":"Uzbequistão"},{"t1":"Colômbia","t2":"Congo"},
    {"t1":"Colômbia","t2":"Portugal"},{"t1":"Congo","t2":"Uzbequistão"},
    {"t1":"Inglaterra","t2":"Croácia"},{"t1":"Gana","t2":"Panamá"},
    {"t1":"Inglaterra","t2":"Gana"},{"t1":"Panamá","t2":"Croácia"},
    {"t1":"Panamá","t2":"Inglaterra"},{"t1":"Croácia","t2":"Gana"},
]

def normalize(name):
    import unicodedata
    s = unicodedata.normalize('NFD', name.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z ]', '', s).strip()
    return NAME_MAP.get(s, name)

def find_jogo(t1, t2):
    for idx, j in enumerate(JOGOS):
        if j["t1"] == t1 and j["t2"] == t2: return idx, False
        if j["t1"] == t2 and j["t2"] == t1: return idx, True
    return None, None

def main():
    results = {"0":[2,0], "1":[2,1]}
    
    key = os.environ.get("FOOTBALL_DATA_KEY", "")
    if key:
        try:
            url = "https://api.football-data.org/v4/competitions/WC/matches?status=FINISHED"
            req = urllib.request.Request(url, headers={"X-Auth-Token": key})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                for m in data.get("matches", []):
                    t1 = normalize(m.get("homeTeam",{}).get("name",""))
                    t2 = normalize(m.get("awayTeam",{}).get("name",""))
                    g1 = m.get("score",{}).get("fullTime",{}).get("home")
                    g2 = m.get("score",{}).get("fullTime",{}).get("away")
                    if g1 is None or g2 is None: continue
                    idx, inv = find_jogo(t1, t2)
                    if idx is not None:
                        results[str(idx)] = [g2,g1] if inv else [g1,g2]
            print(f"API ok: {len(results)} jogos")
        except Exception as e:
            print(f"API erro: {e}")

    os.makedirs("data", exist_ok=True)
    with open("data/results.json", "w", encoding="utf-8") as f:
        json.dump({
            "resultados": {"fase1": results, "oitavas":{}, "quartas":{}, "semi":{}, "final":{}},
            "updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }, f, ensure_ascii=False, indent=2)
    print("results.json atualizado!")

if __name__ == "__main__":
    main()
```

Depois de colar clica **"Commit changes"** → **"Commit changes"** de novo.

Quando confirmar, vamos testar se o robozinho roda — é só um clique.
