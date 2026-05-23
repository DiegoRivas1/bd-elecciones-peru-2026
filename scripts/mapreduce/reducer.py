#!/usr/bin/env python3
import sys

current_partido = None
total = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    partido, votos = parts[0], parts[1]
    try:
        votos = int(votos)
    except:
        continue
    if partido == current_partido:
        total += votos
    else:
        if current_partido:
            print(f"{current_partido}\t{total}")
        current_partido = partido
        total = votos

if current_partido:
    print(f"{current_partido}\t{total}")
