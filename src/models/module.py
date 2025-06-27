from app import db

class Module(db.Model):
    __tablename__: str = "modules"

    id = db.Column("id", db.Integer, primary_key=True)
    code = db.Column("code", db.String(20), nullable=False, unique=True)
    title = db.Column("title", db.String(150), nullable=False)
    # Add other searchable information here

