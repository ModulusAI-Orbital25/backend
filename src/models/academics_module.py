from app import db


completed_modules_table = db.Table(
    "completed_modules",
    db.Column(
        "academics_id", db.Integer, db.ForeignKey("academics.user_id"), primary_key=True
    ),
    db.Column("module_id", db.Integer, db.ForeignKey("modules.id"), primary_key=True),
)
