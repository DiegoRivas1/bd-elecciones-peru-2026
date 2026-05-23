import requests
import json
import time

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "referer": "https://resultadoelectoral.onpe.gob.pe/main/resumen",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}
cookies = {
    "_ga": "GA1.1.2006958363.1776058733",
    "_ga_7X9XC2V582": "GS2.1.s1779548405$o19$g1$t1779549089$j60$l0$h544642402",
}

BASE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend"
PARAMS = "?idEleccion=10&idAmbitoGeografico=1"

ubigeos = {}  # ubigeo → {nombre, tipo, padre}

# 1. Departamentos
r = requests.get(f"{BASE}/ubigeos/departamentos{PARAMS}", headers=headers, cookies=cookies)
departamentos = r.json()['data']
print(f"Departamentos: {len(departamentos)}")

for dpto in departamentos:
    id_dpto = dpto['ubigeo']
    nombre_dpto = dpto['nombre']
    ubigeos[id_dpto] = {"nombre": nombre_dpto, "tipo": "departamento", "departamento": nombre_dpto, "provincia": "", "distrito": ""}

    # 2. Provincias de cada departamento
    r = requests.get(f"{BASE}/ubigeos/provincias{PARAMS}&idUbigeoDepartamento={id_dpto}", headers=headers, cookies=cookies)
    if not r.json().get('data'):
        continue
    provincias = r.json()['data']

    for prov in provincias:
        id_prov = prov['ubigeo']
        nombre_prov = prov['nombre']
        ubigeos[id_prov] = {"nombre": nombre_prov, "tipo": "provincia", "departamento": nombre_dpto, "provincia": nombre_prov, "distrito": ""}

        # 3. Distritos de cada provincia
        r2 = requests.get(f"{BASE}/ubigeos/distritos{PARAMS}&idUbigeoProvincia={id_prov}", headers=headers, cookies=cookies)
        if not r2.json().get('data'):
            continue
        distritos = r2.json()['data']

        for dist in distritos:
            id_dist = dist['ubigeo']
            nombre_dist = dist['nombre']
            ubigeos[id_dist] = {"nombre": nombre_dist, "tipo": "distrito", "departamento": nombre_dpto, "provincia": nombre_prov, "distrito": nombre_dist}

        time.sleep(0.1)
    time.sleep(0.2)
    print(f"  {nombre_dpto}: {len(provincias)} provincias procesadas")

# Guardar JSON
with open('/home/ec2-user/ubigeos_onpe.json', 'w', encoding='utf-8') as f:
    json.dump(ubigeos, f, ensure_ascii=False, indent=2)

print(f"\nTotal ubigeos descargados: {len(ubigeos)}")
print("Verificando claves conocidas:")
for k in ['040000','040100','040103','040127','140000','140100','140101']:
    if k in ubigeos:
        print(f"  {k} → {ubigeos[k]['nombre']}")
