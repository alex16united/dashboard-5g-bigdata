from flask import Flask, render_template
import folium
import csv

app = Flask(__name__)

@app.route('/')
def mapa():
    # Crear mapa centrado en Madrid
    mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=11)

    # Leer datos del CSV
    with open('data/antenas_madrid.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for fila in reader:
            try:
                lat = float(fila['Latitud'])
                lon = float(fila['Longitud'])
                nombre = fila['Antena']
                zona = fila['Zona']
                tecnologia = fila['Tecnologia']
                capacidad = float(fila['Capacidad_MB'])

                color = 'red' if tecnologia == '5G' else 'blue'

                # Punto principal
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=8,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.9,
                    popup=f"<b>{nombre}</b><br>Zona: {zona}<br>Tecnología: {tecnologia}<br>Capacidad: {capacidad} MB"
                ).add_to(mapa)

                # Onda expansiva (animación visual, no movimiento del punto)
                folium.Circle(
                    location=[lat, lon],
                    radius=250,
                    color=color,
                    fill=True,
                    fill_opacity=0.2
                ).add_to(mapa)

            except Exception as e:
                print("⚠️ Error en fila:", e)

    # Leyenda (como la original del 10 de octubre)
    leyenda_html = '''
     <div style="
       position: fixed;
       bottom: 30px;
       left: 30px;
       width: 180px;
       z-index:9999;
       background-color:white;
       border:2px solid grey;
       border-radius:8px;
       padding:10px;
       font-size:14px;
       box-shadow:2px 2px 6px rgba(0,0,0,0.3);
     ">
       <b>📡 Leyenda de Antenas</b><br>
       <i style="background:red;width:10px;height:10px;display:inline-block;border-radius:50%;"></i> 5G (alta capacidad)<br>
       <i style="background:blue;width:10px;height:10px;display:inline-block;border-radius:50%;"></i> 4G (media capacidad)
     </div>
    '''
    mapa.get_root().html.add_child(folium.Element(leyenda_html))

    # Animación CSS sutil (efecto pulso)
    estilo_css = """
    <style>
    @keyframes pulso {
        0% { transform: scale(1); opacity: 0.4; }
        50% { transform: scale(1.8); opacity: 0.1; }
        100% { transform: scale(1); opacity: 0.4; }
    }
    .leaflet-interactive[fill-opacity="0.2"] {
        animation: pulso 3s infinite ease-in-out;
    }
    </style>
    """
    mapa.get_root().header.add_child(folium.Element(estilo_css))

    mapa.save('templates/mapa.html')
    return render_template('mapa.html')


if __name__ == '__main__':
    app.run(debug=True)


