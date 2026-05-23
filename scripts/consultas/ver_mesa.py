import requests
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

codigo = sys.argv[1] if len(sys.argv) > 1 else "007172"
codigo = codigo.zfill(6)

url = f"https://resultadoelectoral.onpe.gob.pe/presentacion-backend/actas/buscar/mesa?codigoMesa={codigo}&idEleccion=10"
r = requests.get(url, headers=headers, cookies=cookies)
data = r.json()

if not data.get('success') or not data.get('data'):
    print(f"Mesa {codigo} no encontrada")
    sys.exit(1)

acta = data['data'][0]
print("=== INFORMACIÓN DE LA MESA ===")
print(f"Código Mesa:        {acta.get('codigoMesa')}")
print(f"Local de votación:  {acta.get('nombreLocalVotacion')}")
print(f"Ubigeo:             {acta.get('idUbigeo')}")
print(f"Electores hábiles:  {acta.get('totalElectoresHabiles')}")
print(f"Votos emitidos:     {acta.get('totalVotosEmitidos')}")
print(f"Votos válidos:      {acta.get('totalVotosValidos')}")
print(f"Estado acta:        {acta.get('descripcionEstadoActa')}")
print()
print("=== VOTOS POR PARTIDO ===")
for p in acta.get('detalle', []):
    nombre = p.get('adDescripcion', '')
    votos = p.get('adVotos') or 0
    if votos > 0:
        print(f"  {nombre}: {votos} votos")
