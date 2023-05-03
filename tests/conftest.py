import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planet


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_planet(app):
    planet = Planet(name="Mars", description="We are here!", radius="3958.8")
    db.session.add(planet)
    db.session.commit()
    return planet

@pytest.fixture
def saved_planets(app):
    mercury = Planet(name="Mercury",
                     description = "Closest planet to the sun",
                     radius=1516)
    venus = Planet(name="Venus",
                   description= "Hottest planet in our solar system.",
                   radius=3760.4)
    mars=Planet(name="Mars",
                description="Also known as the Red Planet",
                radius=1511)
    
    db.session.add_all([mercury, venus, mars])
    db.session.commit()