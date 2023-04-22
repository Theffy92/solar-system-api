from flask import Blueprint, jsonify

class Planet:

    def __init__(self, id, name, description, radius):
        self.id = id
        self.name = name
        self.description = description
        self.radius = radius


planets = [
    Planet(1, "Mercury", "Closest planet to the sun", 1516),
    Planet(2, "Venus", "Hottest planet in our solar system", 3760.4),
    Planet(3, "Earth", "You are here!", 3958.8),
    Planet(4, "Mars", "Also known as the Red Planet", 1516),
    Planet(5, "Jupiter", "Largest planet in our solar system", 43441),
    Planet(6, "Saturn", "Planet with the lowest mean density", 36184),
    Planet(7, "Uranus", "Planet with the most extreme seasons in our solar system", 15759),
    Planet(8, "Neptune", "Farthest planet from the sun", 15299),
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