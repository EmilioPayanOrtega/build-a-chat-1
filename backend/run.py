from gevent import monkey
monkey.patch_all()
from app import create_app, socketio

app = create_app()

with app.app_context():
    from app.models import db
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
