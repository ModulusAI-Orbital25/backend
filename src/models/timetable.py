
from models import db
from models.academics import Academics 

class Timetable(db.Model):
    __tablename__ = "timetables"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("academics.user_id"), unique=True, nullable=False)
    
    sem1 = db.Column(db.Text, default="")
    sem2 = db.Column(db.Text, default="")
    sem3 = db.Column(db.Text, default="")
    sem4 = db.Column(db.Text, default="")
    sem5 = db.Column(db.Text, default="")
    sem6 = db.Column(db.Text, default="")
    sem7 = db.Column(db.Text, default="")
    sem8 = db.Column(db.Text, default="")

    com1 = db.Column(db.Boolean)
    com2 = db.Column(db.Boolean)
    com3 = db.Column(db.Boolean)
    com4 = db.Column(db.Boolean)
    com5 = db.Column(db.Boolean)
    com6 = db.Column(db.Boolean)
    com7 = db.Column(db.Boolean)
    com8 = db.Column(db.Boolean)



    def serialize(self):
        return {
            "semesters": [
                {"semester": i+1, "modules": getattr(self, f"sem{i+1}").split(",") if getattr(self, f"sem{i+1}") else [], "completed": getattr(self, f"com{i+1}")}
                for i in range(8)
            ]
        }
