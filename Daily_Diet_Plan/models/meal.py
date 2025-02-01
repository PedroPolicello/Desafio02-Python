from datetime import datetime
from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # O autoincrement já é ativado automaticamente
    name = db.Column(db.String(100), nullable=False)  # Nome obrigatório, máx. 100 caracteres
    description = db.Column(db.Text, nullable=True)   # Texto grande opcional
    dateTime = db.Column(db.String(10), nullable=False)  # Data como texto livre e obrigatório
    inDiet = db.Column(db.Boolean, nullable=False, default=False)  # Se está dentro da dieta, padrão True