from . import create_app

app, mail = create_app()


from . import routes  # Import routes

# me = User(name='john', email='vhjbhb')
# db.session.add(me)
# db.commit(me)

if __name__ == "__main__":
    app.run()