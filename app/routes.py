from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.planet import Planet
from app.route_helpers import validate_model

bp = Blueprint("planets", __name__, url_prefix="/planets")

@bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"],
                        description=request_body['description'],
                        radius=request_body['radius']
                        )
    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created", 201)

@bp.route("", methods=["GET"])
def read_all_planets():

    name_param = request.args.get("name")
    description_param = request.args.get("description")
    radius_param = request.args.get("radius")

    planet_query = Planet.query

    if name_param:
        planet_query = planet_query.filter_by(name=name_param)
    if description_param:
        planet_query = planet_query.filter(Planet.description.ilike(
            f"%{description_param}%"))
    if radius_param:
        # filter planets with a radius greater than query param
        # How can we give the option of filter lesser than or greater than?
        # Would we need to prompt the user to include that param and then build
        # conditionals to check if they want to find greater or less than?
        planet_query = planet_query.filter(Planet.radius>radius_param)
    
    planets_response = [planet.to_dict() for planet in planet_query]
    
    return jsonify(planets_response)


@bp.route("/<planet_id>", methods=["GET"])
def read_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict()

@bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius = request_body["radius"]

    db.session.commit()

    return make_response(jsonify(f"Planet #{planet.id} successfully updated"), 200)


@bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()

    return make_response(jsonify(f"Planet #{planet_id} successfully deleted"), 200)


# class Planet:

#     def __init__(self, id, name, description, radius):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.radius = radius


# planets = [
#     Planet(1, "Mercury", "Closest planet to the sun", 1516),
#     Planet(2, "Venus", "Hottest planet in our solar system", 3760.4),
#     Planet(3, "Earth", "You are here!", 3958.8),
#     Planet(4, "Mars", "Also known as the Red Planet", 1516),
#     Planet(5, "Jupiter", "Largest planet in our solar system", 43441),
#     Planet(6, "Saturn", "Planet with the lowest mean density", 36184),
#     Planet(7, "Uranus", "Planet with the most extreme seasons in our solar system", 15759),
#     Planet(8, "Neptune", "Farthest planet from the sun", 15299),
# ]

# planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# @planets_bp.route("", methods=["GET"])
# def get_planets():
#     planets_response = []
    
#     for planet in planets:
#         planet_dict = {
#             "id":planet.id,
#             "name": planet.name,
#             "description": planet.description,
#             "radius": planet.radius
#         }
#         planets_response.append(planet_dict)

#     return jsonify(planets_response)

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"message":f"planet {planet_id} invalid"}, 400))
    
#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
#     abort(make_response({"message":f"planet {planet_id} not found"}, 404))

# @planets_bp.route("/<planet_id>", methods=["GET"])
# def get_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return dict(
#         id=planet.id,
#         name=planet.name,
#         description=planet.description,
#     )
