#!/usr/bin/env python3
"""finantari_rural.json (dashboard intern) -> data.json (pagina publică). Usage: make_public_data.py <in.json> <data.json>"""
import json, sys, datetime
src = json.load(open(sys.argv[1], encoding="utf-8"))
rows = src if isinstance(src, list) else (src.get("rows") or src.get("data") or [])
today = datetime.date.today().isoformat()
cutoff = (datetime.date.today() - datetime.timedelta(days=10)).isoformat()  # apelurile expirate rămân vizibile 10 zile
pub = []
for r in rows:
    if not (r.get("titlu") and r.get("url")): continue
    if r.get("termen") and r["termen"] < cutoff: continue
    pub.append({"id": r.get("id"), "program": r.get("program"), "domeniu": r.get("domeniu"),
                "regiune": r.get("regiune"), "titlu": r.get("titlu"), "beneficiari": r.get("beneficiari"),
                "suma": r.get("suma") or r.get("sprijin"), "descriere": r.get("descriere"),
                "termen": r.get("termen"), "url": r.get("url")})
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).isoformat(timespec="seconds")
json.dump({"actualizat": now, "sursa": "Centrul de Dezvoltare SMART", "apeluri": pub},
          open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(pub), "apeluri publice")
