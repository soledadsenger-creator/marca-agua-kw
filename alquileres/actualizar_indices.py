"""Baja los índices oficiales y arma indices.json (copia de respaldo de la calculadora).

La página primero los pide en vivo al BCRA y a datos.gob.ar; este archivo es lo que usa
si esas fuentes no responden. Lo corre solo una acción de GitHub todos los días.

Fuentes:
  ICL  -> BCRA, variable 40 (diaria)
  CER  -> BCRA, variable 30 (diaria)
  UVA  -> BCRA, variable 31 (diaria)
  Dólar -> BCRA, variable 5 (tipo de cambio mayorista, Com. A 3500) — lo usa el simulador hipotecario
  IPC  -> INDEC vía datos.gob.ar, serie 148.3_INIVELNAL_DICI_M_26 (mensual, nivel general)
"""
import json
import os
import urllib.request
from datetime import date, datetime, timezone

DESDE = "2019-01-01"
BCRA = {"icl": 40, "cer": 30, "uva": 31, "dolar": 5}
IPC_SERIE = "148.3_INIVELNAL_DICI_M_26"
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indices.json")


def leer(url):
    req = urllib.request.Request(url, headers={"User-Agent": "kw-calculadora-alquileres"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def bcra(var):
    hasta = date.today().replace(year=date.today().year + 1).isoformat()
    datos, offset = {}, 0
    while True:
        url = (f"https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/{var}"
               f"?desde={DESDE}&hasta={hasta}&limit=3000&offset={offset}")
        d = leer(url)
        filas = d["results"][0]["detalle"] if d.get("results") else []
        for f in filas:
            datos[f["fecha"]] = f["valor"]
        total = d["metadata"]["resultset"]["count"]
        offset += len(filas)
        if not filas or offset >= total:
            break
    return dict(sorted(datos.items()))


def ipc():
    url = (f"https://apis.datos.gob.ar/series/api/series/?ids={IPC_SERIE}"
           f"&start_date={DESDE}&limit=1000&format=json")
    d = leer(url)
    return {f[0][:7]: f[1] for f in d["data"] if f[1] is not None}


def main():
    salida = {"actualizado": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    for k, v in BCRA.items():
        salida[k] = bcra(v)
    salida["ipc"] = ipc()
    for k in ("icl", "cer", "uva", "ipc"):
        if len(salida[k]) < 12:
            raise SystemExit(f"{k}: vinieron muy pocos datos, no piso el archivo")
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, separators=(",", ":"))
    print({k: (len(v), list(v)[-1]) for k, v in salida.items() if isinstance(v, dict)})


if __name__ == "__main__":
    main()
