from app.route_helpers import validate_model
from app.models.planet import Planet
from werkzeug.exceptions import HTTPException
import pytest

def test_get_all_planets_with_no_records(client):
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_one_planet(client, one_planet):
    response = client.get(f"/planets/{one_planet.id}")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["name"] == one_planet.name
    assert response_body["description"] == one_planet.description
    assert response_body["radius"] == one_planet.radius

def test_get_one_planet_from_empty_database(client):
    response = client.get(f"/planets/200")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {'message': 'Planet 200 not found'}
    
def test_get_all_planets_from_database(client, saved_planets):
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body[0] == {"id": 1,
        "name": "Mercury",
        "description":"Closest planet to the sun",
        "radius":float(1516)
    }
    assert response_body[1]["name"] == "Venus"
    assert response_body[1]["description"] == "Hottest planet in our solar system."
    assert response_body[1]["radius"] == 3760.4
    assert response_body[2]["name"] == "Mars"
    assert response_body[2]["description"] == "Also known as the Red Planet"
    assert response_body[2]["radius"] == 1511

def test_create_one_planet(client):
    EXPECTED_PLANET= dict(
        name= "Jupiter",
        description= "Largest planet in our solar system.",
        radius= 43441
    )
    response = client.post("/planets", json= EXPECTED_PLANET)
    response_body = response.get_data(as_text=True)

    assert response.status_code == 201
    assert response_body == f"Planet {EXPECTED_PLANET['name']} successfully created"

def test_validate_planet(saved_planets):
    result = validate_model(Planet, 1)
    assert result.id == 1
    assert result.name == "Mercury"
    assert result.description == "Closest planet to the sun"
    assert result.radius == 1516

def test_validate_nonint_planet(saved_planets):
    with pytest.raises(HTTPException):
        validate_model(Planet, "three")

def test_validate_nonexisting_planet(saved_planets):
    with pytest.raises(HTTPException):
        validate_model(Planet, 356)

def test_update_planet(client, saved_planets):
    test_data={
        "name": "Mercurio",
        "description": "El planeta más cercano al sol",
        "radius": 1516
    }

    response = client.put("/planets/1", json=test_data)
    response_body= response.get_json()

    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_with_extra_keys(client, saved_planets):
    test_data={"extra": "some stuff",
               "name": "New Planet",
               "description": "The best planet",
               "radius": 1516.8,
               "another": "last value"}
    
    response = client.put("/planets/1", json=test_data)
    response_body= response.get_json()

    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_missing_record(client, saved_planets):
    test_data = {
        "name": "New Planet",
        "description": "The Best!",
        "radius": 254.2
    }

    response = client.put("/planets/4", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message":"Planet 4 not found"}

def test_delete_planet(client, saved_planets):
    # Act
    response = client.delete("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully deleted"

def test_delete_planet_missing_record(client, saved_planets):
    # Act
    response = client.delete("/planets/4")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 4 not found"}

def test_delete_planet_invalid_id(client, saved_planets):
    # Act
    response = client.delete("/planets/luna")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet luna invalid"}



