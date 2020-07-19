from app import routes, db
from app.models import User

routes


me = User(name='john', email='vhjbhb')
db.session.add(me)
db.commit(me)
