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
    assert response_body == {'message': 'planet 200 not found'}

