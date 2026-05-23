#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('codigo_mesa'):
        continue
    parts = line.split(',')
    if len(parts) < 6:
        continue
    partido = parts[3].strip()
    votos = parts[4].strip()
    try:
        votos = int(votos)
    except:
        continue
    if partido in ('VOTOS NULOS', 'VOTOS EN BLANCO'):
        continue
    print(f"{partido}\t{votos}")
