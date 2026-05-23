#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('codigo_mesa'):
        continue
    parts = line.split(',')
    if len(parts) < 6:
        continue
    ubigeo  = parts[1].strip()
    partido = parts[3].strip()
    votos   = parts[4].strip()
    try:
        votos = int(votos)
    except:
        continue
    if partido in ('VOTOS NULOS', 'VOTOS EN BLANCO', 'VOTOS IMPUGNADOS'):
        continue
    # Clave única: ubigeo|||partido para que el sort agrupe correctamente
    print(f"{ubigeo}|||{partido}\t{votos}")
