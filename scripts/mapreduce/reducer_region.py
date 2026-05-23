#!/usr/bin/env python3
import sys

current_key = None
total = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    key, votos = parts[0], parts[1]
    try:
        votos = int(votos)
    except:
        continue
    if key == current_key:
        total += votos
    else:
        if current_key:
            ubigeo, partido = current_key.split('|||')
            print(f"{ubigeo}\t{partido}\t{total}")
        current_key = key
        total = votos

if current_key:
    ubigeo, partido = current_key.split('|||')
    print(f"{ubigeo}\t{partido}\t{total}")
