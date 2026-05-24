import sys
import subprocess
sys.path.insert(0, '/home/ec2-user')
from ubigeos import get_full

nivel  = sys.argv[1] if len(sys.argv) > 1 else "departamento"
codigo = sys.argv[2] if len(sys.argv) > 2 else "04"
carpeta = sys.argv[3] if len(sys.argv) > 3 else "/onpe/output_region_final"

result = subprocess.run(
    ["hdfs", "dfs", "-cat", f"{carpeta}/part-00000"],
    capture_output=True, text=True
)

votos = {}
for line in result.stdout.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) != 3:
        continue
    ubigeo, partido, v = parts
    try:
        v = int(v)
    except:
        continue
    if nivel == "departamento" and ubigeo[:2] == codigo[:2].zfill(2):
        votos[partido] = votos.get(partido, 0) + v
    elif nivel == "provincia" and ubigeo[:4] == codigo[:4].zfill(4):
        votos[partido] = votos.get(partido, 0) + v
    elif nivel == "distrito" and ubigeo == codigo.zfill(6):
        votos[partido] = votos.get(partido, 0) + v

codigo_full = codigo.zfill(6) if nivel == "distrito" else (codigo.zfill(4) + "00" if nivel == "provincia" else codigo.zfill(2) + "0000")
lugar = get_full(codigo_full)

print(f"\n=== Resultados por {nivel.upper()}: {lugar} ===")
print(f"    (Fuente: {carpeta})\n")
for partido, v in sorted(votos.items(), key=lambda x: x[1], reverse=True):
    print(f"  {partido:50s} {v:>10,}")
