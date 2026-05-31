from app import create_app
from app.models import db

app = create_app()
with app.app_context():
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Tables in metadata: {db.metadata.tables.keys()}")
