"""
IP-Control: API REST con Flask para el inventario de direccionamiento IP.
Asignatura: Programación en Redes
Los datos usan redes privadas de ejemplo (RFC 1918), no direcciones reales.
"""
from flask import Flask, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Inventario de ejemplo (en memoria). Personaliza nombres y datos como tuyos.
# ---------------------------------------------------------------------------
direcciones = [
    {"id": 1, "direccion_ip": "192.168.10.1",   "dispositivo": "Router-Principal", "subred": "192.168.10.0", "tipo_asignacion": "estatica", "estado": "asignada"},
    {"id": 2, "direccion_ip": "192.168.10.10",  "dispositivo": "Servidor-Archivos", "subred": "192.168.10.0", "tipo_asignacion": "estatica", "estado": "asignada"},
    {"id": 3, "direccion_ip": "192.168.10.50",  "dispositivo": "Laptop-Docente",   "subred": "192.168.10.0", "tipo_asignacion": "DHCP",     "estado": "asignada"},
    {"id": 4, "direccion_ip": "192.168.10.51",  "dispositivo": "Sin asignar",      "subred": "192.168.10.0", "tipo_asignacion": "DHCP",     "estado": "disponible"},
    {"id": 5, "direccion_ip": "192.168.20.1",   "dispositivo": "Switch-Lab",       "subred": "192.168.20.0", "tipo_asignacion": "estatica", "estado": "asignada"},
    {"id": 6, "direccion_ip": "192.168.20.100", "dispositivo": "Sin asignar",      "subred": "192.168.20.0", "tipo_asignacion": "DHCP",     "estado": "disponible"},
    {"id": 7, "direccion_ip": "10.0.0.20",      "dispositivo": "Impresora-Red",    "subred": "10.0.0.0",     "tipo_asignacion": "estatica", "estado": "asignada"},
    {"id": 8, "direccion_ip": "10.0.0.21",      "dispositivo": "Sin asignar",      "subred": "10.0.0.0",     "tipo_asignacion": "DHCP",     "estado": "disponible"},
]


# GET /  -> estado de la API
@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "Bienvenido a IP-Control API",
        "estado": "La API funciona correctamente",
        "endpoints": [
            "/direcciones",
            "/direcciones/<id>",
            "/direcciones/estado/<estado>",
            "/direcciones/subred/<subred>",
        ],
    }), 200


# GET /direcciones  -> todas las direcciones
@app.route("/direcciones", methods=["GET"])
def obtener_direcciones():
    return jsonify({"total": len(direcciones), "direcciones": direcciones}), 200


# GET /direcciones/<id>  -> una direccion por id (404 si no existe)
@app.route("/direcciones/<int:id_registro>", methods=["GET"])
def obtener_direccion(id_registro):
    for registro in direcciones:
        if registro["id"] == id_registro:
            return jsonify(registro), 200
    return jsonify({
        "error": "No encontrado",
        "mensaje": f"No existe un registro con id {id_registro}",
    }), 404


# GET /direcciones/estado/<estado>  -> filtra por 'asignada' o 'disponible'
@app.route("/direcciones/estado/<estado>", methods=["GET"])
def filtrar_por_estado(estado):
    resultado = [d for d in direcciones if d["estado"].lower() == estado.lower()]
    return jsonify({"estado": estado, "total": len(resultado), "direcciones": resultado}), 200


# GET /direcciones/subred/<subred>  -> filtra por subred (ej. 192.168.10.0)
@app.route("/direcciones/subred/<subred>", methods=["GET"])
def filtrar_por_subred(subred):
    resultado = [d for d in direcciones if d["subred"] == subred]
    return jsonify({"subred": subred, "total": len(resultado), "direcciones": resultado}), 200


# Respuesta JSON para rutas que no existen (en lugar de la pagina HTML por defecto)
@app.errorhandler(404)
def ruta_no_encontrada(e):
    return jsonify({"error": "No encontrado", "mensaje": "La ruta solicitada no existe"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
