from app import create_app
from extensions import socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0', allow_unsafe_werkzeug=True)

