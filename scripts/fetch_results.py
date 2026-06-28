bash

cat /mnt/user-data/outputs/update_results.py
Saída

#!/usr/bin/env python3
import json, re, urllib.request, os, datetime

NAME_MAP = {
    "mexico":"México","south africa":"África do Sul","africa do sul":"África do Sul",
    "korea republic":"Coreia do Sul","south korea":"Coreia do Sul",
    "czech republic":"Rep. Tcheca","czechia":"Rep. Tcheca",
    "canada":"Canadá","bosnia and herzegovina":"Bósnia","bosnia herzegovina":"Bósnia",
    "qatar":"Catar","switzerland":"Suíça",
    "brazil":"Brasil","morocco":"Marrocos",
    "haiti":"Haiti","scotland":"Escócia",
    "united states":"EUA","usa":"EUA",
    "paraguay":"Paraguai","australia":"Austrália",
    "turkey":"Turquia","turkiye":"Turquia","germany":"Alemanha",
    "curacao":"Curaçao","cote d ivoire":"Costa do Marfim",
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
    "portugal":"Portugal","dr congo":"RD Congo","congo dr":"RD Congo",
    "congo":"RD Congo","democratic republic of congo":"RD Congo",
    "uzbekistan":"Uzbequistão","colombia":"Colômbia",
    "england":"Inglaterra","croatia":"Croácia",
    "ghana":"Gana","panama":"Panamá",
    "norway":"Noruega","sweden":"Suécia",
    "countries baixos":"Países Baixos","netherlands":"Países Baixos",
    "rd congo":"RD Congo",
}

# Jogos fase de grupos (72) — índice 0-71
JOGOS_GRUPOS = [
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
    {"t1":"Portugal","t2":"RD Congo"},{"t1":"Uzbequistão","t2":"Colômbia"},
    {"t1":"Portugal","t2":"Uzbequistão"},{"t1":"Colômbia","t2":"RD Congo"},
    {"t1":"Colômbia","t2":"Portugal"},{"t1":"RD Congo","t2":"Uzbequistão"},
    {"t1":"Inglaterra","t2":"Croácia"},{"t1":"Gana","t2":"Panamá"},
    {"t1":"Inglaterra","t2":"Gana"},{"t1":"Panamá","t2":"Croácia"},
    {"t1":"Panamá","t2":"Inglaterra"},{"t1":"Croácia","t2":"Gana"},
]

# Jogos 1/16 avos — na ordem do chaveamento (índice 0-15)
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

# Mapeamento de stage da API para fase do bolão
STAGE_MAP = {
    "ROUND_OF_16": "dezesseis",
    "QUARTER_FINALS": "oitavas",
    "SEMI_FINALS": "semi",
    "THIRD_PLACE": "terceiro",
    "FINAL": "final",
}

import unicodedata

def normalize(name):
    s = unicodedata.normalize('NFD', name.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z ]', '', s).strip()
    return NAME_MAP.get(s, name.title())

def find_in_list(jogos, t1, t2):
    for idx, j in enumerate(jogos):
        if j["t1"] == t1 and j["t2"] == t2: return idx, False
        if j["t1"] == t2 and j["t2"] == t1: return idx, True
    return None, None

def main():
    # Carrega results.json existente para preservar o que já foi salvo
    os.makedirs("data", exist_ok=True)
    existing = {}
    try:
        with open("data/results.json", "r", encoding="utf-8") as f:
            existing = json.load(f).get("resultados", {})
    except Exception:
        pass

    # Estrutura base preservando dados existentes
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
    if key:
        try:
            url = "https://api.football-data.org/v4/competitions/WC/matches?status=FINISHED"
            req = urllib.request.Request(url, headers={"X-Auth-Token": key})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())

            count = 0
            for m in data.get("matches", []):
                stage = m.get("stage", "")
                t1_raw = m.get("homeTeam", {}).get("name", "")
                t2_raw = m.get("awayTeam", {}).get("name", "")
                t1 = normalize(t1_raw)
                t2 = normalize(t2_raw)

                score = m.get("score", {})
                ft = score.get("fullTime", {})
                g1 = ft.get("home")
                g2 = ft.get("away")
                if g1 is None or g2 is None:
                    continue

                # Para mata-mata: usar placar do tempo normal + prorrogação (fullTime da API já inclui ET)
                # Penáltis ficam em score.penalties — ignoramos para pontuação

                if stage == "GROUP_STAGE":
                    idx, inv = find_in_list(JOGOS_GRUPOS, t1, t2)
                    if idx is not None:
                        results["fase1"][str(idx)] = [g2, g1] if inv else [g1, g2]
                        count += 1

                elif stage in STAGE_MAP:
                    fase_id = STAGE_MAP[stage]
                    jogos_fase = JOGOS_DEZESSEIS if fase_id == "dezesseis" else None
                    # Para oitavas em diante, a API retorna os times reais;
                    # buscamos na lista da fase correspondente se disponível
                    if jogos_fase:
                        idx, inv = find_in_list(jogos_fase, t1, t2)
                        if idx is not None:
                            results[fase_id][str(idx)] = [g2, g1] if inv else [g1, g2]
                            count += 1
                    else:
                        # Para quartas, semi, terceiro, final: não temos lista fixa ainda
                        # (times dependem do chaveamento dinâmico)
                        # Guardamos por ordem de jogo da fase conforme a API retorna
                        fase_jogos = results.get(fase_id, {})
                        # Usa o matchday ou id como chave temporária
                        match_id = str(m.get("id", ""))
                        fase_jogos[match_id] = {
                            "t1": t1, "t2": t2,
                            "g1": g1 if not inv else g2,
                            "g2": g2 if not inv else g1
                        }
                        results[fase_id] = fase_jogos
                        count += 1

            print(f"API ok: {count} jogos atualizados")
        except Exception as e:
            print(f"API erro: {e}")
    else:
        print("Sem chave de API — mantendo dados existentes")

    with open("data/results.json", "w", encoding="utf-8") as f:
        json.dump({
            "resultados": results,
            "updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }, f, ensure_ascii=False, indent=2)
    print("results.json atualizado!")

if __name__ == "__main__":
    main()
Concluído
O arquivo novo está certo e é
