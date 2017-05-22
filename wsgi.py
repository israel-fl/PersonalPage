from app import create_app, socketio, db
from flask import render_template
app = create_app()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    # start the database engine
    db.create_all()
    socketio.run(app, host="0.0.0.0", port=8080)
