import eventlet
eventlet.monkey_patch()

from app import create_app, socketio
import os

app = create_app()

# NO usar db.create_all() aquí — SQLAlchemy lo hará cuando se necesite
# Pero si quieres mantenerlo:
with app.app_context():
    from app.models import db
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
