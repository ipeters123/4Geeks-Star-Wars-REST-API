"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)
# // line below edited in class

# // beginning user section


@app.route('/user', methods=['GET'])
def handle_hello():

    users_query = User.query.all()

    all_user = list(map(lambda x: x.serialize(), users_query))

    return jsonify(all_user), 200


@app.route('/user', methods=['POST'])
def createUser():
    body = request.get_json()
    if body == None:
        return "The request body is null", 400
    if 'email' not in body:
        return "Add the email", 400
    if 'password' not in body:
        return "Add user password", 400
    if 'is_active' not in body:
        return "Add if the user if active", 400

    new_user = User(
        email=body["email"], password=body["password"], is_active=body["is_active"])
    db.session.add(new_user)
    db.session.commit()

    return 'User was added', 200


@app.route('/user/<int:id>', methods=['PUT'])
def updateUser(id):
    user1 = User.query.get(id)
    print(user1.email)
    body = request.get_json()
    if body == None:
        return 'Body is empty', 400
    if 'email' not in body:
        return "Add the user email", 400

    user1.email = body["email"]
    db.session.commit()
    return 'ok'


@app.route('/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    user1 = User.query.get(id)
    if user1 == None:
        raise APIException('User does not exist', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return 'User deleted'


# // beginning characters section
@app.route('/characters', methods=['GET'])
def get_characters():

    characters_query = Characters.query.all()

    fave_characters = list(map(lambda x: x.serialize(), characters_query))

    return jsonify(fave_characters), 200


@app.route('/characters', methods=['POST'])
def new_character():
    body = request.get_json()
    if body == None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add character name", 400
    if 'gender' not in body:
        return "Add character gender", 400
    if 'birth_year' not in body:
        return "Add character birth year", 400
    if 'home_planet' not in body:
        return "Add character home planet", 400

    new_character = Characters(name=body["name"], gender=body["gender"],
                               birth_year=body["birth_year"], home_planet=body["home_planet"])
    db.session.add(new_character)
    db.session.commit()
    return 'Thank you!', 200


@app.route('/characters/<int:id>', methods=['PUT'])
def updateCharacters(id):
    character1 = Characters.query.get(id)
    print(character1.name)
    body = request.get_json()
    if body == None:
        return 'Body is empty', 400
    if 'name' not in body:
        return "Add the character name", 400

    character1.name = body["name"]
    db.session.commit()
    return 'ok'


@app.route('/characters/<int:id>', methods=['DELETE'])
def deleteCharacter(id):
    character1 = Characters.query.get(id)
    if character1 == None:
        raise APIException('Character does not exist', status_code=404)
    db.session.delete(character1)
    db.session.commit()
    return 'Character deleted'


# // beginning planets section
@app.route('/planets', methods=['GET'])
def get_planets():

    planets_query = Planets.query.all()

    planet = list(map(lambda x: x.serialize(), Planets_query))

    return jsonify(planet), 200


@app.route('/planets', methods=['POST'])
def planet():
    body = request.get_json()
    if body == None:
        return "The request body is null", 400
    if 'name' not in body:
        return "Add planet", 400
    if 'population' not in body:
        return "Add population", 400
    if 'diameter' not in body:
        return "Add diameter", 400
    if 'climate' not in body:
        return "Add climate", 400

    planet = Planets(name=body["name"], population=body["population"],
                     diameter=body["diameter"], climate=body["climate"])
    db.session.add(planet)
    db.session.commit()
    return 'Thank you!', 200


@app.route('/planets/<int:id>', methods=['PUT'])
def updatePlanets(id):
    planet1 = Planets.query.get(id)
    print(planet1.name)
    body = request.get_json()
    if body == None:
        return 'Body is empty', 400
    if 'name' not in body:
        return "Add the planet name", 400

    planet1.name = body["name"]
    db.session.commit()
    return 'ok'


@app.route('/planets/<int:id>', methods=['DELETE'])
def deletePlanet(id):
    planet1 = Planets.query.get(id)
    if planet1 == None:
        raise APIException('Planet does not exist', status_code=404)
    db.session.delete(planet1)
    db.session.commit()
    return 'Planet deleted'


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
