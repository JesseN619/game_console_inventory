from flask import Blueprint, request, jsonify
from console_inventory.helpers import token_required
from console_inventory.models import db, User, Console, console_schema, consoles_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'a_value': 'hello', 'another_value': 'world'}

# CREATE CONSOLE ENDPOINT
@api.route('/consoles', methods = ['POST'])
@token_required
def create_console(current_user_token):
    name = request.json['name']
    release_date = request.json['release_date']
    price = request.json['price']
    company = request.json['company']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    console = Console(name, release_date, price, company, user_token = user_token)

    db.session.add(console)
    db.session.commit()

    response = console_schema.dump(console)
    return jsonify(response)

#Retrieve all consoles
@api.route('/consoles', methods = ['GET'])
@token_required
def get_consoles(current_user_token):
    owner = current_user_token.token
    consoles = Console.query.filter_by(user_token = owner).all()
    response = consoles_schema.dump(consoles)
    return jsonify(response)

# Retrieve single console
@api.route('/consoles/<id>', methods = ['GET'])
@token_required
def get_console(current_user_token, id):
    console = Console.query.get(id)
    response = console_schema.dump(console)
    return jsonify(response)

# Update a console by ID endpoint
@api.route('/consoles/<id>', methods = ['POST'])
@token_required
def update_console(current_user_token, id):
    console = Console.query.get(id)
    print(console)
    if console:
        console.name = request.json['name']
        console.release_date = request.json['release_date']
        console.price = request.json['price']
        console.company = request.json['company']
        console.user_token = current_user_token.token

        db.session.commit()

        response = console_schema.dump(console)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That console does not exist!'})

# Delete console by ID
@api.route('/consoles/<id>', methods = ['DELETE'])
@token_required
def delete_console(current_user_token, id):
    console = Console.query.get(id)
    if console:
        db.session.delete(console)
        db.session.commit()

        response = console_schema.dump(console)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That console does not exist!'})