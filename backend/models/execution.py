# backend/models/execution.py

from models import db
from datetime import datetime

class Execution(db.Model):
    __tablename__ = 'executions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=True)
    error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Execution {self.id} - {self.language}>"
