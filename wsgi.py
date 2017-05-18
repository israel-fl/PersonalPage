from app import create_app, socketio

app = create_app(debug=True)


if __name__ == "__main__":
    app.config.update(TEMPLATES_AUTO_RELOAD=True)
    socketio.run(app, host="0.0.0.0", port=8080)
