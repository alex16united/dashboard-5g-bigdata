import folium
import csv

m = folium.Map(location=[40.4168, -3.7038], zoom_start=11)

with open('data/antenas_madrid.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for r in reader:
        lat, lon = float(r['Latitud']), float(r['Longitud'])
        tec = r['Tecnologia']
        color = 'red' if tec == '5G' else 'blue'

        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=f"{r['Antena']}<br>{r['Zona']}<br>{r['Tecnologia']} - {r['Capacidad_MB']} MB"
        ).add_to(m)

        folium.Circle(
            location=[lat, lon],
            radius=230,
            color=color,
            fill=True,
            fill_opacity=0.18
        ).add_to(m)

leyenda = """
<div style='position: fixed; bottom: 30px; left: 30px; z-index:9999; background: white;
border: 2px solid grey; border-radius: 8px; padding: 10px; font-size: 14px;'>
<b>📡 Leyenda de Antenas</b><br>
<span style='color:red;'>●</span> 5G (alta capacidad)<br>
<span style='color:blue;'>●</span> 4G (media capacidad)
</div>
"""
m.get_root().html.add_child(folium.Element(leyenda))

m.save('templates/mapa.html')
print("✅ Mapa generado en templates/mapa.html")

