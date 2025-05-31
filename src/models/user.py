from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("username", db.String(50))
    display_name = db.Column("display_name", db.String(100))

    def serialize(self):
        return {"id": self.id, "name": self.name, "display": self.display_name}
