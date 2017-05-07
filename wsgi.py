from app.app import socketio, app


if __name__ == "__main__":
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
