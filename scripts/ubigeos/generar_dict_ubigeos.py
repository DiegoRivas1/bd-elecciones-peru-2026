import json

with open('/home/ec2-user/ubigeos_onpe.json', 'r', encoding='utf-8') as f:
    ubigeos = json.load(f)

lines = ['# Diccionario de Ubigeos - Fuente: API ONPE Elecciones 2026\n']
lines.append('# Total: {} ubigeos (departamentos, provincias y distritos)\n\n'.format(len(ubigeos)))
lines.append('UBIGEOS = {\n')

for codigo, data in sorted(ubigeos.items()):
    nombre = data['nombre']
    tipo = data['tipo']
    dpto = data['departamento']
    prov = data['provincia']
    dist = data['distrito']
    lines.append(f'    "{codigo}": {{"nombre": "{nombre}", "tipo": "{tipo}", "departamento": "{dpto}", "provincia": "{prov}", "distrito": "{dist}"}},\n')

lines.append('}\n\n')
lines.append('''
def get_lugar(ubigeo):
    """Retorna info completa dado un ubigeo"""
    return UBIGEOS.get(str(ubigeo).zfill(6), {
        "nombre": "Desconocido", "tipo": "", 
        "departamento": "Desconocido", "provincia": "Desconocido", "distrito": "Desconocido"
    })

def get_nombre(ubigeo):
    """Retorna solo el nombre del lugar"""
    return get_lugar(ubigeo)["nombre"]

def get_departamento(ubigeo):
    """Retorna nombre del departamento dado cualquier ubigeo"""
    data = get_lugar(ubigeo)
    return data["departamento"]

def get_provincia(ubigeo):
    """Retorna nombre de la provincia dado cualquier ubigeo"""
    return get_lugar(ubigeo)["provincia"]

def get_distrito(ubigeo):
    """Retorna nombre del distrito dado ubigeo de 6 digitos"""
    return get_lugar(ubigeo)["distrito"]

def get_full(ubigeo):
    """Retorna string completo: Distrito, Provincia, Departamento"""
    d = get_lugar(ubigeo)
    if d["tipo"] == "distrito":
        return f"{d['distrito']}, {d['provincia']}, {d['departamento']}"
    elif d["tipo"] == "provincia":
        return f"{d['provincia']}, {d['departamento']}"
    else:
        return d["departamento"]

if __name__ == "__main__":
    # Prueba
    for cod in ["040000","040100","040103","040127","140101","200000"]:
        print(f"{cod} → {get_full(cod)}")
''')

with open('/home/ec2-user/ubigeos.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"✅ ubigeos.py generado con {len(ubigeos)} entradas")
