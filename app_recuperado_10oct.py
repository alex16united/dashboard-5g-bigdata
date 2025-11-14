from flask import Flask, render_template
import folium
import csv

app = Flask(__name__)

@app.route('/')
def mapa():
    # Crear mapa centrado en Madrid
    mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=11, tiles="OpenStreetMap")

    # Leer CSV de antenas
    with open("data/antenas_madrid.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for fila in reader:
            try:
                lat = float(fila["Latitud"])
                lon = float(fila["Longitud"])
                capacidad = float(fila["Capacidad_MB"])
                nombre = fila["Antena"]
                tecnologia = fila.get("Tecnologia", "")

                # Color según tecnología o capacidad
                color = "red" if (tecnologia == "5G" or capacidad > 4800) else "blue"

                # Marcador principal
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=10,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.9,
                    popup=f"<b>{nombre}</b><br>Tecnología: {tecnologia}<br>Capacidad: {capacidad} MB"
                ).add_to(mapa)

                # Capa animada (onda expansiva)
                folium.Circle(
                    location=[lat, lon],
                    radius=100,
                    color=color,
                    fill=True,
                    fill_opacity=0.15,
                ).add_to(mapa)

            except Exception as e:
                print("⚠️ Error al leer fila:", e)

    # Leyenda estática abajo a la izquierda
    leyenda_html = '''
     <div style="
       position: fixed;
       bottom: 20px; left: 20px;
       width: 160px; z-index:9999;
       background-color: white;
       border:2px solid grey;
       border-radius:8px;
       padding: 10px;
       font-size:14px;
       box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
     ">
       <b>📡 Leyenda de Antenas</b><br>
       <i style="background:red;width:10px;height:10px;display:inline-block;border-radius:50%;"></i> 5G (alta capacidad)<br>
       <i style="background:blue;width:10px;height:10px;display:inline-block;border-radius:50%;"></i> 4G (media capacidad)
     </div>
    '''
    mapa.get_root().html.add_child(folium.Element(leyenda_html))

    # Añadir animación CSS
    estilo_css = """
    <style>
      .leaflet-interactive {
        transition: transform 2s ease-in-out;
        animation: pulso 2s infinite ease-in-out;
      }
      @keyframes pulso {
        0%   { transform: scale(0.8); opacity: 0.5; }
        50%  { transform: scale(1.4); opacity: 0.2; }
        100% { transform: scale(0.8); opacity: 0.5; }
      }
    </style>
    """
    mapa.get_root().header.add_child(folium.Element(estilo_css))

    mapa.save("templates/mapa.html")
    return render_template("mapa.html")

if __name__ == "__main__":
    app.run(debug=True)

