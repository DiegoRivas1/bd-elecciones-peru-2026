from flask import Flask, jsonify, request, render_template_string
import subprocess, sys
sys.path.insert(0, '/home/ec2-user')
from ubigeos import get_full, UBIGEOS

app = Flask(__name__)

def leer_nacional():
    result = subprocess.run(["hdfs","dfs","-cat","/onpe/output_nacional_final/part-00000"],capture_output=True,text=True)
    datos = []
    for line in result.stdout.strip().split('\n'):
        parts = line.split('\t')
        if len(parts)==2:
            try: datos.append({"partido":parts[0],"votos":int(parts[1])})
            except: pass
    return sorted(datos, key=lambda x: x['votos'], reverse=True)

def leer_region(nivel, codigo):
    result = subprocess.run(["hdfs","dfs","-cat","/onpe/output_region_final/part-00000"],capture_output=True,text=True)
    votos = {}
    for line in result.stdout.strip().split('\n'):
        parts = line.split('\t')
        if len(parts)!=3: continue
        ubigeo, partido, v = parts
        try: v = int(v)
        except: continue
        if nivel=="departamento" and ubigeo[:2]==codigo[:2].zfill(2):
            votos[partido] = votos.get(partido,0)+v
        elif nivel=="provincia" and ubigeo[:4]==codigo[:4].zfill(4):
            votos[partido] = votos.get(partido,0)+v
        elif nivel=="distrito" and ubigeo==codigo.zfill(6):
            votos[partido] = votos.get(partido,0)+v
    return sorted([{"partido":p,"votos":v} for p,v in votos.items()], key=lambda x: x['votos'], reverse=True)

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/nacional')
def api_nacional():
    return jsonify(leer_nacional())

@app.route('/api/region')
def api_region():
    nivel = request.args.get('nivel','departamento')
    codigo = request.args.get('codigo','04')
    resultados = leer_region(nivel, codigo)
    codigo_full = codigo.zfill(6) if nivel=="distrito" else (codigo.zfill(4)+"00" if nivel=="provincia" else codigo.zfill(2)+"0000")
    lugar = get_full(codigo_full)
    return jsonify({"lugar":lugar,"resultados":resultados})

@app.route('/api/departamentos')
def api_departamentos():
    return jsonify([{"codigo":k,"nombre":v["nombre"]} for k,v in sorted(UBIGEOS.items()) if v["tipo"]=="departamento"])

@app.route('/api/provincias')
def api_provincias():
    dpto = request.args.get('dpto','')
    return jsonify([{"codigo":k,"nombre":v["nombre"]} for k,v in sorted(UBIGEOS.items()) if v["tipo"]=="provincia" and k.startswith(dpto[:2])])

@app.route('/api/distritos')
def api_distritos():
    prov = request.args.get('prov','')
    return jsonify([{"codigo":k,"nombre":v["nombre"]} for k,v in sorted(UBIGEOS.items()) if v["tipo"]=="distrito" and k.startswith(prov[:4])])

HTML = open('/home/ec2-user/dashboard.html').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
