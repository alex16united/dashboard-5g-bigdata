import requests

API_KEY = "pk.1e88cb95532b119759c306044514d836"

# Coordenadas de Madrid (sur, oeste, norte, este)
bbox = "40.32,-3.90,40.52,-3.55"

url = f"https://api.opencellid.org/cell/getInArea?key={API_KEY}&bbox={bbox}&format=csv"

print("📡 Descargando datos reales de antenas 4G/5G de Madrid...")
r = requests.get(url)

if r.status_code == 200 and len(r.text) > 100:
    with open("antenas_madrid_reales.csv", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("✅ Archivo guardado correctamente como antenas_madrid_reales.csv")
else:
    print("⚠️ No se recibieron datos válidos o hubo un error.")
    print("Código:", r.status_code)
    print(r.text[:500])



