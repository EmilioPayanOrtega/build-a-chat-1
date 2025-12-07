import eventlet
eventlet.monkey_patch()

from flask import send_from_directory
from backend.app import create_app, socketio
import os

# Crear instancia de la app
app = create_app()

# Rutas para servir el frontend desde /frontend/dist
FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
FRONTEND_ASSETS = os.path.join(FRONTEND_DIST, "assets")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """
    Servir archivos estáticos generados por Vite.
    """
    # Si el archivo existe dentro de /assets lo servimos
    asset_path = os.path.join(FRONTEND_ASSETS, path)
    if path.startswith("assets/") and os.path.exists(asset_path):
        return send_from_directory(FRONTEND_DIST, path)

    # Si existe el archivo general
    full_path = os.path.join(FRONTEND_DIST, path)
    if path != "" and os.path.exists(full_path):
        return send_from_directory(FRONTEND_DIST, path)

    # Ruta por defecto = index.html
    return send_from_directory(FRONTEND_DIST, "index.html")


# Crear tablas solo en entorno local
if os.environ.get("ENV", "local") == "local":
    with app.app_context():
        from app.models import db
        db.create_all()

# Ejecución local — Render no usa esto
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
