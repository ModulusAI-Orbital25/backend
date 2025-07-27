from app import db


class Module(db.Model):
    __tablename__: str = "modules"

    id = db.Column("id", db.Integer, primary_key=True)
    code = db.Column("code", db.String(20), nullable=False, unique=True)
    title = db.Column("title", db.String(150), nullable=False)
    description = db.Column("description", db.Text, nullable=False)
    credit = db.Column("credit", db.Float, nullable=False)
    # Extra information might be stored, including department, faculty, ...
    # Prereq tree can be store as text
    # Add other searchable information here
