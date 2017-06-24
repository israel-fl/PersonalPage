from app import create_app, socketio
from database.db_adapter import db
from flask import render_template

app = create_app()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


if __name__ == "__main__":
    # start the database engine
    socketio.run(app, host="0.0.0.0", port=8080)
