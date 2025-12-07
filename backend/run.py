import eventlet
eventlet.monkey_patch()

from flask import send_from_directory
from app import create_app, socketio   # ← FIX IMPORT
import os

# Crear instancia de la app
app = create_app()

# Ruta base del frontend
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")
FRONTEND_ASSETS = os.path.join(FRONTEND_DIST, "assets")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """
    Servir archivos estáticos generados por Vite.
    """

    # Si es un asset (JS, CSS, imágenes)
    asset_path = os.path.join(FRONTEND_DIST, path)
    if path and os.path.exists(asset_path):
        return send_from_directory(FRONTEND_DIST, path)

    # Default -> index.html
    return send_from_directory(FRONTEND_DIST, "index.html")


# Crear tablas solo en entorno local
if os.environ.get("ENV", "local") == "local":
    with app.app_context():
        from app.models import db
        db.create_all()

# Ejecutar localmente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
