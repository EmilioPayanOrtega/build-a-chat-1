import eventlet
eventlet.monkey_patch()   # ⬅️ Obligatorio para evitar bloqueos del servidor

from app import create_app, socketio
import os

# Crear instancia de la app
app = create_app()

# Inicializar la base de datos dentro del contexto
with app.app_context():
    from app.models import db
    db.create_all()  # Seguro aquí; no interfiere con eventlet

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    # Ejecución con eventlet — modo recomendado para WebSockets
    # "allow_unsafe_werkzeug=False" se evita para mantener compatibilidad con eventlet
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=False,         # ⚠️ Evita auto-reload, causa problemas con socketio + eventlet
        use_reloader=False   # ⬅️ CRUCIAL: eventlet NO soporta el reloader de Flask
    )
