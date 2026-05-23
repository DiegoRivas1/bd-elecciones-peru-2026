import requests
import csv
import time
import sys

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "es-ES,es;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
}
cookies = {
    "_ga": "GA1.1.2006958363.1776058733",
    "_ga_7X9XC2V582": "GS2.1.s1776213407$o5$g1$t1776213434$j33$l0$h2049449661",
}

inicio = int(sys.argv[1]) if len(sys.argv) > 1 else 1
fin    = int(sys.argv[2]) if len(sys.argv) > 2 else 92766

def obtener_acta(codigo_mesa):
    url = f"https://resultadoelectoral.onpe.gob.pe/presentacion-backend/actas/buscar/mesa?codigoMesa={codigo_mesa}&idEleccion=10"
    try:
        r = requests.get(url, headers=headers, cookies=cookies, timeout=15)
        return r.json()
    except:
        return None

codigos = [str(i).zfill(6) for i in range(inicio, fin + 1)]
procesadas = 0
encontradas = 0

with open('/home/ec2-user/votos_final.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['codigo_mesa', 'ubigeo', 'local_votacion', 'partido', 'votos', 'votos_validos_mesa'])

    for codigo in codigos:
        data = obtener_acta(codigo)
        procesadas += 1

        if not data or not data.get('success') or not data.get('data'):
            if procesadas % 500 == 0:
                print(f"[{procesadas}/{len(codigos)}] Mesas con datos: {encontradas}")
            time.sleep(0.1)
            continue

        acta = data['data'][0]
        ubigeo = str(acta.get('idUbigeo', '')).zfill(6)  # ← con zfill
        local = acta.get('nombreLocalVotacion', '')
        votos_validos = acta.get('totalVotosValidos', 0)
        estado = acta.get('descripcionEstadoActa', '')

        if estado != 'Contabilizada':
            continue

        encontradas += 1
        for partido in acta.get('detalle', []):
            nombre = partido.get('adDescripcion', '')
            votos = partido.get('adVotos') or 0
            writer.writerow([codigo, ubigeo, local, nombre, votos, votos_validos])

        if procesadas % 100 == 0:
            print(f"[{procesadas}/{len(codigos)}] Mesas contabilizadas: {encontradas}")
        time.sleep(0.2)

print(f"\n Completado: {encontradas} mesas de {procesadas} consultadas")
