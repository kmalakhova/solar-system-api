from app import db 
from models.planet import Planet
from flask import request, Blueprint, make_response, jsonify 

planet_bp = Blueprint("planets", __name__, url_prefix="/planets") 

@planet_bp.route("add-planet", methods=["POST"])
def add_planet():    
    """Adds a new planet record to the DB table"""
    request_body = request.get_json() 
    new_planet = Planet(
        name=request_body["name"],
        description=request_body["description"], 
        order=request_body["order"] 
    )
    
    db.session.add(new_planet) 
    db.session.commit() 

    return jsonify(f"Planet {new_planet.name} has been successfully added."), 201 

@planet_bp.route("/all-planets", methods=["GET"])
def get_all_planets():
    """Gets data of the existing planets in the DB table"""
    all_planets = Planet.query.all() 
    response = [] 

    if all_planets: 
        for planet in all_planets:
            response.append({
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "order": planet.order
                })
        return jsonify(response), 200
    
    if len(response) == 0:
        print('hey there!')
        return jsonify(response), 200
    
    return({"message": "No planets were found."}, 404) 

@planet_bp.route("/<planet_id>", methods=["GET"]) 
def get_one_planet(planet_id):
    """Gets data of a particular planet"""
    planet = Planet.query.get(planet_id)

    if planet:
        return({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "order": planet.order
        }, 200)

    return({"message": f"Planet with id #{planet_id} was not found."}, 404) 

@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    """Updates a portion of a single planet's data"""
    planet = Planet.query.get(planet_id)
    
    if planet:
        request_body = request.get_json()
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.order = request_body["order"]

        db.session.commit()
        return ({"message": f"Planet {planet_id} was successfully updated."}, 200)

    return ({"message": f"Planet with id #{planet_id} was not found."}, 404)

@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    """Deletes a planet from the database"""
    planet = Planet.query.get(planet_id)

    if planet:
        db.session.delete(planet)
        db.session.commit()
        return ({"message": f"Planet with id {planet_id} has been deleted."}, 200)

    return ({"message": f"Planet with id #{planet_id} was not found."}, 404)
    