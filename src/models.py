from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)
    birth_year = db.Column(db.Integer(), unique=False, nullable=False)
    home_planet = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "name": self.name,
            "gender": self.email,
            "birth_year": self.birth_year,
            "home_planet": self.home_planet
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer(), nullable=False)
    diameter = db.Column(db.Integer(), nullable=False)
    climate = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "name": self.name,
            "population": self.population,
            "diameter": self.diameter,
            "climate": self.climate
        }
