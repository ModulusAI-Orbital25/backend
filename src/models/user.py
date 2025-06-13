from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from models.user_module import completed_modules_table


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("username", db.String(50), nullable=False, unique=True)
    display_name = db.Column("display_name", db.String(100), nullable=False)
    password_hash = db.Column("password", db.String(162), nullable=False)

    # Many-to-many relationship to Module
    completed_modules = db.relationship(
        "Module",
        secondary=completed_modules_table,
        back_populates="users_completed",
    )

    # One-to-one relationship to Academics
    academics = db.relationship(
        "Academics",
        uselist=False,
        back_populates="user",
    )

    def serialize(self):
        return {"id": self.id, "name": self.name, "display": self.display_name}

    def set_password(self, password_raw):
        self.password_hash = generate_password_hash(password_raw)

    def check_password(self, password_raw):
        return check_password_hash(self.password_hash, password_raw)
