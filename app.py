from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

# Página principal
@app.route("/")
def index():
    return render_template("index.html", title="Inicio")

# Mapa de antenas
@app.route("/mapa")
def mapa():
    return render_template("mapa_antenas.html", title="Mapa de Antenas")

# Mapa de usuarios (ejemplo)
@app.route("/usuarios")
def usuarios():
    return render_template("mapa_usuarios.html", title="Mapa de Usuarios")

# Comparativa
@app.route("/comparativa")
def comparativa():
    return render_template("comparativa.html", title="Comparativa")

# Predicción
@app.route("/prediccion")
def prediccion():
    return render_template("prediccion.html", title="Predicción")

# Realidad virtual
@app.route("/vr")
def vr():
    return render_template("vr.html", title="VR")

# 🌱 NUEVA RUTA: Sostenibilidad
@app.route("/sostenibilidad")
def sostenibilidad():
    return render_template("sostenibilidad.html", title="Sostenibilidad")

# Endpoint JSON para datos de antenas
@app.route("/data")
def data():
    filas = []
    try:
        with open("data/antenas_madrid.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for r in reader:
                try:
                    lat = round(float(r.get("Latitud")), 6)
                    lon = round(float(r.get("Longitud")), 6)
                    filas.append({
                        "id": r.get("Antena"),
                        "nombre": r.get("Antena"),
                        "lat": lat,
                        "lon": lon,
                        "tipo": r.get("Tecnologia"),
                        "potencia": float(r.get("Capacidad_MB") or 10)
                    })
                except Exception as e:
                    print("❌ Error en fila:", e)
                    continue
    except FileNotFoundError:
        print("⚠️ No se encontró el archivo data/antenas_madrid.csv")

    return jsonify(filas)

if __name__ == "__main__":
    app.run(debug=True)


