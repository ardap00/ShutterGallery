from app import create_app
from app.models import db, followers

app = create_app()
with app.app_context():
    followers.create(db.engine, checkfirst=True)
    print("Followers table forcefully created.")
