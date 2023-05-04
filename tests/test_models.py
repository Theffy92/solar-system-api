from app.models.planet import Planet
import pytest

def test_to_dict_no_missing_data():
    test_data = Planet(id=1,
        name="Mercury",
        description="Closest planet to the sun",
        radius= 1516
    )

    result = test_data.to_dict()

    assert len(result) == 4
    assert result['id'] == 1
    assert result['name'] == "Mercury"
    assert result['description']=="Closest planet to the sun"
    assert result['radius']==1516

def test_to_dict_missing_name():
    test_data = Planet(id=1,
        description="Closest planet to the sun",
        radius= 1516
    )

    result = test_data.to_dict()

    assert len(result) == 4
    assert result['id'] == 1
    assert result['name'] is None
    assert result['description']=="Closest planet to the sun"
    assert result['radius']==1516

def test_to_dict_missing_description():
    test_data = Planet(id=1,
        name="Mercury",
        radius= 1516
    )

    result = test_data.to_dict()

    assert len(result) == 4
    assert result['id'] == 1
    assert result['name'] == "Mercury"
    assert result['description'] is None
    assert result['radius']==1516

def test_from_dict_returns_planet():
    planet_data= {
        "name": "Mercury",
        "description":"Closest planet to the sun",
        "radius": 1516
    }

    new_planet = Planet.from_dict(planet_data)

    assert new_planet.name=="Mercury"
    assert new_planet.description=="Closest planet to the sun"
    assert new_planet.radius == 1516

def test_from_dict_with_no_name():
    planet_data= dict(
        description= "Closest planet to the sun",
        radius=1516
    )

    with pytest.raises(KeyError, match='name'):
        new_planet = Planet.from_dict(planet_data)