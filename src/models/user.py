from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("username", db.String(50), nullable=False)
    display_name = db.Column("display_name", db.String(100), nullable=False)
    password_hash = db.Column("password", db.String(128), nullable=False)

    def serialize(self):
        return {"id": self.id, "name": self.name, "display": self.display_name}

    def set_password(self, password_raw):
        self.password_hash = generate_password_hash(password_raw)

    def check_password(self, password_raw):
        return check_password_hash(self.password_hash, password_raw)
