import eventlet
eventlet.monkey_patch()

from app import create_app, socketio
import os

# Crear instancia de la app
app = create_app()

# Crear tablas SOLO en entorno local (evita errores en Render)
if os.environ.get("ENV", "local") == "local":
    with app.app_context():
        from app.models import db
        db.create_all()

# Ejecución local — NO se usa en Render (Render usa gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
