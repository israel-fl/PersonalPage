from app import create_app, socketio
from flask import render_template
app = create_app()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)
