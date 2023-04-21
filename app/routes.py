from flask import Blueprint, jsonify

class Planet:

    def __init__(self, id, name, description, radius):
        self.id = id
        self.name = name
        self.description = description
        self.radius = radius


planets = [
    Planet(1, "Mercury", "First planet from the Sun", 1516),
    Planet(2, "Venus", "Second planet from the Sun", 3760.4),
    Planet(3, "Earth", "Third planet from the Sun", 3958.8)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_planets():
    planets_response = []
    
    for planet in planets:
        planet_dict = {
            "id":planet.id,
            "name": planet.name,
            "description": planet.description,
            "radius": planet.radius
        }

        planets_response.append(planet_dict)

    return jsonify(planets_response)