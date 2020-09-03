from . import create_app
app, mail = create_app()


from . import routes  # Import routes

if __name__ == "__main__":
    app.run()