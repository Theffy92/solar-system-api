from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.moon import Moon
from app.route_helpers import validate_model

bp= Blueprint("moons", __name__, url_prefix="/moons")

# @bp.route("", methods=["POST"])
# def create_moon():
#     request_body = request.get_json()
#     new_moon = Moon(name=request_body["name"],
#                         description=request_body['description'],
#                         radius=request_body['radius']
#                         )
#     db.session.add(new_planet)
#     db.session.commit()