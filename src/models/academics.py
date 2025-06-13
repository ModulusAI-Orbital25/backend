from app import db
from models.academics_module import completed_modules_table


class Academics(db.Model):
    __tablename__ = "academics"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    primaryMajor = db.Column("primaryMajor", db.String(100), nullable=False)
    secondaryMajor = db.Column("secondaryMajor", db.String(100), nullable=True)
    minor1 = db.Column("minor1", db.String(100), nullable=True)
    minor2 = db.Column("minor2", db.String(100), nullable=True)
    completedModules = db.Column("completedModules", db.String(400), nullable=False)
    currentSemester = db.Column("currentSemester", db.Integer, nullable=False)
    internshipSem = db.Column("internshipSem", db.Integer, nullable=True)

    # One-to-one relationship to User
    user = db.relationship(
        "User",
        back_populates="academics",
    )

    # Many-to-many relationship to Module
    completed_modules = db.relationship(
        "Module",
        secondary=completed_modules_table,
        back_populates="users_completed",
    )

    def serialize(self):
        return {
            "id": self.user_id,
            "primaryMajor": self.primaryMajor,
            "secondaryMajor": self.secondaryMajor,
            "minor1": self.minor1,
            "minor2": self.minor2,
            "completedModules": self.completedModules,
            "currentSemester": self.currentSemester,
            "internshipSem": self.internshipSem,
        }
