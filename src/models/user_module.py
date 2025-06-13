from app import db


completed_modules_table = db.Table(
    "completed_modules",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("module_id", db.Integer, db.ForeignKey("modules.id"), primary_key=True),
)
